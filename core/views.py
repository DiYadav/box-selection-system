from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Box, Order, Product
from .serializers import AdHocRecommendRequestSerializer,BoxSerializer,OrderCreateSerializer,OrderSerializer,ProductSerializer 
from .services import NoSuitableBoxError,PackItem,expand_order_items,recommend_box


def _recommendation_payload(recommendation):
    """Shared JSON shape for a successful recommendation, used by both the
    order-based and ad-hoc endpoints so API consumers get a consistent
    response either way.
    """
    return {
        "recommended_box": BoxSerializer(recommendation.box).data,
        "total_weight_kg": recommendation.total_weight,
        "total_item_volume_cm3": recommendation.total_volume,
        "box_internal_volume_cm3": recommendation.box_volume,
        "weight_utilization_pct": recommendation.weight_utilization_pct,
        "volume_utilization_pct": recommendation.volume_utilization_pct,
        "boxes_considered": recommendation.candidates_considered,
    }


class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class BoxListView(ListAPIView):
    queryset = Box.objects.all()
    serializer_class = BoxSerializer


class OrderCreateView(APIView):
    def post(self, request):
        serializer = OrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        items = expand_order_items(order)
        try:
            recommendation = recommend_box(items, Box.objects.all())
        except NoSuitableBoxError as exc:
            return Response(
                {
                    "order": OrderSerializer(order).data,
                    "recommended_box": None,
                    "error": str(exc),
                },
                status=status.HTTP_201_CREATED,
            )
        order.recommended_box = recommendation.box
        order.save(update_fields=["recommended_box"])
        response_data = {"order": OrderSerializer(order).data}
        response_data.update(_recommendation_payload(recommendation))
        return Response(response_data, status=status.HTTP_201_CREATED)


class OrderDetailView(RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderRecommendBoxView(APIView):
    """Recomputes (and re-caches) the box recommendation for an existing
    order. Useful if the box catalogue changed since the order was placed."""
    def get(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)
        items = expand_order_items(order)
        try:
            recommendation = recommend_box(items, Box.objects.all())
        except NoSuitableBoxError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        order.recommended_box = recommendation.box
        order.save(update_fields=["recommended_box"])
        return Response(_recommendation_payload(recommendation), status=status.HTTP_200_OK)


class AdHocRecommendBoxView(APIView):
    """
    Body: {"items": [{"product_id": 1, "quantity": 2}, ...]}
    Stateless equivalent of the order flow - useful for a "what box would I
    need" preview before an order is actually placed, e.g. from a cart page.
    """
    def post(self, request):
        serializer = AdHocRecommendRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        items = []
        for entry in serializer.validated_data["items"]:
            product = entry["product"]
            quantity = entry["quantity"]
            for _ in range(quantity):
                items.append(
                    PackItem(
                        dimensions=product.dimensions,
                        weight=product.weight_kg,
                        label=product.name,
                    )
                )
        try:
            recommendation = recommend_box(items, Box.objects.all())
        except NoSuitableBoxError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        return Response(_recommendation_payload(recommendation), status=status.HTTP_200_OK)
