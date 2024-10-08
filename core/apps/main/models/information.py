from django.db import models

from core.apps.main.entities.information import InformationEntity


class Information(models.Model):
    text_info = models.TextField()

    class Meta:
        db_table = "information"
        verbose_name = "Информация"

    def to_entity(
        self,
    ) -> InformationEntity:
        return InformationEntity(
            text_info=self.text_info,
        )
