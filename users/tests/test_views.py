import re
from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from django.core import mail
from django.urls import reverse
from .test_setup import TestSetUp

User = get_user_model()


""" Registration Tests """
class RegistrationTest(TestSetUp):
	""" Test the functionality of the Registration API """

	def test_registration(self):
		"""Test registration"""

		response = self.client.post(self.register_url, {
			"email": "JoN@WaYnE.com",
			"first_name": "Jon",
			"last_name": "Wayne",
			"password1": "Response2000",
			"password2": "Response2000",
		})

		user = User.objects.get(email="jon@wayne.com")

		self.assertEqual(response.status_code, 201)
		self.assertEqual(response.data['detail'], 'Verification e-mail sent.')
		self.assertIsNotNone(user)
		self.assertTrue(user.check_password('Response2000'))
		self.assertTrue(user.is_active)
		self.assertFalse(user.is_admin)
		self.assertFalse(user.is_staff)
		self.assertFalse(user.is_course_creator)
		self.assertFalse(user.is_superuser)


""" Login Tests """
class LoginTest(TestSetUp):
	""" Test the functionality of the Login API """

	def test_basic_login(self):
		"""Test login"""

		response = self.client.post(self.register_url, {
			"email": "jOhN@SmIth.iO",
			"first_name": "John",
			"last_name": "Smith",
			"password1": "Response12345",
			"password2": "Response12345",
		})

		user = User.objects.get(email="john@smith.io")

		response1 = self.client.post(self.login_url, {
			"email": "john@smith.io", "password": "Response12345" }, format="json")
		response2 = self.client.login(email="john@smith.io", password="Response12345")
		response3 = self.client.post(self.logout_url, {})

		email = mail.outbox[0]
		pattern = re.compile(r"https?://(www\.)?[a-zA-z0-9:/.]+\/account\/confirm\/email\/([a-zA-Z0-9_:.-]+)\/")
		match = pattern.search(email.body)

		response4 = self.client.get(reverse('account_confirm_email', kwargs={"key":match.group(2)}))
		user_verified = EmailAddress.objects.get(email=user.email, user_id=user.id)

		response5 = self.client.post(self.login_url, {
			"email": "john@smith.io", "password": "Response12345" }, format="json")

		self.assertEqual(response1.status_code, 400)
		self.assertEqual(response3.status_code, 401)
		self.assertEqual(response4.status_code, 302)
		self.assertEqual(response5.status_code, 200)
		self.assertEqual(email.to[0], "john@smith.io")
		self.assertEqual(len(match.group(2)), 53)
		self.assertTrue(response2)
		self.assertTrue(user.is_authenticated)
		self.assertTrue(user_verified)
		self.assertIsNotNone(match)
		self.assertIsNotNone(response5.data['access_token'])
		self.assertIsNotNone(response5.data['refresh_token'])
		with self.assertRaises(KeyError):
			access_token = response1.data['access_token']
			refresh_token = response1.data['refresh_token']

	def test_inactive_login(self):
		"""Test Failed Login For Inactive Users"""

		wayne = User.objects.create(email="wayne@smith.io")
		wayne.set_password("Response12345")
		wayne.is_active = False
		wayne.save()

		email_address = EmailAddress.objects.get_or_create(
			user_id=wayne.id, email="wayne@smith.io", verified=True, primary=True)

		response1 = self.client.post(self.login_url, {
			"email": "wayne@smith.io", "password": "Response12345" }, format="json")

		response2 = self.client.login(email=wayne.email, password="Response12345")

		response3 = self.client.post(self.logout_url, {})
		
		self.assertEqual(response1.status_code, 400)
		self.assertEqual(response3.status_code, 401)
		self.assertFalse(response2)
		with self.assertRaises(KeyError):
			token_key = response1.data['key']


""" Logout Tests """
class LogoutTest(TestSetUp):
	""" Test the functionality of the Login API """

	def test_basic_logout(self):
		"""Test login"""

		response1 = self.client.post(self.register_url, {
			"email": "janE@SmIth.iO",
			"first_name": "Jane",
			"last_name": "Smith",
			"password1": "Response12345",
			"password2": "Response12345",
		})

		email = mail.outbox[0]
		pattern = re.compile(r"https?://(www\.)?[a-zA-z0-9:/.]+\/account\/confirm\/email\/([a-zA-Z0-9_:.-]+)\/")
		match = pattern.search(email.body)
		response2 = self.client.get(reverse('account_confirm_email', kwargs={"key":match.group(2)}))

		response3 = self.client.post(self.login_url, {
			"email": "jane@smith.io", "password": "Response12345" }, format="json")

		response4 = self.client.post(self.logout_url, {}, format="json")

		response5 = self.client.post(self.logout_url, {
			"refresh": response3.data['refresh_token']
		}, format="json")

		response6 = self.client.post(self.login_url, {
			"email": "jane@smith.io", "password": "Response12345" }, format="json")

		self.assertEqual(response1.status_code, 201)
		self.assertEqual(response2.status_code, 302)
		self.assertEqual(response3.status_code, 200)
		self.assertEqual(response4.status_code, 401)
		self.assertEqual(response5.status_code, 200)
		self.assertEqual(response6.status_code, 200)
		self.assertNotEqual(response3.data['access_token'], response6.data['access_token'])
		self.assertNotEqual(response3.data['refresh_token'], response6.data['refresh_token'])
		self.assertIsNotNone(match)
		self.assertIsNotNone(response3.data['access_token'])
		self.assertIsNotNone(response3.data['refresh_token'])
		self.assertIsNotNone(response6.data['access_token'])
		self.assertIsNotNone(response6.data['refresh_token'])
		with self.assertRaises(KeyError):
			access_token = response1.data['access_token']
			refresh_token = response1.data['refresh_token']


