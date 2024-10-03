from django.db import models


class Information(models.Model):
    text_info = models.TextField()

    class Meta:
        db_table = "information"
        verbose_name = "Информация"
