from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class Costumer(models.Model):
    # CASCADE, when a user is deleted, will  delete it relationship with Costumer as well

    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)  # null=True, in order not to face errors while login
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)

    # in order to see the costumer name when add him on db rather than costumer(1)
    def __str__(self):
        if self.name:
            return self.name
        else:
            return self.email

    class Meta:
        db_table = "costumer"


class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)  # null=True, in order not to face errors while login

    def __str__(self):
        return self.name

    class Meta:
        db_table = "tag"


class Product(models.Model):
    CATEGORY = (
        ('Purito', 'Purito'),
        ('Missha', 'Missha'),
        ('Innistfree', 'Innistfree'),
        ('Isntree', 'Isntree'),
    )
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField(max_length=200, null=True)
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    description = models.CharField(max_length=200, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    # if pc can't find a specific img it gives empty img rather than error in all page
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    class Meta:
        db_table = "product"


class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered'),
    )
    # on_delete = models.SET_NULL, if we delete this costumer order, in db will remain no orders
    costumer = models.ForeignKey(Costumer, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total_price for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    class Meta:
        db_table = "order"


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total_price(self):
        total = self.product.price * self.quantity
        return total

    class Meta:
        db_table = "orderItem"

    def __str__(self):
        return str(self.product.name)


class ShippingAddress(models.Model):
    costumer = models.ForeignKey(Costumer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address

    class Meta:
        db_table = "shippingAddress"
