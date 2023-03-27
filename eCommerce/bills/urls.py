from django.urls import include, path
from django.contrib import admin
from .views import ProductViewSet, OrderViewSet, OrderDetailsViewSet
from bills import views

product_list = ProductViewSet.as_view({
    "get": "list",
    "post": "create"
})

product_detail = ProductViewSet.as_view({
    "get": "retrieve",
    "put": "update",
    "delete": "destroy"
})

order_list = OrderViewSet.as_view({
    "get": "list",
    "post": "create"
})

order_detail = OrderViewSet.as_view({
    "get": "retrieve",
    "delete": "destroy"
})

orderDetail_list = OrderDetailsViewSet.as_view({
    "get": "list",
    "post": "create"
})

orderDetail_detail = OrderDetailsViewSet.as_view({
    "get": "retrieve",
    "delete": "destroy"
})




urlpatterns = [
    path("product/", product_list),
    path("product/<int:pk>", product_detail),
    path("product/mostSell", views.mostSell),
    path("order/", order_list),
    path("order/<int:pk>", order_detail),
    path("orderDetail/", orderDetail_list),
    path("orderDetail/<int:pk>", orderDetail_detail),
]
