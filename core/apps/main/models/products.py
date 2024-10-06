from django.db import models

from core.apps.common.models import TimeBaseModel
from core.apps.main.entities.product import (
    CategoriesProduct,
    ProductEntity,
)


class Products(TimeBaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    slug = models.SlugField(unique=True, null=True, max_length=100, verbose_name="URL")
    image = models.ImageField(upload_to="products/%Y/%m/%d/")
    discount = models.DecimalField(
        blank=True,
        max_digits=10,
        default=0.00,
        decimal_places=2,
    )
    price = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    count_product = models.PositiveIntegerField(default=0, verbose_name="Количество")
    category = models.ForeignKey(
        "CategoriesProduct",
        on_delete=models.PROTECT,
        blank=True,
    )
    id_product = models.DecimalField(decimal_places=0, max_digits=7, null=True)

    class Meta:
        db_table = "products"
        verbose_name = "Товары"
        ordering = ("id",)

    def to_entity(self) -> ProductEntity:
        return ProductEntity(
            id_product=self.id_product,
            name=self.name,
            description=self.description,
            slug=self.slug,
            image=self.image,
            discount=self.discount,
            price=self.price,
            count_product=self.count_product,
            category=self.category,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    def __str__(self):
        return self.name


class CategoriesProduct(TimeBaseModel):
    category = models.CharField(max_length=40, unique=True)
    slug = models.SlugField(unique=True, max_length=40, null=True)

    def to_entity(self) -> CategoriesProduct:
        return CategoriesProduct(
            category=self.category,
            slug=self.slug,
        )

    def __str__(self):
        return self.category

    class Meta:
        db_table = "category"
        verbose_name = "Категорию"
        ordering = ("id",)
