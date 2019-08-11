import datetime

from django.contrib.auth.models import User
from rest_framework import serializers

from .models import List, Products, PriceHistory


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = ['id', 'name', 'type']

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        user = self.context['request'].user
        instance.__setattr__('user_id', user.id)
        instance.save()
        return instance


class ProductForMagazin(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    magazin_id = serializers.IntegerField()
    category_id = serializers.IntegerField()
    price = serializers.IntegerField()
    from_date = serializers.DateField(required=False)


class ProductForWishlist(serializers.Serializer):
    product_id = serializers.IntegerField()
    wishlist_id = serializers.IntegerField()


class ProductDetailSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField(read_only=True)
    date = serializers.DateField(required=False)

    class Meta:
        model = Products
        fields = ['id', 'name', 'price', 'date']

    def get_price(self, validated_data):
        if validated_data.get('date'):
            price = PriceHistory.objects.filter(
                product_id=validated_data['id'],
                from_date=validated_data['date']
            ).first()
            if not price:
                date = validated_data['date']
                prices = PriceHistory.objects.filter(product_id=validated_data['id']).order_by('from_date')
                if prices.filter(from_date__gte=date):
                    price = prices.filter(from_date__lte=date).first()
                else:
                    price = prices.last()

                if price:
                    return price.price
        else:
            price = PriceHistory.objects.filter(product_id=validated_data['id']).order_by('from_date').last()
            return price.price


class PriceSerializer(serializers.Serializer):
    price = serializers.IntegerField()
    date = serializers.DateField()


class PriceCategory(serializers.Serializer):
    category_id = serializers.IntegerField()
    price = serializers.IntegerField()


class AveragePrice(serializers.Serializer):
    MONTHS, DAYS = "MONTHS", "DAYS"
    SUM_TYPE = [
        (MONTHS, MONTHS),
        (DAYS, DAYS)
    ]

    product_id = serializers.IntegerField()
    from_date = serializers.DateField()
    to_date = serializers.DateField()
    sum_for = serializers.ChoiceField(choices=SUM_TYPE)
