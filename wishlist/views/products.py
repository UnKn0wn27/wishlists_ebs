import datetime
import calendar

from django.http.response import Http404
from rest_framework import decorators, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from wishlist.tools import get_date_range
from wishlist.tools import find_weeks
from wishlist.models import Products, PriceHistory, List
from wishlist.serializer import (
    ProductForMagazin, ProductForWishlist, ProductDetailSerializer, PriceSerializer,
    PriceCategory, AveragePrice
)


@decorators.api_view(['POST'])
@decorators.permission_classes([permissions.IsAuthenticated])
def add_to_product(request):
    serializer = ProductForMagazin(data=request.data)
    if serializer.is_valid():
        product = Products.objects.create(name=serializer.data['name'])
        product.list.add(serializer.data['magazin_id'], serializer.data['category_id'])
        from_date = serializer.data['from_date'] if serializer.data.get('from_date') else datetime.date.today()
        PriceHistory.objects.create(product=product, price=serializer.data['price'], from_date=from_date)

        return Response(serializer.data, status=200)
    return Response(serializer.errors, status=400)


@decorators.api_view(['POST'])
@decorators.permission_classes([permissions.IsAuthenticated])
def add_to_wishlist(request):
    serializer = ProductForWishlist(data=request.data)
    if serializer.is_valid():
        product = Products.objects.get(id=serializer.data['product_id'])
        product.list.add(serializer.data['wishlist_id'])
        product.count_wished_product()

        return Response(serializer.data, status=200)
    return Response(serializer.errors, status=400)


@decorators.api_view(['POST'])
@decorators.permission_classes([permissions.IsAuthenticated])
def change_price_category(request):
    serializer = PriceCategory(data=request.data)

    if serializer.is_valid():
        try:
            category = List.objects.get(
                id=serializer.data['category_id'],
                type=List.CATEGORY
            )
        except:
            raise Http404

        products = category.products.all().values_list('id', flat=True)

        PriceHistory.objects.bulk_create([
            PriceHistory(product_id=i, price=serializer.data['price'], from_date=datetime.date.today())
            for i in products])

        return Response(request.data, status=200)
    return Response(request.errors, status=400)


@decorators.api_view(['POST'])
@decorators.permission_classes([permissions.IsAuthenticated])
def get_average_price(request):
    serializer = AveragePrice(data=request.data)
    response = []
    if serializer.is_valid():
        try:
            product = Products.objects.get(id=serializer.data['product_id'])
        except:
            raise Http404

        price_history = list(PriceHistory.objects.filter(
            product_id=product.id,
            from_date__gte=serializer.data['from_date'],
            from_date__lte=serializer.data['to_date']
        ).order_by('from_date').values('price', 'from_date'))

        price_history_dict = {i['from_date']: i['price'] for i in price_history}

        if serializer.data['sum_for'] == 'MONTHS':
            date_range = get_date_range(price_history[0]['from_date'], price_history[-1]['from_date'])
            date_range = [i for i in date_range]
            months = {}
            price = None
            for date in date_range:
                if not months.get(date.month):
                    months[date.month] = {
                        'year': date.year,
                        'prices': []
                    }
                if price_history_dict.get(date):
                    price = price_history_dict[date]
                if price is not None:
                    months[date.month]['prices'].append(price)
            response = [{
                'month': calendar.month_name[k],
                'year': i['year'],
                'price': sum(i['prices']) / len(i['prices'])
            } for k, i in months.items()]

        elif serializer.data['sum_for'] == 'DAYS':
            week_range = find_weeks(price_history[0]['from_date'], price_history[-1]['from_date'])

            weeks = {}
            price = None
            for w in week_range:
                if not weeks.get(w['week']):
                    weeks[w['week']] = {
                        'week_day': w['week_day'],
                        'prices': []
                    }
                if price_history_dict.get(w['week_day']):
                    price = price_history_dict[w['week_day']]
                if price is not None:
                    weeks[w['week']]['prices'].append(price)

            response = [{
                'week': k,
                'week_day': i['week_day'],
                'price': sum(i['prices']) / len(i['prices'])
            } for k, i in weeks.items()]

        return Response(response, status=200)
    return Response(serializer.errors, status=400)


class ProductPriceDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Products.objects.get(pk=pk)
        except Products.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        product = self.get_object(pk).__dict__
        if request.GET.get('date'):
            product['date'] = request.GET['date']
        serliallizer = ProductDetailSerializer(product)
        return Response(serliallizer.data)

    def post(self, request, pk):
        self.get_object(pk)
        serializer = PriceSerializer(data=request.data)
        if serializer.is_valid():
            PriceHistory.objects.create(
                price=serializer.data['price'],
                from_date=serializer.data['date'],
                product_id=pk
            )
            return Response(status=200)
        return Response(serializer.errors, status=400)


class PriceDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return PriceHistory.objects.get(pk=pk)
        except Products.DoesNotExist:
            raise Http404

    def put(self, request, pk):
        self.get_object(pk)
        serializer = PriceSerializer(data=request.data)
        if serializer.is_valid():
            PriceHistory.objects.filter(id=pk).update(
                price=serializer.data['price'],
                from_date=serializer.data['date']
            )
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        self.get_object(pk).delete()
        return Response(status=204)
