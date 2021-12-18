from django.db import models


class Subscriber(models.Model):
	email = models.EmailField(max_length=150, unique=True)

	def __str__(self):
		return self.email