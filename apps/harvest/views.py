from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth import forms, login, authenticate, logout
from django.core.urlresolvers import reverse
from django.contrib import messages

from .forms import RegisterForm
from .models import Product


class ApplicationContext(object):

    @classmethod
    def context(cls, logged_in=False):
        print('login?', logged_in)
        if not logged_in:
            rightmenu = [
                {
                    'url': '/harvest/login',
                    'title': 'Login',
                },
                {
                    'url': '/harvest/register',
                    'title': 'Register',
                },
            ]
        else:
            rightmenu = [
                {
                    'url': '/harvest/products',
                    'title': 'Dashboard',
                },
                {
                    'url': '/logout',
                    'title': 'Logout',
                },
            ]

        return {
            'title': '',
            'brand': 'harVestHub',
            'page_title': 'harVestHub',
            'warnings': [],
            'infos': [],
            'rightmenu': rightmenu
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
    form = RegisterForm
    context = ApplicationContext.context()

    def get(self, request):
        print('register get')
        self.context['form'] = self.form()
        print('context', self.context)
        return render(request, 'harvest/register.html', self.context)

    def post(self, request):
        print('register post')
        form = self.form(request.POST)
        print('User', form)
        print('isvalid', form.is_valid())
        if form.is_valid():
            form.save()
            messages.add_message(self.request, messages.INFO,
                                 'Registered Account. Please Log In')
            return redirect('/harvest/success')
        else:
            context = {'form': form}
            return render(request, 'harvest/register.html', context)


class RegisterSuccess(ApplicationView, View):
    context = ApplicationContext.context()
    template = 'harvest/success.html'


class Login(View):
    form = forms.AuthenticationForm
    context = ApplicationContext.context()

    def get(self, request):
        print('login get')
        self.context['form'] = self.form()
        print('context', self.context)
        return render(request, 'harvest/login.html', self.context)

    def post(self, request):
        print('login post')
        form = self.form(None, request.POST)
        self.context['form'] = form
        print('form', form)
        print('context', self.context)
        print('is_valid', form.is_valid())
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/harvest/products')
            else:
                return render(request, 'harvest/login.html', self.context)
        else:
            return render(request, 'harvest/login.html', self.context)


class Logout(View):
    def get(self, request):
        logout(request)
        messages.add_message(self.request, messages.INFO, 'Logged out. Thank you for using na ka!')
        return redirect('/')


class Dashboard(View):
    def get(self, request):
        print('Dashboard get', request)
        return HttpResponse('DASHBOARD')


class ProductListView(ListView):
    model = Product
    template_name = 'harvest/products.html'

    def get_queryset(self):
        print('user', self.request.user.id)
        return Product.objects.filter(user_id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context.update(ApplicationContext.context(logged_in=True))

        print('context:', context)
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'harvest/product_show.html'

    def get_queryset(self):
        return Product.objects.filter(user_id=self.request.user.id)

    def get_context_data(self, **kwargs):
        print('ProductDetailView get_context_data')
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context.update(ApplicationContext.context(logged_in=True))
        print('context', context)
        return context


class ProductCreateView(CreateView):
    model = Product
    fields = ['name', 'description', 'category', 'stock', 'price']
    # form_class = ProductForm

    def get_success_url(self):
        print('ProductCreateView#get_success_url')
        print('object.id', self.object.id)
        return "harvest/products/{}".format(self.object.id)

    def form_valid(self, form):
        print('ProductCreateView#form_valid', form)
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        print('saved', self.object)
        messages.add_message(self.request, messages.INFO, 'Created Product')
        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        print('ProductCreateView#get_context_data', kwargs)
        context = super(ProductCreateView, self).get_context_data(**kwargs)
        context.update(ApplicationContext.context(logged_in=True))
        print('context', context)
        return context


class ProductDeleteView(DeleteView):
    model = Product
    success_url = '/harvest/products'


class ProductUpdateView(UpdateView):
    model = Product
    fields = ['name', 'description', 'category', 'stock', 'price']

    def get_success_url(self):
        print('ProductCreateView#get_success_url')
        print('object.id', self.object.id)
        return "harvest/products/{}".format(self.object.id)

    def form_valid(self, form):
        print('ProductCreateView#form_valid', form)
        self.object = form.save(commit=False)
        # self.object.user = self.request.user
        self.object.save()
        messages.add_message(self.request, messages.INFO, 'Updated Product')
        print('saved', self.object)
        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        print('ProductUpdateView#get_context_data', kwargs)
        context = super(ProductUpdateView, self).get_context_data(**kwargs)
        context.update(ApplicationContext.context(logged_in=True))
        print('method', self.request.method)
        if self.request.method == 'POST':
            context['warnings'] = ['aaaaaaaa']
        print('context', context)
        return context
