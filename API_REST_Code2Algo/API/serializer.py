from rest_framework_mongoengine import serializers

from .models import Methods


class MethodsSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Methods
        fields = '__all__'
