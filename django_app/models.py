from django.db import models


class AttributeName(models.Model):
    nazev = models.CharField(max_length=255, null=True)
    zobrazit = models.BooleanField(null=True)
    kod = models.CharField(max_length=255, null=True)

    def to_dict(self):
        return {
            "id": self.id,
            "nazev": self.nazev,
            "zobrazit": self.zobrazit,
            "kod": self.kod,
        }


class AttributeValue(models.Model):
    hodnota = models.CharField(max_length=255)

    def to_dict(self):
        return {"id": self.id, "hodnota": self.hodnota}


class Attribute(models.Model):
    nazev_atributu = models.ForeignKey(AttributeName, on_delete=models.CASCADE)
    hodnota_atributu = models.ForeignKey(AttributeValue, on_delete=models.CASCADE)

    def to_dict(self):
        return {
            "id": self.id,
            "nazev_atributu": self.nazev_atributu.to_dict(),
            "hodnota_atributu": self.hodnota_atributu.to_dict(),
        }


class Product(models.Model):
    nazev = models.CharField(max_length=255)
    description = models.TextField()
    cena = models.DecimalField(max_digits=10, decimal_places=2)
    mena = models.CharField(max_length=3)
    published_on = models.DateTimeField(null=True, blank=True)
    is_published = models.BooleanField(default=False)

    def to_dict(self):
        return {
            "id": self.id,
            "nazev": self.nazev,
            "description": self.description,
            "cena": self.cena,
            "mena": self.mena,
            "published_on": self.published_on,
            "is_published": self.is_published,
        }


class ProductAttributes(models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def to_dict(self):
        return {
            "id": self.id,
            "attribute": self.attribute.to_dict(),
            "product": self.product.to_dict(),
        }


class Image(models.Model):
    obrazek = models.URLField()

    def to_dict(self):
        return {
            "id": self.id,
            "obrazek": self.obrazek,
        }


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    obrazek = models.ForeignKey(Image, on_delete=models.CASCADE)
    nazev = models.CharField(max_length=255)

    def to_dict(self):
        return {
            "id": self.id,
            "product": self.product.to_dict(),
            "obrazek": self.obrazek.to_dict(),
            "nazev": self.nazev,
        }


class Catalog(models.Model):
    nazev = models.CharField(max_length=255)
    obrazek = models.ForeignKey(Image, on_delete=models.CASCADE, null=True)
    products = models.ManyToManyField(Product)
    attributes = models.ManyToManyField(Attribute)

    def to_dict(self):
        return {
            "id": self.id,
            "nazev": self.nazev,
            "obrazek": self.obrazek.to_dict() if self.obrazek else None,
            "products": [product.id for product in self.products.all()],
            "attributes": [attribute.id for attribute in self.attributes.all()],
        }
