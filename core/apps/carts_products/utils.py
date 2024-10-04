from django.shortcuts import get_object_or_404

from core.apps.main.models.products import Products


class GetProductObjectUtils:
    @staticmethod
    def get_product_object(id_product_or_slug):
        """Получить объект продукта по идентификатору или slug."""
        return (
            get_object_or_404(Products, id=id_product_or_slug)
            if isinstance(id_product_or_slug, int)
            else get_object_or_404(Products, slug=id_product_or_slug)
        )
