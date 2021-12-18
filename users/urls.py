from django.urls import path
from users.views import (
	FacebookLoginView, # FacebookConnectView, 
	GoogleLoginView, # GoogleConnectView, 
	PasswordResetConfirmUIDTokenView, ResendEmailVerificationView
)

urlpatterns = [
	# path('auth/social/facebook/connect/', FacebookConnectView.as_view(), name="facebook-connect"),
	path('auth/social/facebook/login/', FacebookLoginView.as_view(), name="facebook-login"),
	# path('auth/social/google/connect/', GoogleConnectView.as_view(), name="google-connect"),
	path('auth/social/google/login/', GoogleLoginView.as_view(), name="google-login"),
	path('auth/password_reset_confirm/<uid>/<token>/', PasswordResetConfirmUIDTokenView.as_view(), name="confirm-uid-token"),
	path('auth/account-re-confirm-email/', ResendEmailVerificationView.as_view(), name="account-re-confirm-email"),
]