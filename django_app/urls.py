from django.urls import path

from django_app.views import (
    BaseView,
    DetailModelView,
    DetailModelWithIdView,
    ImportView,
)


urlpatterns = [
    path("", BaseView.as_view(), name="base"),
    path("import", ImportView.as_view(), name="import"),
    path("detail/<str:model_name>/", DetailModelView.as_view(), name="detail"),
    path(
        "detail/<str:model_name>/<int:id>/",
        DetailModelWithIdView.as_view(),
        name="detail_id",
    ),
]
