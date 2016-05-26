from django.shortcuts import render, redirect
from django.views.generic import View
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth import forms, login, authenticate, logout


class ApplicationContext(object):

    @classmethod
    def context(cls):
        return {
            'title': '',
            'brand': 'harVestHub',
            'page_title': 'harVestHub',
            'warnings': [],
            'infos': [],
            'rightmenu': [
                {
                    'url': '/harvest/login',
                    'title': 'Login',
                },
                {
                    'url': '/harvest/register',
                    'title': 'Register',
                },
            ],
        }


class ApplicationView(object):
    template = ''
    context = None
    user = None

    def get(self, request):
        print('get', self.get_template())
        print('context:', self.context)
        return render(request, self.get_template(), self.context)

    def get_template(self):
        if self.template == '':
            raise ImproperlyConfigured('"Template" not defined.')
        return self.template


class Index(ApplicationView, View):
    context = ApplicationContext.context()
    context['title'] = 'Welcome!'
    template = 'index.html'


class Register(View):
    form = forms.UserCreationForm

    def get(self, request):
        print('register get')
        context = {'form': self.form()}
        print('context', context)
        return render(request, 'harvest/register.html', context)

    def post(self, request):
        print('register post')
        form = self.form(request.POST)
        print('form', form)
        print('isvalid', form.is_valid())
        if form.is_valid():
            form.save()
            return redirect('harvest/success')
        else:
            context = {'form': form}
            return render(request, 'harvest/register.html', context)


class RegisterSuccess(ApplicationView, View):
    context = ApplicationContext.context()
    # context['title'] =dd 'Welcome!'
    template = 'harvest/success.html'


class Login(View):
    form = forms.AuthenticationForm

    def get(self, request):
        print('login get')
        context = {'form': self.form()}
        print('context', context)
        return render(request, 'harvest/login.html', context)

    def post(self, request):
        print('login post')
        form = self.form(None, request.POST)
        context = {'form': form}
        print('form', form)
        print('context', context)
        print('is_valid', form.is_valid())
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/harvest/success')
            else:
                return render(request, 'harvest/login.html', context)
        else:
            return render(request, 'harvest/login.html', context)


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('/harvest/login')
