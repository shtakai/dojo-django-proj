"""harvesthub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, patterns
from django.contrib.auth.decorators import login_required
from . import views

# urlpatterns = ['',
    # url(r'^$', views.Register.as_view(), name='accounts-register'),
    # # url(r'^$', Index.as_view()),
# ]
urlpatterns = patterns(
    '',
    url(r'login', views.Login.as_view(), name='accounts-login'),
    url(r'logout', views.Logout.as_view(), name='accounts-logout'),
    url(r'register', views.Register.as_view(), name='accounts-register'),
    url(r'success', views.RegisterSuccess.as_view()),
    url(r'dashboard', login_required(views.Dashboard.as_view()),
        name='dashboard'),
    url(r'^products$', login_required(views.ProductListView.as_view()),
        name='product-list'),
    url(r'products/create$',
        login_required(views.ProductCreateView.as_view()),
        name='product-create'),
    url(r'products/(?P<pk>[-_\w]+)$',
        login_required(views.ProductDetailView.as_view()),
        name='product-detail'),
    url(r'products/(?P<pk>[-_\w]+)/delete$',
        login_required(views.ProductDeleteView.as_view()),
        name='product-delete'),
    url(r'products/(?P<pk>[-_\w]+)/update$',
        login_required(views.ProductUpdateView.as_view()),
        name='product-delete'),
    url(r'^$', views.Index.as_view()),
)
