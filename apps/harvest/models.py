from django.db import models
from django.contrib.auth.models import User


class Member(models.Model):
    CUSTOMER = 'CU'
    SUPPLIER = 'SP'
    DELIVERER = 'DE'
    USER_TYPE_CHOICE = (
        (CUSTOMER, 'Customer'),
        (SUPPLIER, 'Supplier'),
        (DELIVERER, 'Deliverer'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255)
    city = models.CharField(max_length=50)
    province = models.CharField(max_length=50)
    mobile = models.PositiveIntegerField()
    zipcode = models.IntegerField()
    usertype = models.CharField(max_length=2,
                                choices=USER_TYPE_CHOICE,
                                default=CUSTOMER)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
