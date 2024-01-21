import re
from django.http import JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404, get_list_or_404
import json

from django.views.generic.detail import DetailView
from django.apps import apps
from django.core.serializers import serialize

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
                # AttributeName parser
                if key == "AttributeName":
                    # create default values
                    defaults = {
                        "nazev": value["nazev"] if "nazev" in value else None,
                        "zobrazit": value["zobrazit"] if "zobrazit" in value else None,
                    }
                    # update or create
                    AttributeName.objects.update_or_create(
                        id=value["id"],
                        defaults={
                            key: val for key, val in defaults.items() if val is not None
                        },
                    )

                # AttributeValue parser
                elif key == "AttributeValue":
                    # create default values
                    defaults = {
                        "hodnota": value["hodnota"] if "hodnota" in value else None,
                    }
                    # update or create
                    AttributeValue.objects.update_or_create(
                        id=value["id"],
                        defaults={
                            key: val for key, val in defaults.items() if val is not None
                        },
                    )

                # Attribute parser
                elif key == "Attribute":
                    # create default values
                    defaults = {
                        "nazev_atributu": AttributeName.objects.get(
                            id=value["nazev_atributu_id"]
                            if "nazev_atributu_id" in value
                            else None
                        ),
                        "hodnota_atributu": AttributeValue.objects.get(
                            id=value["hodnota_atributu_id"]
                            if "hodnota_atributu_id" in value
                            else None
                        ),
                    }
                    # update or create
                    Attribute.objects.update_or_create(
                        id=value["id"],
                        defaults={
                            key: val for key, val in defaults.items() if val is not None
                        },
                    )

                # Product parser
                elif key == "Product":
                    # create default values
                    defaults = {
                        "nazev": value["nazev"] if "nazev" in value else None,
                        "description": value["description"]
                        if "description" in value
                        else None,
                        "cena": value["cena"] if "cena" in value else None,
                        "mena": value["mena"] if "mena" in value else None,
                        "published_on": value["published_on"]
                        if "published_on" in value
                        else None,
                        "is_published": value["is_published"]
                        if "is_published" in value
                        else None,
                    }
                    # update or create
                    Product.objects.update_or_create(
                        id=value["id"],
                        defaults={
                            key: val for key, val in defaults.items() if val is not None
                        },
                    )

                # Catalog parser
                elif key == "Catalog":
                    # create default values
                    defaults = {
                        "nazev": value["nazev"] if "nazev" in value else None,
                        "obrazek": value["obrazek"] if "obrazek" in value else None,
                    }
                    # update or create
                    Catalog.objects.update_or_create(
                        id=value["id"],
                        defaults={
                            key: val for key, val in defaults.items() if val is not None
                        },
                    )
                    # add products and attributes (M:N relation)
                    products = (
                        Product.objects.filter(id__in=value["products_ids"])
                        if "products_ids" in value
                        else []
                    )
                    attributes = (
                        Attribute.objects.filter(id__in=value["attributes_ids"])
                        if "attributes_ids" in value
                        else []
                    )
                    for product in products:
                        Catalog.objects.get(id=value["id"]).products.add(product)
                    for attribute in attributes:
                        Catalog.objects.get(id=value["id"]).attributes.add(attribute)

                # ProductAttributes parser
                elif key == "ProductAttributes":
                    # create default values
                    defaults = {
                        "attribute": Attribute.objects.get(id=value["attribute"])
                        if "attribute" in value
                        else None,
                        "product": Product.objects.get(id=value["product"])
                        if "product" in value
                        else None,
                    }
                    # update or create
                    ProductAttributes.objects.update_or_create(
                        id=value["id"],
                        defaults={
                            key: val for key, val in defaults.items() if val is not None
                        },
                    )

                # Image parser
                elif key == "Image":
                    defaults = {
                        "obrazek": value["obrazek"] if "obrazek" in value else None
                    }
                    # update or create
                    Image.objects.update_or_create(
                        id=value["id"],
                        defaults={
                            key: val for key, val in defaults.items() if val is not None
                        },
                    )

                # ProductImage parser
                elif key == "ProductImage":
                    # create default values
                    defaults = {
                        "product": Product.objects.get(id=value["product"])
                        if "product" in value
                        else None,
                        "obrazek": Image.objects.get(id=value["obrazek_id"])
                        if "obrazek_id" in value
                        else None,
                        "nazev": value["nazev"] if "nazev" in value else None,
                    }
                    # update or create
                    ProductImage.objects.update_or_create(
                        id=value["id"],
                        defaults={
                            key: val for key, val in defaults.items() if val is not None
                        },
                    )
                else:
                    return JsonResponse({"status": "error", "message": "Neznámý klíč"})
        return JsonResponse({"status": "success"})


class DetailModelView(DetailView):
    def get(self, _, model_name):
        # try to get model
        try:
            model = apps.get_model("django_app", model_name)
        except:
            return JsonResponse({"error": "Model does not exist"}, status=404)
        # get data
        data = model.objects.all()
        # return data
        return JsonResponse({"data": [item.to_dict() for item in data]})


class DetailModelWithIdView(View):
    def get(self, _, model_name, id):
        # try to get model
        try:
            model = apps.get_model("django_app", model_name)
        except:
            return JsonResponse({"error": "Model does not exist"}, status=404)
        # get data
        data = model.objects.get(id=id)
        # return data
        return JsonResponse({"data": data.to_dict()})