""" User Data Tests"""
class UserDataTest(TestSetUp):
	""" Test the functionality of the User Data API """

	def test_get_user_data_without_authentication(self):
		response = self.client.get(self.user_data_url)
		self.assertEqual(response.status_code, 401)

	def test_get_user_data_with_authentication(self):
		barbie = User.objects.create(email="bar@bie.com")
		barbie.set_password("Response12345")
		barbie.is_active = True
		barbie.save()

		email_address = EmailAddress.objects.get_or_create(
			user_id=barbie.id, email="bar@bie.com", verified=True, primary=True)

		response1 = self.client.post(self.login_url, {
			"email": "bar@bie.com", "password": "Response12345" }, format="json")
		self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response1.data['access_token']}");

		response2 = self.client.get(self.user_data_url)

		self.assertEqual(response1.status_code, 200)
		self.assertEqual(response2.status_code, 200)
		self.assertEqual(response2.data['pk'], barbie.pk)
		self.assertEqual(response2.data['email'], "bar@bie.com")


""" Password Change Tests """
class PasswordChangeTest(TestSetUp):
	
	def test_change_password_by_unauthenticated_user(self):
		""" Test to check if the user is not authenticated """

		user = User.objects.create(email="myman@example.com")
		user.set_password('Passing1234')
		user.save()

		response = self.client.post(self.change_password_url, {
			"old_password": "Passing1234",
			"new_password1": "Password1234",
			"new_password2": "Password1234"
		})

		self.assertEqual(response.status_code, 401)

	def test_change_password_by_authenticated_user(self):
		""" Test to change password for an authenticated user """

		mrman = User.objects.create(email="mrman@test.com")
		mrman.set_password("Response12345")
		mrman.is_active = True
		mrman.save()

		email_address = EmailAddress.objects.get_or_create(
			user_id=mrman.id, email="mrman@test.com", verified=True, primary=True)

		response1 = self.client.post(self.login_url, {
			"email": "mrman@test.com", "password": "Response12345" }, format="json")
		self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response1.data['access_token']}");

		response2 = self.client.post(self.change_password_url, {
			"old_password": "Response12345",
			"new_password1": "PassTheGameHere1234",
			"new_password2": "PassTheGameHere1234"
		})

		mrman = User.objects.get(email="mrman@test.com")

		self.assertEqual(response1.status_code, 200)
		self.assertEqual(response2.status_code, 200)
		self.assertTrue(mrman.check_password("PassTheGameHere1234"))


""" Password Reset Tests"""
class PasswordReset(TestSetUp):
	
	def test_reset_password(self):
		user = User.objects.create(email="jimmy@olsen.com")
		user.set_password("Response12345")
		user.is_active = True
		user.save()

		response = self.client.post(self.reset_password_url, {
			"email": "emaildoesnotexist@doesnotexist.com"
		})

		response1 = self.client.post(self.reset_password_url, {
			"email": "jimmy@olsen.com",
		})

		email = mail.outbox[0];
		pattern = re.compile(r"https?://(www\.)?[a-zA-z0-9:/.]+\/account\/password\/reset\/confirm\/([a-zA-Z0-9_:.-]+)\/([a-zA-Z0-9_:.-]+)\/")
		match = pattern.search(email.body)

		url = match.group(0)
		uid = match.group(2)
		token = match.group(3)

		response2 = self.client.post(self.reset_password_confirm_url, {
			"uid": uid,
			"token": token,
			"new_password1": "PasswordJimmy12345",
			"new_password2": "PasswordJimmy12345"
		}, format="json")

		user_reset = User.objects.get(email="jimmy@olsen.com")

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response1.status_code, 200)
		self.assertEqual(response2.status_code, 200)
		self.assertTrue(user_reset.check_password("PasswordJimmy12345"))
		


""" Email Reconfirmation Tests"""
class EmailReconfirmationTest(TestSetUp):

	def test_email_reconfirmation(self):
		"""Test confirmation"""

		user = User.objects.create(email="jOhN@doe.oiO", first_name="John", last_name="Doe")
		user.set_password("Response12345")
		user.save()

		response1 = self.client.post(self.login_url, {
			"email": "john@doe.oio", "password": "Response12345" }, format="json")

		response2 = self.client.post(self.re_confirm_email, {
			"email": "john@doe.oio"}, format="json")

		response6 = self.client.post(self.register_url, {
			"email": "JohNny@WaYnE.com",
			"first_name": "Jon",
			"last_name": "Wayne",
			"password1": "Response2000",
			"password2": "Response2000",
		})

		email = mail.outbox[0]
		pattern = re.compile(r"https?://(www\.)?[a-zA-z0-9:/.]+\/account\/confirm\/email\/([a-zA-Z0-9_:.-]+)\/")
		match = pattern.search(email.body)

		response3 = self.client.get(reverse('account_confirm_email', kwargs={"key":match.group(2)}))

		response4 = self.client.post(self.login_url, {
			"email": "johnny@wayne.com", "password": "Response2000" }, format="json")

		response5 = self.client.post(self.re_confirm_email, {
			"email": "johnny@wayne.com"}, format="json")

		self.assertEqual(response1.status_code, 400)
		self.assertEqual(response2.status_code, 400)
		self.assertEqual(response3.status_code, 302)
		self.assertEqual(response4.status_code, 200)
		self.assertEqual(response5.status_code, 400)
		self.assertEqual(response6.status_code, 201)
		self.assertEqual(email.to[0], "johnny@wayne.com")
		self.assertEqual(len(match.group(2)), 53)
		self.assertIsNotNone(match)
		with self.assertRaises(KeyError):
			access_token = response1.data['access_token']
			refresh_token = response1.data['refresh_token']
