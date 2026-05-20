from django import template
from django.conf import settings
from django.template.loader import render_to_string

from lfs_gtm.ga4_events import (
    build_ga4_add_to_cart,
    build_ga4_begin_checkout,
    build_ga4_purchase,
    build_ga4_view_item,
    build_ga4_view_item_list,
)

register = template.Library()


@register.simple_tag
def gtm_script(gtm_id=None):
    gtm_id = gtm_id or getattr(settings, "GTM_ID", None)
    return render_to_string("lfs_gtm/gtm_script.html", {"gtm_id": gtm_id})


@register.simple_tag
def gtm_noscript(gtm_id=None):
    gtm_id = gtm_id or getattr(settings, "GTM_ID", None)
    return render_to_string("lfs_gtm/gtm_noscript.html", {"gtm_id": gtm_id})


@register.simple_tag(takes_context=True)
def datalayer_push(context, event=None, element_id="datalayer-event"):
    gtm_id = getattr(settings, "GTM_ID", None)
    return render_to_string(
        "lfs_gtm/datalayer_event_script.html",
        {
            "event": event,
            "gtm_id": gtm_id,
            "element_id": element_id,
        },
    )


@register.simple_tag(takes_context=True)
def added_to_cart_script(context, snapshot=None):
    event = build_ga4_add_to_cart(snapshot)
    return datalayer_push(context, event=event, element_id="added-to-cart-event")


@register.simple_tag(takes_context=True)
def view_item_script(context, snapshot=None):
    event = build_ga4_view_item(snapshot)
    return datalayer_push(context, event=event, element_id="view-item-event")


@register.simple_tag(takes_context=True)
def view_item_list_script(context, snapshot=None):
    event = build_ga4_view_item_list(snapshot)
    return datalayer_push(context, event=event, element_id="view-item-list-event")


@register.simple_tag(takes_context=True)
def begin_checkout_script(context, snapshot=None):
    event = build_ga4_begin_checkout(snapshot)
    return datalayer_push(context, event=event, element_id="begin-checkout-event")


@register.simple_tag(takes_context=True)
def purchase_script(context, snapshot=None):
    event = build_ga4_purchase(snapshot)
    return datalayer_push(context, event=event, element_id="purchase-event")
