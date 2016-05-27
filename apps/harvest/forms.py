from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Member


class RegisterForm(UserCreationForm):
    CUSTOMER = 'CU'
    SUPPLIER = 'SP'
    DELIVERER = 'DE'
    USER_TYPE_CHOICE = (
        (CUSTOMER, 'Customer'),
        (SUPPLIER, 'Supplier'),
        (DELIVERER, 'Deliverer'),
    )
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')
    email = forms.EmailField(label='Email Address')
    department = forms.CharField(label='Department')
    address1 = forms.CharField(label='address 1')
    address2 = forms.CharField(label='address 2')
    city = forms.CharField(label='city')
    province = forms.CharField(label='province')
    mobile = forms.IntegerField(label='mobile')
    zipcode = forms.IntegerField(label='zipcode')
    usertype = forms.ChoiceField(label='user type', choices=USER_TYPE_CHOICE)

    class Meta:
            model = User
            # model = Member
            fields = ('username', 'first_name', 'last_name',
                      'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        member = Member()
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password1'])
        # print('department:', self.cleaned_data['department'])
        # member.department = self.cleaned_data['department']
        if commit:
            user.save()
            print('user', user.id)
            member = user.member
            member.department = self.cleaned_data['department']
            member.address1 = self.cleaned_data['address1']
            member.address2 = self.cleaned_data['address2']
            member.city = self.cleaned_data['city']
            member.province = self.cleaned_data['province']
            member.mobile = self.cleaned_data['mobile']
            member.zipcode = self.cleaned_data['zipcode']
            member.usertype = self.cleaned_data['usertype']
            member.save()
            # member.user_id = user.id
            # member.save()
            return user
