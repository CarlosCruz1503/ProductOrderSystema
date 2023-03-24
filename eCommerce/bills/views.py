from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.http import JsonResponse
from bills.models import Product, Order, OrderDetail
from bills.serializers import ProductSerializer, OrderSerializer, OrderDetailSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


@api_view(["GET"])
def mostSell(request):
    contadorDeOrdenes = 0
    mayor = Product.objects.raw(
        "select id from bills_product order by ordered desc limit 1")
    productTem = Product.objects.filter(name=mayor[0]).order_by("-ordered")[0]
    orderDetail = OrderDetail.objects.all()
    for orderSmall in orderDetail:
        if orderSmall.product_id.id == productTem.id:
            contadorDeOrdenes += 1
    if contadorDeOrdenes >= 2:
        serializer = ProductSerializer(productTem, many=False)
        return Response(serializer.data)

    return Response("No se han hecho las suficientes ventas para estimar el producto mas vendido")


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def retrieve(self, request, pk=None):
        orderDetail = OrderDetail.objects.filter(order_id=pk)
        serializer = OrderDetailSerializer(orderDetail, many=True)
        return Response(serializer.data)

    def create(self, request):
        data = request.data
        order = Order.objects.create(
            date=data["date"],
            client=data["client"],
        )
        order.save()

        dataforSerializers = []

        for productV in data["products"]:
            productTem = Product.objects.get(id=productV["product"])
            productTem.stock = productTem.stock - productV["quantity"]

            if (productTem.stock < 1):
                return Response("No hay suficiente Stock de los productos a comprar", status=404)

        for productV in data["products"]:
            try:
                productTem = Product.objects.get(id=productV["product"])
                productTem.stock = productTem.stock - productV["quantity"]
                productTem.ordered = productTem.ordered + productV["quantity"]
                productTem.save()
            except:
                return Response("El id de algunos de los productos a comprar no existe", status=404)

            orderDetail = OrderDetail.objects.create(
                order_id=order,
                product_id=productTem,
                quantity=productV["quantity"]
            )

            dataforSerializers.append(orderDetail)

        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        orderDetail = OrderDetail.objects.filter(order_id=pk)
        orderBig = Order.objects.get(id=pk)
        for orderSmall in orderDetail:
            productTem = Product.objects.get(id=orderSmall.product_id.id)
            productTem.stock = productTem.stock + orderSmall.quantity
            productTem.ordered = productTem.ordered - orderSmall.quantity
            productTem.save()

        orderDetail.delete()
        orderBig.delete()

        return Response("Orden Eliminada con exito")


class OrderDetailsViewSet(viewsets.ModelViewSet):
    queryset = OrderDetail.objects.all()
    serializer_class = OrderDetailSerializer

    def destroy(self, request, pk=None):
        orderDetail = OrderDetail.objects.get(id=pk)
        productTem = Product.objects.get(id=orderDetail.product_id.id)
        productTem.stock = productTem.stock + orderDetail.quantity
        productTem.ordered = productTem.ordered - orderDetail.quantity
        productTem.save()
        orderDetail.delete()

        return Response("Orden Eliminada con exito")
