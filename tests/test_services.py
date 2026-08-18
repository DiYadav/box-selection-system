from decimal import Decimal
from core.services import dimensions_fit
from dataclasses import dataclass
from decimal import Decimal
import pytest
from core.services import PACKING_EFFICIENCY,NoSuitableBoxError,PackItem,dimensions_fit,recommend_box


def test_smaller_item_fits():
    assert dimensions_fit(
        (Decimal("5"), Decimal("5"), Decimal("5")),
        (Decimal("10"), Decimal("10"), Decimal("10")),
    ) is True


def test_item_exactly_equal_to_box_fits():
    assert dimensions_fit(
        (Decimal("10"), Decimal("10"), Decimal("10")),
        (Decimal("10"), Decimal("10"), Decimal("10")),
    ) is True


def test_item_bigger_than_box_does_not_fit():
    assert dimensions_fit(
        (Decimal("20"), Decimal("20"), Decimal("20")),
        (Decimal("10"), Decimal("10"), Decimal("10")),
    ) is False


def test_item_fits_after_rotation():
    assert dimensions_fit(
        (Decimal("30"), Decimal("20"), Decimal("10")),
        (Decimal("10"), Decimal("30"), Decimal("20")),
    ) is True


def test_item_does_not_fit_in_any_rotation():
    assert dimensions_fit(
        (Decimal("31"), Decimal("30"), Decimal("20")),
        (Decimal("10"), Decimal("30"), Decimal("20")),
    ) is False


@dataclass
class FakeBox:
    code: str
    name: str
    internal_dimensions: tuple
    max_weight_kg: Decimal
    cost: Decimal

    @property
    def internal_volume_cm3(self):
        length, width, height = self.internal_dimensions
        return length * width * height


@pytest.fixture
def boxes():
    return [
        FakeBox(
            code="BOX-XS",
            name="Extra Small",
            internal_dimensions=(
                Decimal("10"),
                Decimal("10"),
                Decimal("10"),
            ),
            max_weight_kg=Decimal("2"),
            cost=Decimal("2.00"),
        ),
        FakeBox(
            code="BOX-S",
            name="Small",
            internal_dimensions=(
                Decimal("20"),
                Decimal("20"),
                Decimal("20"),
            ),
            max_weight_kg=Decimal("5"),
            cost=Decimal("4.00"),
        ),
        FakeBox(
            code="BOX-M",
            name="Medium",
            internal_dimensions=(
                Decimal("30"),
                Decimal("30"),
                Decimal("30"),
            ),
            max_weight_kg=Decimal("10"),
            cost=Decimal("7.00"),
        ),
        FakeBox(
            code="BOX-L",
            name="Large",
            internal_dimensions=(
                Decimal("50"),
                Decimal("50"),
                Decimal("50"),
            ),
            max_weight_kg=Decimal("20"),
            cost=Decimal("10.00"),
        ),
    ]


def test_cheapest_feasible_box_wins(boxes):
    item = PackItem(
        dimensions=(
            Decimal("8"),
            Decimal("8"),
            Decimal("8"),
        ),
        weight=Decimal("1"),
        label="Small Item",
    )
    result = recommend_box([item], boxes)
    assert result.box.code == "BOX-XS"


def test_heavy_item_bumps_to_next_box(boxes):
    item = PackItem(
        dimensions=(
            Decimal("8"),
            Decimal("8"),
            Decimal("8"),
        ),
        weight=Decimal("3"),
        label="Heavy Item",
    )
    result = recommend_box([item], boxes)
    assert result.box.code == "BOX-S"


def test_weight_exceeding_every_box_raises_error(boxes):
    item = PackItem(
        dimensions=(
            Decimal("8"),
            Decimal("8"),
            Decimal("8"),
        ),
        weight=Decimal("25"),
        label="Very Heavy Item",
    )
    with pytest.raises(NoSuitableBoxError) as exc_info:
        recommend_box([item], boxes)
    assert "BOX-XS" in str(exc_info.value)
    assert "BOX-S" in str(exc_info.value)
    assert "BOX-M" in str(exc_info.value)
    assert "BOX-L" in str(exc_info.value)


