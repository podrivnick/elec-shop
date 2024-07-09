from django.contrib import admin
from .models import Opinions, LikesOpinion

class OpinionsAdmin(admin.ModelAdmin):
    list_display = ['id_product', 'user', 'opinion', 'data_added', 'likes']
    list_filter = ['id_product', 'likes']


admin.site.register(Opinions, OpinionsAdmin)
admin.site.register(LikesOpinion)