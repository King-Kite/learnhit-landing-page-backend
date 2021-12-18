from dj_rest_auth.serializers import UserDetailsSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import Profile

try:
    from allauth.account import app_settings as allauth_settings
    from allauth.account.adapter import get_adapter
    from allauth.utils import email_address_exists
except ImportError:
    raise ImportError('allauth needs to be added to INSTALLED_APPS.')


class ProfileSerializer(serializers.ModelSerializer):
	class Meta:
		model = Profile
		exclude = ('user', 'date_created')


class RegistrationSerializer(RegisterSerializer):

	first_name = serializers.CharField(required=True)
	last_name = serializers.CharField(required=True)
	middle_name = serializers.CharField(required=True)

	def validate_email(self, email):
		email = get_adapter().clean_email(email.lower())
		if allauth_settings.UNIQUE_EMAIL:
			if email and email_address_exists(email):
				raise serializers.ValidationError(
					_('A user is already registered with this e-mail address.'),
				)
		return email

	def custom_signup(self, request, user):
		user.first_name = self.validated_data.get('first_name', '')
		user.last_name = self.validated_data.get('last_name', '')
		user.middle_name = self.validated_data.get('middle_name', "")
		user.save(update_fields=['first_name', 'last_name', 'middle_name'])


class UserDetailSerializer(UserDetailsSerializer):
	profile = ProfileSerializer(read_only=True)
	token = serializers.SerializerMethodField('get_token')

	class Meta(UserDetailsSerializer.Meta):
		fields = UserDetailsSerializer.Meta.fields + ('is_course_creator', 'premium', 'profile', 'token')

	def get_token(self, obj):
		try:
			token = Token.objects.get(user=obj)
			return token.key
		except Token.DoesNotExist:
			token = Token.objects.create(user=obj)
			return token.key
