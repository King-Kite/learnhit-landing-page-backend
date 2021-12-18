from rest_framework import serializers
from .models import Subscriber

class NewsLetterSerializer(serializers.ModelSerializer):
	class Meta:
		model = Subscriber
		fields = '__all__'
