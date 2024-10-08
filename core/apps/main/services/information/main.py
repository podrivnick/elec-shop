from dataclasses import dataclass
from typing import List

from core.apps.main.entities.information import InformationEntity
from core.apps.main.models.information import Information
from core.apps.main.services.information.base import BaseQueryFAQInformationService


@dataclass
class ORMQueryFAQInformationService(BaseQueryFAQInformationService):
    def get_all_information(
        self,
    ) -> List[InformationEntity]:
        all_information = Information.objects.all()

        return [information.to_entity() for information in all_information]
