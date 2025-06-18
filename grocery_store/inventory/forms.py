from django.db import models
from django.forms import ModelForm
from .models import *


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ["name", "category", "unit", "barcode", "cost_price", "selling_price", "order_level"]

class StockForm(ModelForm):
    class Meta:
        model = Movement_of_Items
        fields = ["product", "movement_type", "quantity", "note"]