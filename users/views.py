from allauth.account.forms import default_token_generator
from allauth.account.models import EmailAddress
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.account.utils import url_str_to_user_pk as uid_decoder
from django.contrib.auth import get_user_model
from dj_rest_auth.registration.serializers import ResendEmailVerificationSerializer
from dj_rest_auth.registration.views import SocialLoginView # SocialConnectView,
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _
from rest_framework import permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView;


User = get_user_model();


# class FacebookConnectView(SocialConnectView):
# 	adapter_class = FacebookOAuth2Adapter


class FacebookLoginView(SocialLoginView):
	adapter_class = FacebookOAuth2Adapter


# class GoogleConnectView(SocialConnectView):
# 	adapter_class = GoogleOAuth2Adapter


class GoogleLoginView(SocialLoginView):
	adapter_class = GoogleOAuth2Adapter


class PasswordResetConfirmUIDTokenView(APIView):
	permission_classes = (permissions.AllowAny, )

	def get(self, request, *args, **kwargs):
		_uid = kwargs['uid']
		_token = kwargs['token']

		try:
			if (_uid is not None and _token is not None):
				try:
					uid = force_str(uid_decoder(_uid));
					user = User._default_manager.get(pk=uid)
				except (TypeError, ValueError, OverflowError, User.DoesNotExist):
					return Response({'uid': "Invalid value"}, status=status.HTTP_400_BAD_REQUEST)

				if not default_token_generator.check_token(user, _token):
					return Response({'token': "Invalid value"}, status=status.HTTP_400_BAD_REQUEST)

				if (user is not None and default_token_generator.check_token(user, _token) is True):
					return Response({'success': 'uid and token are valid'}, status=status.HTTP_200_OK)
				else:
					return Response({'error': "uid and token are invalid"}, status=status.HTTP_400_BAD_REQUEST)
			else:
				return Response({'error': "both token and uid are required"}, status=status.HTTP_400_BAD_REQUEST)
		except:
			return Response({'error': "something went wrong"},status=status.HTTP_400_BAD_REQUEST)


class ResendEmailVerificationView(CreateAPIView):
	permission_classes = (permissions.AllowAny,)
	serializer_class = ResendEmailVerificationSerializer

	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)

		try:
			email = EmailAddress.objects.get(**serializer.validated_data)	        	

			if email.verified:
				return Response({
					"error": "Email address is already verified"
				}, status=status.HTTP_400_BAD_REQUEST)

			email.send_confirmation()
			return Response({
				'detail': _('Email verification link sent')
			}, status=status.HTTP_200_OK)

		except EmailAddress.DoesNotExist:
			return Response({
				"error": "Email address does not exist"
			}, status=status.HTTP_400_BAD_REQUEST)
