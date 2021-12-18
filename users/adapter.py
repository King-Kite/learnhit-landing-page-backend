import re
from allauth.account.adapter import DefaultAccountAdapter
from django import forms
from django.conf import settings


def get_context_url(context, url_string):
    try:
        url = context[url_string]
        return url
    except KeyError:
        return None

def get_uid_token_url(django_url, nextjs_url):
    try:
        pattern = re.compile(r"https?://(www\.)?[a-zA-z0-9:/.]+\/password\/reset\/confirm\/([a-zA-Z0-9_:.-]+)\/([a-zA-Z0-9_:.-]+)\/");
        match = pattern.search(django_url)

        if match is None:
            return django_url

        uid = match.group(2)
        token = match.group(3)

        url = f"{nextjs_url}/{uid}/{token}/"

        return url
    except:
        return django_url

def get_email_confirm_url(key):
    nextjs_url = settings.NEXTJS_EMAIL_CONFIRMATION_URL;
    url = f"{nextjs_url}/{key}/"
    return url


class CustomAllauthAdapter(DefaultAccountAdapter):
    # def clean_email(self, email):
    #     if email in settings.ACCOUNT_EMAIL_BLACKLIST:
    #         raise forms.ValidationError(f"{email} is not available")
    #     return super().clean_email(email)
        
    def send_mail(self, template_prefix, email, context):
        previous_confirm_email_url = get_context_url(context, 'activate_url')
        previous_password_reset_url = get_context_url(context, 'password_reset_url')

        if previous_confirm_email_url:
            context['activate_url'] = get_email_confirm_url(context['key'])

        if previous_confirm_email_url is not None and context['key'] is not None:
            context['activate_url'] = get_email_confirm_url(context['key'])

        if previous_password_reset_url is not None:
            context['password_reset_url'] = get_uid_token_url(
                previous_password_reset_url,
                settings.NEXTJS_PASSWORD_RESET_URL
            )

        msg = self.render_mail(template_prefix, email, context)
        msg.send()

    # def get_email_confirmation_url(self, request, emailconfirmation):
    #     """Constructs the email confirmation (activation) url.

    #     Note that if you have architected your system such that email
    #     confirmations are sent outside of the request context `request`
    #     can be `None` here.
    #     """

    #     url = reverse(
    #         "account_confirm_email",
    #         args=[emailconfirmation.key])
    #     ret = build_absolute_uri(
    #         request,
    #         url)
    #     return ret

    #     nextjs_url = settings.NEXTJS_EMAIL_CONFIRMATION_URL
    #     url = f"{nextjs_url}/${emailconfirmation.key}/"

    #     return url