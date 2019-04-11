from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.views.generic import TemplateView


class RedirectLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'admin/login.html'
    extra_context = {
        'site_title': settings.ADMIN_SITE_TITLE,
        'site_header': settings.ADMIN_SITE_HEADER
    }


class ProfileView(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        user = request.user
        return JsonResponse({
            'username': user.username,
        })
