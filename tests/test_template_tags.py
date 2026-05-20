import pytest
from django.template import Context, Template
from django.test import override_settings


@pytest.mark.django_db
def test_gtm_script_renders_when_gtm_id_set():
    tpl = Template("{% load lfs_gtm_tags %}{% gtm_script %}")
    with override_settings(GTM_ID="GTM-UNITTEST"):
        html = tpl.render(Context())
    assert "GTM-UNITTEST" in html
    assert "googletagmanager.com/gtm.js" in html
    assert "consent" in html


@pytest.mark.django_db
def test_gtm_script_empty_without_gtm_id():
    tpl = Template("{% load lfs_gtm_tags %}{% gtm_script %}")
    with override_settings(GTM_ID=None):
        html = tpl.render(Context())
    assert html.strip() == ""


@pytest.mark.django_db
def test_added_to_cart_script_renders_from_snapshot():
    tpl = Template("{% load lfs_gtm_tags %}{% added_to_cart_script snapshot %}")
    snapshot = {
        "currency": "EUR",
        "value": 10.0,
        "line_items": [{"sku": "sku-1", "name": "Product 1", "price": 10.0, "quantity": 1}],
    }
    with override_settings(GTM_ID="GTM-UNITTEST"):
        html = tpl.render(Context({"snapshot": snapshot}))
    assert 'id="added-to-cart-event"' in html
    assert "add_to_cart" in html


@pytest.mark.django_db
def test_begin_checkout_script_renders_from_snapshot():
    tpl = Template("{% load lfs_gtm_tags %}{% begin_checkout_script snapshot %}")
    snapshot = {
        "currency": "EUR",
        "value": 10.0,
        "line_items": [{"sku": "sku-1", "name": "Product 1", "price": 10.0, "quantity": 1}],
    }
    with override_settings(GTM_ID="GTM-UNITTEST"):
        html = tpl.render(Context({"snapshot": snapshot}))
    assert 'id="begin-checkout-event"' in html
    assert "begin_checkout" in html


@pytest.mark.django_db
def test_view_item_list_script_renders_from_snapshot():
    tpl = Template("{% load lfs_gtm_tags %}{% view_item_list_script snapshot %}")
    snapshot = {
        "list_id": "category-1",
        "list_name": "Category 1",
        "currency": "EUR",
        "value": 10.0,
        "line_items": [{"sku": "sku-1", "name": "Product 1", "price": 10.0, "quantity": 1}],
    }
    with override_settings(GTM_ID="GTM-UNITTEST"):
        html = tpl.render(Context({"snapshot": snapshot}))
    assert 'id="view-item-list-event"' in html
    assert "view_item_list" in html
    assert "category-1" in html


@pytest.mark.django_db
def test_view_item_script_renders_from_snapshot():
    tpl = Template("{% load lfs_gtm_tags %}{% view_item_script snapshot %}")
    snapshot = {
        "currency": "EUR",
        "value": 10.0,
        "line_items": [{"sku": "sku-1", "name": "Product 1", "price": 10.0, "quantity": 1}],
    }
    with override_settings(GTM_ID="GTM-UNITTEST"):
        html = tpl.render(Context({"snapshot": snapshot}))
    assert 'id="view-item-event"' in html
    assert "view_item" in html


@pytest.mark.django_db
def test_purchase_script_renders_from_snapshot():
    tpl = Template("{% load lfs_gtm_tags %}{% purchase_script snapshot %}")
    snapshot = {
        "order_id": "ORD-1",
        "currency": "EUR",
        "value": 10.0,
        "tax": 1.0,
        "shipping": 1.0,
        "line_items": [{"sku": "s1", "name": "P", "price": 5.0, "quantity": 1}],
    }
    with override_settings(GTM_ID="GTM-UNITTEST"):
        html = tpl.render(Context({"snapshot": snapshot}))
    assert 'id="purchase-event"' in html
    assert "purchase" in html
    assert "ORD-1" in html
