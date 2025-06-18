from django.db import models
from django.core.files import File
from barcode.writer import ImageWriter
from barcode import EAN13
import io, random


#category is about fruits, vegetables, etc
class Category(models.Model):
    category = models.CharField(max_length=100)
    
    def __str__(self):
        return self.category



#unit is about kgs, litres, etc
class Unit(models.Model):
    unit = models.CharField(max_length=100)
    
    def __str__(self):
        return self.unit
    
#Product details

class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True)
    barcode = models.CharField(max_length=13, blank=True, null=True, unique=True)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    quantity = models.IntegerField(default=0)
    order_level = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name
    
    barcode_image = models.ImageField(upload_to="barcodes/", blank=True)
    
    def save(self, *args, **kwargs):
        if not self.barcode:
            self.barcode = self._generate_unique_barcode()
        super().save(*args, **kwargs)
        
        if not self.barcode_image:
            self._generate_barcode_image()
    def _generate_unique_barcode(self):
        while True:
            code = str(random.randint(10**12, 10**13 - 1))  # 13 digits
            if not Product.objects.filter(barcode=code).exists():
                return code

    def _generate_barcode_image(self):
        rv = io.BytesIO()
        EAN13(self.barcode, writer=ImageWriter()).write(rv)
        rv.seek(0)
        filename = f"{self.pk}_{self.barcode}.png"
        self.barcode_image.save(filename, File(rv), save=True)
    
    quantity = models.IntegerField(default=0)
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(quantity__gte=0), 
                name="quantity_non_negative",
            )
        ]

class Movement_of_Items(models.Model):
    IN = 'IN'
    OUT = 'OUT'
    MOVEMENT_TYPE_CHOICES = [
        ("IN", "Stock In"),
        ("OUT", "Stock Out"),
    ]
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    movement_type = models.CharField(max_length=3, choices=MOVEMENT_TYPE_CHOICES)
    quantity = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    note =  models.TextField(blank=True, null=True, max_length=500)
    
    def save(self, *args, **kwargs):
        #updating the quantity of the product
        if self.movement_type == "IN":
            new_quantity = self.product.quantity + self.quantity
        
        else:
            new_quantity = self.product.quantity - self.quantity
            if new_quantity < 0:
                raise ValueError(
                    f"Cannot move {self.quantity}",
                    f"{self.product.name} has onyl {self.product.quantity}",
                )
        self.product.quantity = new_quantity
        self.product.save()
        super().save(*args, **kwargs)
        
        
    def __str__(self):
        return f"{self.product.name} {self.movement_type} {self.quantity}"
        