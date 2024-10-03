# admin.site.register(Information)
# admin.site.register(Favorites)


# @admin.register(Categories_Product)
# class CategoriesAdmin(admin.ModelAdmin):
#     prepopulated_fields = {"slug": ("category",)}
#     list_display = ["category",]


# @admin.register(Products)
# class ProductsAdmin(admin.ModelAdmin):
#     prepopulated_fields = {"slug": ("name",)}
#     list_display = ["name", "price", "discount"]
#     list_editable = ["discount",]
#     search_fields = ["name", "description"]
#     list_filter = ["discount", "category"]
#     fields = [
#         "name",
#         "category",
#         "slug",
#         "description",
#         "image",
#         ("price", "discount"),
#         "count_product",
#         "id_product"
#     ]
