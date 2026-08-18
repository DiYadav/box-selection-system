from decimal import Decimal
import pytest
from rest_framework.test import APIClient
from core.models import Box, Order, Product


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_product_list(api_client):
    Product.objects.create(
        name="Product A",
        length_cm=Decimal("10"),
        width_cm=Decimal("10"),
        height_cm=Decimal("10"),
        weight_kg=Decimal("1"),
    )
    response = api_client.get("/api/products/")
    assert response.status_code == 200
    assert len(response.data) == 1


@pytest.mark.django_db
def test_box_list(api_client):
    Box.objects.create(
        code="BOX-S",
        name="Small Box",
        internal_length_cm=Decimal("10"),
        internal_width_cm=Decimal("10"),
        internal_height_cm=Decimal("10"),
        max_weight_kg=Decimal("5"),
        cost=Decimal("4"),
    )
    response = api_client.get("/api/boxes/")
    assert response.status_code == 200
    assert len(response.data) == 1


@pytest.mark.django_db
def test_create_order_returns_recommendation_and_persists_it(api_client):
    product = Product.objects.create(
        name="Product A",
        length_cm=Decimal("8"),
        width_cm=Decimal("8"),
        height_cm=Decimal("8"),
        weight_kg=Decimal("1"),
    )
    box = Box.objects.create(
        code="BOX-S",
        name="Small Box",
        internal_length_cm=Decimal("10"),
        internal_width_cm=Decimal("10"),
        internal_height_cm=Decimal("10"),
        max_weight_kg=Decimal("5"),
        cost=Decimal("4"),
    )
    response = api_client.post(
        "/api/orders/",
        {
            "items": [
                {
                    "product_id": product.id,
                    "quantity": 1,
                }
            ]
        },
        format="json",
    )
    assert response.status_code == 201
    assert response.data["recommended_box"]["id"] == box.id
    order_id = response.data["order"]["id"]
    order = Order.objects.get(id=order_id)
    assert order.recommended_box == box


@pytest.mark.django_db
def test_create_order_rejects_empty_items(api_client):
    response = api_client.post(
        "/api/orders/",
        {"items": []},
        format="json",
    )
    assert response.status_code == 400


@pytest.mark.django_db
def test_create_order_rejects_unknown_product(api_client):
    response = api_client.post(
        "/api/orders/",
        {
            "items": [
                {
                    "product_id": 99999,
                    "quantity": 1,
                }
            ]
        },
        format="json",
    )
    assert response.status_code == 400


@pytest.mark.django_db
def test_create_order_without_feasible_box_still_creates_order(api_client):
    product = Product.objects.create(
        name="Heavy Product",
        length_cm=Decimal("5"),
        width_cm=Decimal("5"),
        height_cm=Decimal("5"),
        weight_kg=Decimal("20"),
    )
    Box.objects.create(
        code="BOX-S",
        name="Small Box",
        internal_length_cm=Decimal("10"),
        internal_width_cm=Decimal("10"),
        internal_height_cm=Decimal("10"),
        max_weight_kg=Decimal("5"),
        cost=Decimal("4"),
    )
    response = api_client.post(
        "/api/orders/",
        {
            "items": [
                {
                    "product_id": product.id,
                    "quantity": 1,
                }
            ]
        },
        format="json",
    )
    assert response.status_code == 201
    assert response.data["recommended_box"] is None
    assert "error" in response.data
    assert Order.objects.count() == 1


@pytest.mark.django_db
def test_stateless_recommendation_does_not_create_order(api_client):
    product = Product.objects.create(
        name="Product A",
        length_cm=Decimal("8"),
        width_cm=Decimal("8"),
        height_cm=Decimal("8"),
        weight_kg=Decimal("1"),
    )
    box = Box.objects.create(
        code="BOX-S",
        name="Small Box",
        internal_length_cm=Decimal("10"),
        internal_width_cm=Decimal("10"),
        internal_height_cm=Decimal("10"),
        max_weight_kg=Decimal("5"),
        cost=Decimal("4"),
    )
    response = api_client.post(
        "/api/recommend-box/",
        {
            "items": [
                {
                    "product_id": product.id,
                    "quantity": 1,
                }
            ]
        },
        format="json",
    )
    assert response.status_code == 200
    assert response.data["recommended_box"]["id"] == box.id
    assert Order.objects.count() == 0


@pytest.mark.django_db
def test_existing_order_recommend_box(api_client):
    product = Product.objects.create(
        name="Product A",
        length_cm=Decimal("8"),
        width_cm=Decimal("8"),
        height_cm=Decimal("8"),
        weight_kg=Decimal("1"),
    )
    box = Box.objects.create(
        code="BOX-S",
        name="Small Box",
        internal_length_cm=Decimal("10"),
        internal_width_cm=Decimal("10"),
        internal_height_cm=Decimal("10"),
        max_weight_kg=Decimal("5"),
        cost=Decimal("4"),
    )
    response = api_client.post(
        "/api/orders/",
        {
            "items": [
                {
                    "product_id": product.id,
                    "quantity": 1,
                }
            ]
        },
        format="json",
    )
    order_id = response.data["order"]["id"]
    response = api_client.get(f"/api/orders/{order_id}/recommend-box/")
    assert response.status_code == 200
    assert response.data["recommended_box"]["id"] == box.id


@pytest.mark.django_db
def test_recommend_box_missing_order_returns_404(api_client):
    response = api_client.get("/api/orders/99999/recommend-box/")
    assert response.status_code == 404