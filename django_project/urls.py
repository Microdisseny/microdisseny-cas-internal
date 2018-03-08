"""django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
import os
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse, HttpResponseForbidden
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic.base import RedirectView
import oauth2_provider.views as oauth2_views

from . import views


admin.site.site_header = os.getenv('ADMIN_SITE_HEADER',
                                   _('Microdisseny Internal CAS '
                                     'Administration'))
admin.site.site_title = os.getenv('ADMIN_SITE_TITLE',
                                  _('Microdisseny Internal CAS'))
admin.site.index_title = os.getenv('ADMIN_INDEX_TITLE',
                                   _('Site administration'))

# OAuth2 provider endpoints
oauth2_endpoint_views = [
    url(r'^authorize/$', oauth2_views.AuthorizationView.as_view(),
        name="authorize"),
    url(r'^token/$', oauth2_views.TokenView.as_view(), name="token"),
    url(r'^revoke-token/$', oauth2_views.RevokeTokenView.as_view(),
        name="revoke-token"),
    url(r'^introspect/$', oauth2_views.IntrospectTokenView.as_view(),
        name="introspect"),
]


def is_authenticated(request):
    if request.user.is_authenticated:
        return HttpResponse('OK')
    else:
        return HttpResponseForbidden()


urlpatterns = [
    url(r'^$', RedirectView.as_view(url='login'), name='redirect-to-login'),

    url(r'^accounts/login/$',
        LoginView.as_view(template_name='admin/login.html'),
        name='login'),
    url(r'^accounts/logout/$',
        LogoutView.as_view(next_page=reverse_lazy('login')),
        name='logout'),

    # oauth-toolkit
    # auth urls only
    url(r'^o/', include((oauth2_endpoint_views, 'oauth2_provider'),
                        namespace='oauth2_provider')),

    url(r'^is_authenticated?$', is_authenticated),
    url(r'^profile/$', views.ProfileView.as_view()),
    url(r'', include('mama_cas.urls')),
    url(r'^admin/', include('loginas.urls')),
    url(r'^admin/', admin.site.urls),
]
