import datetime
from django.db import models
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products')
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, related_name='products', null=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ('-created',)
        index_together = (('id', ),)

    def __str__(self):
        return self.name

    @property
    def as_json(self):
        return {
            'name': self.name,
            'image': self.image.url,
            'description': self.description,
            'price': str(self.price),
            'available': str(self.available)
        }


class Client(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=200)
    email = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.first_name}' \
               f'\n{self.last_name}'


class Order(models.Model):
    city = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    total_price = models.FloatField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)
        index_together = (('id', ),)

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)

    def __str__(self):
        return f'Заказ от: {self.client.first_name} {self.client.last_name}'
