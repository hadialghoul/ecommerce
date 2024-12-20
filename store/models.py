from django.db import models

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=255,db_index=True)# y3ne bas yl2e lname bw2f mish bymr2 3layhon kelon
    slug=models.SlugField(max_length=250,unique=True)

    class Meta:
        verbose_name_plural='categories'# hek bbyn esma bel admin

    def __str__(self):
        return self.name

class Product(models.Model):
    category=models.ForeignKey(Category,related_name='product',on_delete=models.CASCADE,null=True)
    title=models.CharField(max_length=250)
    brand=models.CharField(max_length=250, default='un_branded')
    description=models.TextField(blank=True)
    slug=models.SlugField(max_length=255)
    price=models.DecimalField(max_digits=4,decimal_places=2)
    image=models.ImageField(upload_to='images/')

    class Meta:
        verbose_name_plural='products'

    def __str__(self):
        return self.title


