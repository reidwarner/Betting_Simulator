import django.conf.urls.static
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView

urlpatterns = [
    path('betsim/', include('simulator.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include("accounts.urls")),
    path('accounts/', include("django.contrib.auth.urls")),
    path('', TemplateView.as_view(template_name="home.html"), name="home"),
]
