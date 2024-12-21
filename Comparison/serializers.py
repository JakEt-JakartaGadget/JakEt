# Comparison/serializers.py

from rest_framework import serializers
from .models import Gadget

class GadgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gadget
        fields = '__all__'