def test_item_too_large_for_every_box_raises_error(boxes):
    item = PackItem(
        dimensions=(
            Decimal("60"),
            Decimal("10"),
            Decimal("10"),
        ),
        weight=Decimal("1"),
        label="Long Item",
    )
    with pytest.raises(NoSuitableBoxError) as exc_info:
        recommend_box([item], boxes)
    assert "Long Item" in str(exc_info.value)


def test_rotated_item_is_accepted():
    box = FakeBox(
        code="BOX-R",
        name="Rotated Box",
        internal_dimensions=(
            Decimal("10"),
            Decimal("30"),
            Decimal("30"),
        ),
        max_weight_kg=Decimal("10"),
        cost=Decimal("5"),
    )
    item = PackItem(
        dimensions=(
            Decimal("30"),
            Decimal("20"),
            Decimal("10"),
        ),
        weight=Decimal("2"),
        label="Rotatable Item",
    )
    result = recommend_box([item], [box])
    assert result.box.code == "BOX-R"


def test_combined_volume_bumps_to_bigger_box():
    small_box = FakeBox(
        code="BOX-S",
        name="Small",
        internal_dimensions=(
            Decimal("9"),
            Decimal("9"),
            Decimal("6"),
        ),
        max_weight_kg=Decimal("10"),
        cost=Decimal("4"),
    )
    large_box = FakeBox(
        code="BOX-L",
        name="Large",
        internal_dimensions=(
            Decimal("20"),
            Decimal("20"),
            Decimal("20"),
        ),
        max_weight_kg=Decimal("10"),
        cost=Decimal("8"),
    )
    items = [
        PackItem(
            dimensions=(
                Decimal("8"),
                Decimal("8"),
                Decimal("5"),
            ),
            weight=Decimal("1"),
            label="Item A",
        ),
        PackItem(
            dimensions=(
                Decimal("8"),
                Decimal("8"),
                Decimal("5"),
            ),
            weight=Decimal("1"),
            label="Item B",
        ),
    ]
    result = recommend_box(
        items,
        [small_box, large_box],
    )
    assert result.box.code == "BOX-L"


def test_equal_cost_prefers_smaller_volume():
    large_volume = FakeBox(
        code="BOX-A",
        name="Large Volume",
        internal_dimensions=(
            Decimal("20"),
            Decimal("20"),
            Decimal("20"),
        ),
        max_weight_kg=Decimal("10"),
        cost=Decimal("5"),
    )

    small_volume = FakeBox(
        code="BOX-B",
        name="Small Volume",
        internal_dimensions=(
            Decimal("15"),
            Decimal("15"),
            Decimal("15"),
        ),
        max_weight_kg=Decimal("10"),
        cost=Decimal("5"),
    )
    item = PackItem(
        dimensions=(
            Decimal("10"),
            Decimal("10"),
            Decimal("10"),
        ),
        weight=Decimal("2"),label="Item",)
    result = recommend_box([item],[large_volume, small_volume],)
    assert result.box.code == "BOX-B"


def test_empty_items_raise_error(boxes):
    with pytest.raises(ValueError, match="At least one item is required"):
        recommend_box([], boxes)


def test_utilization_percentages_are_correct():
    box = FakeBox(
        code="BOX-U",
        name="Utilization Box",
        internal_dimensions=(
            Decimal("10"),
            Decimal("10"),
            Decimal("10"),
        ),
        max_weight_kg=Decimal("10"),
        cost=Decimal("5"),
    )
    item = PackItem(
        dimensions=(
            Decimal("5"),
            Decimal("5"),
            Decimal("4"),
        ),
        weight=Decimal("2"),
        label="Utilization Item",
    )
    result = recommend_box([item], [box])
    assert result.total_weight == Decimal("2")
    assert result.total_volume == Decimal("100")
    assert result.box_volume == Decimal("1000")
    assert result.weight_utilization_pct == Decimal("20")
    assert result.volume_utilization_pct == Decimal("10")