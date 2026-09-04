from django.db import models

# Create your models here.
class Category(models.Model):
    slug models.SlugField()
    title models.CharField(max_length=255, db_index=True)

class MenuItem(models.Model):
    title models.CharField(max_length=255, db_index=True) 
    price models.DecimalField(max_digits=6, decimal_place=2, db_Index=True) 
    featured models.BooleanField(db_Index=True)
    category models.ForeignKey(Category, on_delete=modesl.PROTECT)