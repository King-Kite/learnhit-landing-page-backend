from django.contrib.auth import get_user_model;


User = get_user_model()


def get_anonymous_user():
    user = User.objects.get_or_create(email="anonymous@learnhit.com")
    return user[0].id