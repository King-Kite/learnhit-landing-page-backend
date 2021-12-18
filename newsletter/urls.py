from django.urls import path
from .views import SubscribeNewsLetter

urlpatterns = [
	path('newsletter/subscribe/', SubscribeNewsLetter.as_view(), name="subscribe-newsletter"),
]