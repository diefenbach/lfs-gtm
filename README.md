# lfs-gtm

Google Tag Manager for [LFS](https://github.com/diefenbach/django-lfs) shops: loads the GTM container with Google
Consent Mode v2, applies the visitor's choice from [lfs-cookie-consent](https://github.com/diefenbach/lfs_cookie_consent),
and pushes the GA4 e-commerce events of the shop (`view_item_list`, `view_item`, `add_to_cart`, `begin_checkout`,
`purchase`) to the `dataLayer`.

What it does not do: the cookie banner (that is lfs-cookie-consent) and the configuration inside Google Tag Manager
(triggers, GA4 tags), which you set up in your GTM container (see [Set up the GTM container](#set-up-the-gtm-container)).

## Installation

```sh
pip install lfs-gtm
```

This installs lfs-cookie-consent as well: without a consent banner GTM never gets consent. Add both apps, `lfs_gtm`
after `lfs_cookie_consent`, and your container ID:

```python
INSTALLED_APPS = [
    # ...
    "lfs_cookie_consent",
    "lfs_gtm",
]

GTM_ID = "GTM-XXXXXXX"
```

Without `GTM_ID` none of the tags renders anything, so a shop can install the app and switch GTM on per environment.

With [lfs-theme](https://github.com/diefenbach/lfs-theme) that is all: the theme includes every tag below when
`lfs_gtm` is installed. With your own theme, add the tags as described in [Templates](#templates).

## How it works

LFS builds tracker-neutral snapshots of what the visitor sees or buys (no GA4 field names), for example
`lfs.cart.utils.cart_items_to_tracking_snapshot` and `lfs.order.utils.order_to_tracking_snapshot`, and hands them
to the templates. lfs-gtm turns a snapshot into a GA4 event (`lfs_gtm/ga4_events.py`) and renders a small script that
pushes it to the `dataLayer`. GTM then fires the GA4 tags you configured for these event names.

```
LFS view → snapshot in the template context → lfs-gtm tag → dataLayer.push → GTM trigger → GA4 tag
```

lfs-gtm itself does not import LFS; the shop's views and templates connect the two. Empty snapshots render nothing.

## Consent Mode

`{% gtm_script %}` defines `dataLayer` and `gtag()`, sets the Consent Mode defaults (analytics and advertising
`denied`, `wait_for_update: 500`) and loads the container.

`lfs_gtm/lfs_gtm_consent.js` listens to the browser event `lfs:consent-changed` that lfs-cookie-consent fires when a
visitor saves a choice, and on every page load once a choice is stored. It then

- calls `gtag('consent', 'update', {analytics_storage, ad_storage})`,
- pushes `analytics_consent_granted` / `analytics_consent_denied` and `advertising_consent_granted` /
  `advertising_consent_denied` to the `dataLayer`,
- deletes the Google Analytics or Ads cookies of a category the visitor declined.

The event's `detail` carries `necessary`, `analytics` and `advertising` (booleans) and an optional `timestamp`.

## Templates

lfs-theme does this for you. In your own theme, the order in the base template matters: the consent adapter must
listen before lfs-cookie-consent fires its first `lfs:consent-changed`.

```django
{% load static lfs_cookie_consent_tags lfs_gtm_tags %}
<head>
    {% gtm_script %}
    <link rel="stylesheet" href="{% static 'lfs_cookie_consent/lfs_cookie_consent.css' %}">
</head>
<body>
    {% gtm_noscript %}
    {% cookie_banner %}
    {% cookie_modal %}
    ...
    <script defer src="{% static 'lfs_cookie_consent/lfs_cookie_consent.js' %}"></script>
    <script defer src="{% static 'lfs_gtm/lfs_gtm_consent.js' %}"></script>
</body>
```

The e-commerce events, each in the template LFS renders for that page:

| Template | Tag | GA4 event | Fires |
|---|---|---|---|
| `lfs/catalog/category_base.html` | `{% view_item_list_script item_list_tracking %}` | `view_item_list` | on a category page with products, per page of the list |
| `lfs/search/search_results.html` | `{% view_item_list_script item_list_tracking %}` | `view_item_list` | on search results with a search term |
| `lfs/catalog/product_base.html` | `{% view_item_script product_tracking %}` | `view_item` | when the product page loads, for the variant shown |
| `lfs/cart/cart.html` | `{% added_to_cart_script added_to_cart_tracking %}` | `add_to_cart` | once after a product was added to the cart |
| `lfs/checkout/new_addresses.html` | `{% begin_checkout_script begin_checkout_tracking %}` | `begin_checkout` | once when the checkout starts (GET of the address step) |
| `lfs/checkout/thank_you_page.html` | `{% purchase_script order_tracking %}` | `purchase` | once on the thank-you page after an order |

`add_to_cart`, `begin_checkout` and `purchase` fire once per action: LFS stores the snapshot in the session where the
action happens (adding to the cart, "Checkout", placing the order) and takes it out on the page that shows the
result, so reloading that page does not count the action again. `view_item` and `view_item_list` fire on every page
load.

Not covered: `page_view` (comes from the GA4 configuration in GTM), `view_cart`, and a new `view_item` when the
visitor switches the variant on the product page without reloading it.

`{% datalayer_push event "element-id" %}` pushes any event dict you build yourself.

## Events

The GA4 events follow Google's recommended e-commerce events:

| Event | `ecommerce` fields |
|---|---|
| `view_item_list` | `item_list_id`, `item_list_name`, `currency`, `value`, `items` |
| `view_item`, `add_to_cart`, `begin_checkout` | `currency`, `value`, `items` |
| `purchase` | `transaction_id`, `currency`, `value`, `tax`, `shipping`, `items` |

Each item has `item_id` (the SKU), `item_name`, `price` and `quantity`. For a category list `item_list_id` is the
category's slug and `item_list_name` its name; for search results they are `search` and the search term.

## Set up the GTM container

In Google Tag Manager, for each event name above:

1. A trigger of type *Custom Event* with exactly that event name.
2. A GA4 event tag that sends the `ecommerce` data of the push (`items`, `value`, `currency`, `transaction_id`, …).
3. Consent: let the tags respect Consent Mode; the `*_consent_*` events can serve as additional triggers.

Checklist: `GTM_ID` set · base template in the order above · a trigger and GA4 tag per event · consent settings in
GTM match the categories of the banner.

## Adding an event

1. In LFS (or your shop): build a tracker-neutral snapshot and put it into the template context, through the session
   if it should fire once per action.
2. In `lfs_gtm/ga4_events.py`: a `build_ga4_<event>(snapshot)` that returns the GA4 payload, or `None`.
3. In `lfs_gtm/templatetags/lfs_gtm_tags.py`: a tag that calls it and renders `lfs_gtm/datalayer_event_script.html`.
4. In the template: load `lfs_gtm_tags` and use the tag.

## Development

```sh
uv sync --group test
uv run pytest
```

The tests of the snapshots and of where the events fire are in django-lfs (`lfs/catalog/tests/test_product_tracking.py`,
`lfs/catalog/tests/test_item_list_tracking.py`, `lfs/checkout/tests/test_begin_checkout_gtm.py`).

## License

MIT, see [LICENSE](LICENSE).
