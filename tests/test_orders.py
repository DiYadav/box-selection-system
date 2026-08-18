from decimal import Decimal
import pytest
from core.models import Box, Order, OrderItem, Product
from core.services import expand_order_items, recommend_box
from core.services import NoSuitableBoxError,expand_order_items,recommend_box



@pytest.mark.django_db
def test_order_items_are_expanded_by_quantity():
    product = Product.objects.create(
        name="Test Product",
        length_cm=Decimal("10"),
        width_cm=Decimal("10"),
        height_cm=Decimal("10"),
        weight_kg=Decimal("2"),
    )
    order = Order.objects.create()
    OrderItem.objects.create(order=order,product=product,quantity=3,)
    items = expand_order_items(order)
    assert len(items) == 3
    assert all(                              
        item.dimensions == (
            Decimal("10"),
            Decimal("10"),
            Decimal("10"),
        )
        for item in items
    )
    assert all(                                      
        item.weight == Decimal("2")
        for item in items
    )


@pytest.mark.django_db
def test_multiple_order_items_are_expanded_correctly():
    product_a = Product.objects.create(
        name="Product A",
        length_cm=Decimal("10"),
        width_cm=Decimal("10"),
        height_cm=Decimal("10"),
        weight_kg=Decimal("2"),
    )
    product_b = Product.objects.create(
        name="Product B",
        length_cm=Decimal("5"),
        width_cm=Decimal("5"),
        height_cm=Decimal("5"),
        weight_kg=Decimal("1"),
    )
    order = Order.objects.create()
    OrderItem.objects.create(
        order=order,
        product=product_a,
        quantity=2,
    )
    OrderItem.objects.create(
        order=order,
        product=product_b,
        quantity=1,
    )
    items = expand_order_items(order)
    assert len(items) == 3
    total_weight = sum(item.weight for item in items)  
    assert total_weight == Decimal("5")
    total_volume = sum(                  
        item.dimensions[0]
        * item.dimensions[1]
        * item.dimensions[2]
        for item in items
    )
    assert total_volume == Decimal("2125")


@pytest.mark.django_db
def test_order_flow_selects_cheapest_feasible_box():
    product = Product.objects.create(
        name="Small Product",
        length_cm=Decimal("8"),
        width_cm=Decimal("8"),
        height_cm=Decimal("8"),
        weight_kg=Decimal("1"),
    )
    small_box = Box.objects.create(
        code="BOX-S",
        name="Small Box",
        internal_length_cm=Decimal("10"),
        internal_width_cm=Decimal("10"),
        internal_height_cm=Decimal("10"),
        max_weight_kg=Decimal("5"),
        cost=Decimal("4"),
    )
    large_box = Box.objects.create(
        code="BOX-L",
        name="Large Box",
        internal_length_cm=Decimal("20"),
        internal_width_cm=Decimal("20"),
        internal_height_cm=Decimal("20"),
        max_weight_kg=Decimal("10"),
        cost=Decimal("8"),
    )
    order = Order.objects.create()
    OrderItem.objects.create(order=order,product=product,quantity=1,)
    items = expand_order_items(order)
    recommendation = recommend_box(items,Box.objects.all(),)
    assert recommendation.box == small_box


@pytest.mark.django_db
def test_quantity_can_force_larger_box():
    product = Product.objects.create(
        name="Heavy Product",
        length_cm=Decimal("5"),
        width_cm=Decimal("5"),
        height_cm=Decimal("5"),
        weight_kg=Decimal("2"),
    )
    small_box = Box.objects.create(
        code="BOX-S",
        name="Small Box",
        internal_length_cm=Decimal("10"),
        internal_width_cm=Decimal("10"),
        internal_height_cm=Decimal("10"),
        max_weight_kg=Decimal("5"),
        cost=Decimal("4"),
    )

    large_box = Box.objects.create(
        code="BOX-L",
        name="Large Box",
        internal_length_cm=Decimal("20"),
        internal_width_cm=Decimal("20"),
        internal_height_cm=Decimal("20"),
        max_weight_kg=Decimal("10"),
        cost=Decimal("8"),
    )
    order = Order.objects.create()
    OrderItem.objects.create(order=order,product=product,quantity=3,)
    items = expand_order_items(order)
    recommendation = recommend_box(items,Box.objects.all(),)
    assert len(items) == 3
    assert recommendation.box == large_box


@pytest.mark.django_db
def test_order_flow_raises_when_no_box_is_feasible():
    product = Product.objects.create(
        name="Very Heavy Product",
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
    order = Order.objects.create()
    OrderItem.objects.create(order=order,product=product,quantity=1,)
    items = expand_order_items(order)
    with pytest.raises(NoSuitableBoxError):
        recommend_box(items,Box.objects.all(),)


@pytest.mark.django_db
def test_order_flow_accepts_rotated_product():
    product = Product.objects.create(
        name="Rotated Product",
        length_cm=Decimal("30"),
        width_cm=Decimal("20"),
        height_cm=Decimal("10"),
        weight_kg=Decimal("2"),
    )
    box = Box.objects.create(
        code="BOX-R",
        name="Rotated Box",
        internal_length_cm=Decimal("10"),
        internal_width_cm=Decimal("30"),
        internal_height_cm=Decimal("30"),
        max_weight_kg=Decimal("10"),
        cost=Decimal("5"),
    )
    order = Order.objects.create()
    OrderItem.objects.create(order=order,product=product,quantity=1,)
    items = expand_order_items(order)
    recommendation = recommend_box(items,Box.objects.all(),)
    assert recommendation.box == box


@pytest.mark.django_db
def test_order_flow_combined_volume_requires_larger_box():
    product = Product.objects.create(
        name="Volume Product",
        length_cm=Decimal("9"),
        width_cm=Decimal("9"),
        height_cm=Decimal("6"),
        weight_kg=Decimal("1"),
    )
    small_box = Box.objects.create(
        code="BOX-S",
        name="Small Box",
        internal_length_cm=Decimal("10"),
        internal_width_cm=Decimal("10"),
        internal_height_cm=Decimal("10"),
        max_weight_kg=Decimal("10"),
        cost=Decimal("4"),
    )
    large_box = Box.objects.create(
        code="BOX-L",
        name="Large Box",
        internal_length_cm=Decimal("20"),
        internal_width_cm=Decimal("20"),
        internal_height_cm=Decimal("20"),
        max_weight_kg=Decimal("10"),
        cost=Decimal("8"),
    )
    order = Order.objects.create()
    OrderItem.objects.create(order=order,product=product,quantity=2,)
    items = expand_order_items(order)
    recommendation = recommend_box(items,Box.objects.all(),)
    assert recommendation.box == large_box