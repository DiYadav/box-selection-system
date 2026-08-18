from django.db import models
from django.core.validators import MinValueValidator
from django.db import models



from django.core.validators import MinValueValidator
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    length_cm = models.DecimalField(max_digits=8,decimal_places=2,validators=[MinValueValidator(0.01)],)
    width_cm = models.DecimalField(max_digits=8,decimal_places=2,validators=[MinValueValidator(0.01)],)
    height_cm = models.DecimalField(max_digits=8,decimal_places=2,validators=[MinValueValidator(0.01)],)
    weight_kg = models.DecimalField(max_digits=8, decimal_places=2,validators=[MinValueValidator(0.01)],)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    @property
    def dimensions(self):
        return (self.length_cm,self.width_cm,self.height_cm,)

    @property
    def volume_cm3(self):
        return (self.length_cm * self.width_cm * self.height_cm)


class Box(models.Model):
    code = models.CharField(max_length=50,unique=True,)
    name = models.CharField(max_length=255)
    internal_length_cm = models.DecimalField(max_digits=8,decimal_places=2,validators=[MinValueValidator(0.01)],)
    internal_width_cm = models.DecimalField(max_digits=8,decimal_places=2,validators=[MinValueValidator(0.01)],)
    internal_height_cm = models.DecimalField(max_digits=8,decimal_places=2,validators=[MinValueValidator(0.01)],)
    max_weight_kg = models.DecimalField(max_digits=8,decimal_places=2, validators=[MinValueValidator(0.01)],)
    cost = models.DecimalField(max_digits=8,decimal_places=2,validators=[MinValueValidator(0)],)

    class Meta:
        ordering = ["cost"]

    def __str__(self):
        return f"{self.code} ({self.name})"

    @property
    def internal_dimensions(self):
        return (self.internal_length_cm,self.internal_width_cm,self.internal_height_cm,)

    @property
    def internal_volume_cm3(self):
        return (self.internal_length_cm * self.internal_width_cm * self.internal_height_cm)


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    recommended_box = models.ForeignKey(Box,null=True,blank=True,on_delete=models.SET_NULL,related_name="orders",)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.pk}"



class OrderItem(models.Model):
    order = models.ForeignKey(Order,related_name="items",on_delete=models.CASCADE,)
    product = models.ForeignKey(Product,on_delete=models.PROTECT,)
    quantity = models.PositiveIntegerField( default=1, validators=[MinValueValidator(1)],)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"