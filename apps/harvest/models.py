from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Member(models.Model):
    CUSTOMER = 'CU'
    SUPPLIER = 'SP'
    DELIVERER = 'DE'
    USER_TYPE_CHOICE = (
        (CUSTOMER, 'Customer'),
        (SUPPLIER, 'Supplier'),
        (DELIVERER, 'Deliverer'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    department = models.CharField(max_length=100, null=True)
    address1 = models.CharField(max_length=255, null=True)
    address2 = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=50, null=True)
    province = models.CharField(max_length=50, null=True)
    mobile = models.PositiveIntegerField(null=True)
    zipcode = models.IntegerField(null=True)
    usertype = models.CharField(max_length=2,
                                choices=USER_TYPE_CHOICE,
                                default=CUSTOMER, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def create_member(sender, instance, created, **kwargs):
        if created:
            # user is created, not changed
            Member.objects.create(user=instance)

    post_save.connect(create_member, sender=User)


class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    stock = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User)

