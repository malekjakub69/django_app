from django.http import JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404, get_list_or_404
import json

from django.views.generic.detail import DetailView
from django.apps import apps

from django_app.models import (
    Attribute,
    AttributeName,
    AttributeValue,
    Catalog,
    Image,
    Product,
    ProductAttributes,
    ProductImage,
)


class BaseView(View):
    def get(self, request):
        return JsonResponse({"status": "success"})


class ImportView(View):
    def post(self, request):
        data = json.loads(request.body)
        for item in data:
            for key, value in item.items():
                print(key, value)
                if key == "AttributeName":
                    defaults = {
                        "nazev": value["nazev"] if "nazev" in value else None,
                        # default value is True
                        "zobrazit": value["zobrazit"] if "zobrazit" in value else True,
                    }
                    AttributeName.objects.update_or_create(
                        id=value["id"], defaults=defaults
                    )

                elif key == "AttributeValue":
                    AttributeValue.objects.update_or_create(
                        id=value["id"], hodnota=value["hodnota"]
                    )
                elif key == "Attribute":
                    defaults = {
                        "nazev_atributu": AttributeName.objects.get(
                            id=value["nazev_atributu_id"]
                        ),
                        "hodnota_atributu": AttributeValue.objects.get(
                            id=value["hodnota_atributu_id"]
                        ),
                    }
                    Attribute.objects.update_or_create(
                        id=value["id"], defaults=defaults
                    )
                elif key == "Product":
                    defaults = {
                        "nazev": value["nazev"],
                        "description": value["description"],
                        "cena": value["cena"],
                        "mena": value["mena"],
                        "published_on": value["published_on"],
                        "is_published": value["is_published"],
                    }
                    Product.objects.update_or_create(id=value["id"], defaults=defaults)
                elif key == "Catalog":
                    defaults = {
                        "nazev": value["nazev"],
                        "obrazek": value["obrazek"],
                        "products": Product.objects.filter(
                            id__in=value["products_ids"]
                        ),
                        "attributes": Attribute.objects.filter(
                            id__in=value["attributes_ids"]
                        ),
                    }
                    Catalog.objects.update_or_create(id=value["id"], defaults=defaults)
                elif key == "ProductAttributes":
                    defaults = {
                        "attribute": Attribute.objects.get(id=value["attribute"]),
                        "product": Product.objects.get(id=value["product"]),
                    }
                    ProductAttributes.objects.update_or_create(
                        id=value["id"], defaults=defaults
                    )
                elif key == "Image":
                    defaults = {"obrazek": value["obrazek"]}
                    Image.objects.update_or_create(id=value["id"], defaults=defaults)
                elif key == "ProductImage":
                    defaults = {
                        "product": Product.objects.get(id=value["product"]),
                        "obrazek": Image.objects.get(id=value["obrazek_id"]),
                        "nazev": value["nazev"],
                    }
                    ProductImage.objects.update_or_create(
                        id=value["id"], defaults=defaults
                    )
                else:
                    return JsonResponse({"status": "error", "message": "Neznámý klíč"})
        return JsonResponse({"status": "success"})


class DetailModelView(DetailView):
    def get(self, _, model_name):
        model = apps.get_model("django_app", model_name)
        data = model.objects.all()
        return JsonResponse({"data": list(data)})


class DetailModelWithIdView(View):
    def get(self, _, model_name, id):
        model = apps.get_model("django_app", model_name)
        print(model)
        data = get_object_or_404(model, id)
        return JsonResponse({"data": json.dumps(data)})
