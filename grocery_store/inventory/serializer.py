from rest_framework import serializers
from .models import *

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Product
        fields = '__all__'            # or list them explicitly

class StockMovementSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Movement_of_Items
        fields = "__all__"