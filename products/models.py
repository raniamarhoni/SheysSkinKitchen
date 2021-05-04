from django.db import models


class Category(models.Model):

    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Product(models.Model):
    category = models.ForeignKey('Category', null=True, blank=True,
                                 on_delete=models.SET_NULL)
    name = models.CharField(max_length=254)
    description = models.TextField()
    ingredients = models.TextField()
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name


class Size(models.Model):
    product = models.ForeignKey(
        'Product', null=True, blank=True, on_delete=models.SET_NULL)
    sku = models.CharField(max_length=254, null=True, blank=True)
    size = models.CharField(max_length=25)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    stock = models.DecimalField(max_digits=6, decimal_places=0)

    def __str__(self):
        return self.size


class Review(models.Model):
    product = models.ForeignKey(
        'Product', null=True, on_delete=models.SET_NULL)
    star = models.IntegerField(null=True, blank=True)
    review = models.TextField()
    date_created = models.DateField()

    def __str__(self):
        return str(self.star)
