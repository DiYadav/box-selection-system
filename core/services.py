from dataclasses import dataclass
from decimal import Decimal
from itertools import permutations


PACKING_EFFICIENCY = Decimal("0.80")


@dataclass(frozen=True)
class PackItem:
    dimensions: tuple[Decimal, Decimal, Decimal]
    weight: Decimal
    label: str


@dataclass(frozen=True)
class Recommendation:
    box: object
    total_weight: Decimal
    total_volume: Decimal
    box_volume: Decimal
    weight_utilization_pct: Decimal
    volume_utilization_pct: Decimal
    candidates_considered: int


class NoSuitableBoxError(Exception):
    """Raised when no candidate box can safely contain all items."""
    def __init__(self, reasons):
        self.reasons = reasons
        message = "No suitable box found. " + " | ".join(reasons)
        super().__init__(message)


def dimensions_fit(item_dimensions, box_dimensions):
    """Return True if the item fits in the box in any axis-aligned rotation."""
    for permutation in permutations(item_dimensions):
        if all(item_side <= box_side for item_side, box_side in zip(permutation, box_dimensions)):
            return True
    return False


def _item_volume(dimensions):
    length, width, height = dimensions
    return length * width * height


def recommend_box(items, boxes):
    items = list(items)
    boxes = list(boxes)
    if not items:
        raise ValueError("At least one item is required.")
    total_weight = sum((item.weight for item in items),Decimal("0"),)
    total_volume = sum((_item_volume(item.dimensions) for item in items),Decimal("0"),)
    rejection_reasons = []
    feasible_boxes = []
    for box in boxes:
        reasons = []
        if total_weight > box.max_weight_kg:
            reasons.append(f"total weight {total_weight} kg exceeds "f"maximum {box.max_weight_kg} kg" )
        for item in items:
            if not dimensions_fit(item.dimensions,box.internal_dimensions,):
                reasons.append(
                    f"item '{item.label}' with dimensions "
                    f"{item.dimensions} does not fit inside box "
                    f"dimensions {box.internal_dimensions} in any rotation"
                )
                break
        usable_volume = (box.internal_volume_cm3 * PACKING_EFFICIENCY)
        if total_volume > usable_volume:
            reasons.append(f"total item volume {total_volume} cm3 exceeds "f"usable volume {usable_volume} cm3")
        if reasons:
            rejection_reasons.append(f"{box.code}: " + "; ".join(reasons))
            continue
        feasible_boxes.append(box)
    if not feasible_boxes:
        raise NoSuitableBoxError(rejection_reasons)
    winner = min(feasible_boxes,key=lambda box: (box.cost,box.internal_volume_cm3,),)
    weight_utilization = (total_weight / winner.max_weight_kg) * Decimal("100")
    volume_utilization = (total_volume / winner.internal_volume_cm3) * Decimal("100")
    return Recommendation(
        box=winner,
        total_weight=total_weight,
        total_volume=total_volume,
        box_volume=winner.internal_volume_cm3,
        weight_utilization_pct=weight_utilization,
        volume_utilization_pct=volume_utilization,
        candidates_considered=len(boxes),
    )


def expand_order_items(order):
    """Convert OrderItems with quantities into individual PackItems."""
    items = []
    for order_item in order.items.select_related("product").all():
        product = order_item.product
        for _ in range(order_item.quantity):
            items.append(
                PackItem(
                    dimensions=product.dimensions,
                    weight=product.weight_kg,
                    label=product.name,
                )
            )
    return items