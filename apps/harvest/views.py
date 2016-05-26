from django.shortcuts import render
from django.views.generic import View
from django.core.exceptions import ImproperlyConfigured


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
