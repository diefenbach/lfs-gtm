from lfs_gtm.ga4_events import (
    build_ga4_add_to_cart,
    build_ga4_begin_checkout,
    build_ga4_purchase,
    build_ga4_view_item,
    build_ga4_view_item_list,
)


def test_build_ga4_add_to_cart_maps_snapshot():
    snapshot = {
        "currency": "EUR",
        "value": 22.0,
        "line_items": [
            {"sku": "sku-1", "name": "Product 1", "price": 11.0, "quantity": 2},
        ],
    }
    event = build_ga4_add_to_cart(snapshot)

    assert event["event"] == "add_to_cart"
    assert event["ecommerce"]["currency"] == "EUR"
    assert event["ecommerce"]["value"] == 22.0
    assert len(event["ecommerce"]["items"]) == 1
    assert event["ecommerce"]["items"][0]["item_id"] == "sku-1"
    assert event["ecommerce"]["items"][0]["item_name"] == "Product 1"
    assert event["ecommerce"]["items"][0]["price"] == 11.0
    assert event["ecommerce"]["items"][0]["quantity"] == 2


def test_build_ga4_view_item_list_maps_snapshot():
    snapshot = {
        "list_id": "category-1",
        "list_name": "Category 1",
        "currency": "EUR",
        "value": 30.0,
        "line_items": [
            {"sku": "sku-1", "name": "Product 1", "price": 10.0, "quantity": 1},
            {"sku": "sku-2", "name": "Product 2", "price": 20.0, "quantity": 1},
        ],
    }
    event = build_ga4_view_item_list(snapshot)

    assert event["event"] == "view_item_list"
    assert event["ecommerce"]["item_list_id"] == "category-1"
    assert event["ecommerce"]["item_list_name"] == "Category 1"
    assert event["ecommerce"]["value"] == 30.0
    assert len(event["ecommerce"]["items"]) == 2
    assert event["ecommerce"]["items"][0]["item_id"] == "sku-1"


def test_build_ga4_view_item_list_returns_none_for_empty_snapshot():
    assert build_ga4_view_item_list(None) is None
    assert build_ga4_view_item_list({"list_id": "x", "list_name": "y", "line_items": []}) is None


def test_build_ga4_begin_checkout_maps_snapshot():
    snapshot = {
        "currency": "EUR",
        "value": 22.0,
        "line_items": [
            {"sku": "sku-1", "name": "Product 1", "price": 11.0, "quantity": 2},
        ],
    }
    event = build_ga4_begin_checkout(snapshot)

    assert event["event"] == "begin_checkout"
    assert event["ecommerce"]["currency"] == "EUR"
    assert event["ecommerce"]["value"] == 22.0
    assert len(event["ecommerce"]["items"]) == 1
    assert event["ecommerce"]["items"][0]["item_id"] == "sku-1"


def test_build_ga4_begin_checkout_returns_none_for_empty_snapshot():
    assert build_ga4_begin_checkout(None) is None
    assert build_ga4_begin_checkout({"currency": "EUR", "value": 0, "line_items": []}) is None


def test_build_ga4_add_to_cart_returns_none_for_empty_snapshot():
    assert build_ga4_add_to_cart(None) is None
    assert build_ga4_add_to_cart({"currency": "EUR", "value": 0, "line_items": []}) is None


def test_build_ga4_purchase_maps_snapshot():
    snapshot = {
        "order_id": "ORD-42",
        "currency": "EUR",
        "value": 9.8,
        "tax": 1.56,
        "shipping": 1.0,
        "line_items": [
            {"sku": "sku-1", "name": "Product 1", "price": 1.1, "quantity": 2},
        ],
    }
    event = build_ga4_purchase(snapshot)

    assert event["event"] == "purchase"
    assert event["ecommerce"]["transaction_id"] == "ORD-42"
    assert event["ecommerce"]["value"] == 9.8
    assert event["ecommerce"]["tax"] == 1.56
    assert event["ecommerce"]["shipping"] == 1.0
    assert event["ecommerce"]["currency"] == "EUR"
    assert len(event["ecommerce"]["items"]) == 1
    assert event["ecommerce"]["items"][0]["item_id"] == "sku-1"
    assert event["ecommerce"]["items"][0]["item_name"] == "Product 1"
    assert event["ecommerce"]["items"][0]["price"] == 1.1
    assert event["ecommerce"]["items"][0]["quantity"] == 2


def test_build_ga4_purchase_returns_none_for_empty_snapshot():
    assert build_ga4_purchase(None) is None
    assert build_ga4_purchase({}) is None


def test_build_ga4_view_item_maps_snapshot():
    snapshot = {
        "currency": "EUR",
        "value": 11.0,
        "line_items": [
            {"sku": "sku-1", "name": "Product 1", "price": 11.0, "quantity": 1},
        ],
    }
    event = build_ga4_view_item(snapshot)

    assert event["event"] == "view_item"
    assert event["ecommerce"]["currency"] == "EUR"
    assert event["ecommerce"]["value"] == 11.0
    assert len(event["ecommerce"]["items"]) == 1
    assert event["ecommerce"]["items"][0]["item_id"] == "sku-1"
    assert event["ecommerce"]["items"][0]["item_name"] == "Product 1"
    assert event["ecommerce"]["items"][0]["price"] == 11.0
    assert event["ecommerce"]["items"][0]["quantity"] == 1


def test_build_ga4_view_item_returns_none_for_empty_snapshot():
    assert build_ga4_view_item(None) is None
    assert build_ga4_view_item({"currency": "EUR", "value": 0, "line_items": []}) is None
