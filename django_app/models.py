from django.db import models


class AttributeName(models.Model):
    nazev = models.CharField(max_length=255, null=True)
    zobrazit = models.BooleanField()


class AttributeValue(models.Model):
    hodnota = models.CharField(max_length=255)


class Attribute(models.Model):
    nazev_atributu = models.ForeignKey(AttributeName, on_delete=models.CASCADE)
    hodnota_atributu = models.ForeignKey(AttributeValue, on_delete=models.CASCADE)


class Product(models.Model):
    nazev = models.CharField(max_length=255)
    description = models.TextField()
    cena = models.DecimalField(max_digits=10, decimal_places=2)
    mena = models.CharField(max_length=3)
    published_on = models.DateTimeField(null=True, blank=True)
    is_published = models.BooleanField(default=False)


class ProductAttributes(models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class Image(models.Model):
    obrazek = models.URLField()


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    obrazek = models.ForeignKey(Image, on_delete=models.CASCADE)
    nazev = models.CharField(max_length=255)


class Catalog(models.Model):
    nazev = models.CharField(max_length=255)
    obrazek = models.ForeignKey(Image, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    attributes = models.ManyToManyField(Attribute)
