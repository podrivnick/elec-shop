from dataclasses import dataclass
from datetime import date
from typing import (
    List,
    Union,
)

from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from core.apps.main.models.products import Products
from core.apps.main.utils import GetUserModel

from .config import data_form_finalize
from .exceptions import *  # noqa
from .models import (
    LikesOpinion,
    Opinions,
)
from .utils import GetProductObjectUtils


User = get_user_model()


@dataclass
class GetOpinionsProduct:
    id_product: int

    def get_count_opinions(self) -> int:
        opinions = self.get_opinions_product()

        return len(opinions)

    def get_opinions_product(self) -> List:
        opinions = Opinions.objects.filter(id_product=self.id_product).select_related(
            "id_product",
            "user",
        )  # noqa
        opinions = [item for item in opinions]  # noqa

        return opinions


@dataclass
class IndexToMove:
    user: User
    opinions: Union[Opinions, QuerySet[Opinions]]

    def index_to_move_opinions(self):
        """Найти индекс мнения, оставленного данным пользователем.

        Используется генераторное выражение для перебора мнений.
        enumerate возвращает индекс и элемент на каждой итерации.

        """

        index_to_move = next(
            (i for i, item in enumerate(self.opinions) if item.user == self.user),
            None,
        )

        # Если мнение пользователя найдено (индекс не равен None)
        if index_to_move is not None:
            # Удалить элемент из текущей позиции и вставить его в начало списка
            self.opinions.insert(0, self.opinions.pop(index_to_move))

        return self.opinions


@dataclass
class ProductsPageServices:
    username: str
    opinions: Union[Opinions, QuerySet[Opinions]]
    product_object: Union[Products, QuerySet[Products]]
    is_page_of_product: bool

    def get_liked_opinions(self):
        if self.opinions:
            get_user_object = GetUserModel(self.username)
            user = get_user_object.get_user_model()

            list_liked_opinion = []

            for object_opinion in self.opinions:
                is_liked_opinion = LikesOpinion.objects.filter(
                    user=user,
                    id_product=self.product_object,
                    opinion_id=object_opinion.pk,
                ).select_related(
                    "id_product",
                    "user",
                )

                list_liked_opinion.append(is_liked_opinion.first())

            if self.is_page_of_product:
                services_change_opinions = IndexToMove(user, self.opinions)
                self.opinions = services_change_opinions.index_to_move_opinions()

                return self.opinions, list_liked_opinion
            else:
                return list_liked_opinion

        else:
            # Чтобы не попасть в ошибку DoesNotExist
            return [], []


@dataclass
class DeleteOpinionServices:
    username: str
    pk_product: int

    def delete_opinion_services(self):
        get_user_object = GetUserModel(self.username)
        user = get_user_object.get_user_model()

        opinion_user = Opinions.objects.get(user=user, id_product=self.pk_product)
        opinion_user.delete()


@dataclass
class SaveOpinionServices:
    username: str
    id_product: int
    opinion: str

    def save_opinion_services(self):
        get_user_object = GetUserModel(self.username)

        user = get_user_object.get_user_model()
        product_object = GetProductObjectUtils.get_product_object(int(self.id_product))

        opinions = Opinions.objects.filter(id_product=self.id_product, user=user)

        if not opinions:
            Opinions.objects.create(
                id_product=product_object,
                opinion=self.opinion,
                user=user,
                data_added=date.today(),
            )
            return True
        else:
            return False


@dataclass
class ChangerCountLikesServices:
    username: str
    id_product: int
    opinion_id: int

    def change_count_liked_opinions(self):
        get_user_object = GetUserModel(self.username)

        user = get_user_object.get_user_model()
        product = GetProductObjectUtils.get_product_object(int(self.id_product))
        opinion = Opinions.objects.get(pk=self.opinion_id, id_product=product)

        is_opinion_liked = LikesOpinion.objects.filter(
            user=user,
            id_product=product,
            opinion_id=opinion,
        ).first()

        if is_opinion_liked:
            is_opinion_liked.delete()
            opinion.likes = opinion.likes - 1
            new_count_like = opinion.likes
        else:
            LikesOpinion.objects.create(
                user=user,
                id_product=product,
                opinion_id=opinion,
            )
            opinion.likes = opinion.likes + 1
            new_count_like = opinion.likes

        opinion.save()

        return new_count_like


@dataclass
class FinalizeServices:
    username: str

    def formating_data_of_user_to_form(self):
        get_user_object = GetUserModel(self.username)

        user = get_user_object.get_user_model()

        initial_data = {}
        for key, value in data_form_finalize.items():
            try:
                if not hasattr(user, value):
                    raise AttributeNotInObject(value, user)  # noqa

                attribute_value = getattr(user, value)

                # Check for TypeError
                if not isinstance(user, get_user_model()):
                    raise ObjectNotValid(user)  # noqa

                # Check for ValueError
                if attribute_value is None:  # noqa
                    raise AttributeNotValid(user, value)  # noqa

                initial_data[key] = attribute_value
            except BaseExceptionClass as error:  # noqa
                print(error.message)
                """initial_data = { 'first_name': user.first_name, 'last_name':
                user.last_name, 'email': user.email,

                    'phone': user.phone,
                } - we'll get

                """

        return initial_data
