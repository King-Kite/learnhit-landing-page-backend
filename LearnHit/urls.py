from allauth.account.views import ConfirmEmailView
from django.contrib import admin
from django.urls import include, path

from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = "LearnHit Administration"
admin.site.site_title = "LearnHit Administration Portal"
admin.site.index_title = "LearnHit Administration Portal"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),

    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    path('auth/account-confirm-email/<str:key>/',  ConfirmEmailView.as_view(), name="account_confirm_email"),

    path('', include('newsletter.urls')),
    path('', include('users.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
