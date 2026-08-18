from django.urls import path
from .views import AdHocRecommendBoxView,BoxListView,OrderCreateView,OrderDetailView,OrderRecommendBoxView,ProductListView


urlpatterns = [
    path("products/", ProductListView.as_view(), name="product-list"),
    path("boxes/", BoxListView.as_view(), name="box-list"),
    path("orders/", OrderCreateView.as_view(), name="order-create"),
    path("orders/<int:pk>/", OrderDetailView.as_view(), name="order-detail"),
    path("orders/<int:pk>/recommend-box/",OrderRecommendBoxView.as_view(),name="order-recommend-box",),
    path("recommend-box/",AdHocRecommendBoxView.as_view(),name="recommend-box",),
]