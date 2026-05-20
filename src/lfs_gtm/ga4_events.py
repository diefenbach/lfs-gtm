"""Map tracker-neutral shop snapshots to GA4 dataLayer event payloads."""


def build_ga4_add_to_cart(snapshot):
    """
    Convert a cart tracking snapshot from LFS into a GA4 add_to_cart event dict.
    """
    if not snapshot or not snapshot.get("line_items"):
        return None

    items = [
        {
            "item_id": line["sku"],
            "item_name": line["name"],
            "price": line["price"],
            "quantity": line["quantity"],
        }
        for line in snapshot.get("line_items", [])
    ]

    return {
        "event": "add_to_cart",
        "ecommerce": {
            "currency": snapshot.get("currency", "EUR"),
            "value": snapshot["value"],
            "items": items,
        },
    }


def build_ga4_view_item(snapshot):
    """
    Convert a product tracking snapshot from LFS into a GA4 view_item event dict.
    """
    if not snapshot or not snapshot.get("line_items"):
        return None

    items = [
        {
            "item_id": line["sku"],
            "item_name": line["name"],
            "price": line["price"],
            "quantity": line["quantity"],
        }
        for line in snapshot.get("line_items", [])
    ]

    return {
        "event": "view_item",
        "ecommerce": {
            "currency": snapshot.get("currency", "EUR"),
            "value": snapshot["value"],
            "items": items,
        },
    }


def build_ga4_view_item_list(snapshot):
    """
    Convert an item list tracking snapshot from LFS into a GA4 view_item_list event dict.
    """
    if not snapshot or not snapshot.get("line_items"):
        return None

    items = [
        {
            "item_id": line["sku"],
            "item_name": line["name"],
            "price": line["price"],
            "quantity": line["quantity"],
        }
        for line in snapshot.get("line_items", [])
    ]

    return {
        "event": "view_item_list",
        "ecommerce": {
            "item_list_id": snapshot["list_id"],
            "item_list_name": snapshot["list_name"],
            "currency": snapshot.get("currency", "EUR"),
            "value": snapshot["value"],
            "items": items,
        },
    }


def build_ga4_begin_checkout(snapshot):
    """
    Convert a cart tracking snapshot from LFS into a GA4 begin_checkout event dict.
    """
    if not snapshot or not snapshot.get("line_items"):
        return None

    items = [
        {
            "item_id": line["sku"],
            "item_name": line["name"],
            "price": line["price"],
            "quantity": line["quantity"],
        }
        for line in snapshot.get("line_items", [])
    ]

    return {
        "event": "begin_checkout",
        "ecommerce": {
            "currency": snapshot.get("currency", "EUR"),
            "value": snapshot["value"],
            "items": items,
        },
    }


def build_ga4_purchase(snapshot):
    """
    Convert an order tracking snapshot from LFS into a GA4 purchase event dict.
    """
    if not snapshot or not snapshot.get("order_id"):
        return None

    items = [
        {
            "item_id": line["sku"],
            "item_name": line["name"],
            "price": line["price"],
            "quantity": line["quantity"],
        }
        for line in snapshot.get("line_items", [])
    ]

    return {
        "event": "purchase",
        "ecommerce": {
            "transaction_id": snapshot["order_id"],
            "value": snapshot["value"],
            "tax": snapshot["tax"],
            "shipping": snapshot["shipping"],
            "currency": snapshot.get("currency", "EUR"),
            "items": items,
        },
    }
