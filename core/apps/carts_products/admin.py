from django.contrib import admin

from core.apps.carts_products.models.review import (
    LikesReviews,
    Reviews,
)


class ReviewsAdmin(admin.ModelAdmin):
    list_display = ["id_product", "user", "review", "data_added", "likes"]
    list_filter = ["id_product", "likes"]


admin.site.register(Reviews, ReviewsAdmin)
admin.site.register(LikesReviews)
