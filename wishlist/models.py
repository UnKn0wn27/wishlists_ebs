from django.db import models
from django.contrib.auth.models import User


class List(models.Model):
    WISHLIST, MAGAZIN, CATEGORY = "WISHLIST", "MAGAZIN", "CATEGORY"
    LIST_TYPE = [
        (WISHLIST, WISHLIST),
        (MAGAZIN, MAGAZIN),
        (CATEGORY, CATEGORY)
    ]

    name = models.CharField(max_length=255)
    type = models.CharField(max_length=10, choices=LIST_TYPE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Products(models.Model):
    name = models.CharField(max_length=255)
    wished_product = models.IntegerField(default=0)
    list = models.ManyToManyField(List, related_name='products')

    def count_wished_product(self):
        self.wished_product = Products.objects.get(id=self.id).list.filter(type='WISHLIST').values(
            'user_id').distinct().count()
        self.save()


class PriceHistory(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    price = models.IntegerField()
    from_date = models.DateField()
