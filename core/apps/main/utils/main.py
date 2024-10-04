from dataclasses import dataclass

from django.contrib.auth import get_user_model
from django.contrib.postgres.search import (
    SearchHeadline,
    SearchQuery,
    SearchRank,
    SearchVector,
)


def q_search(query, current_db):
    if query.isdigit() and len(query) <= 7:
        return current_db.filter(id=int(query))

    vector = SearchVector("name", "description")
    query = SearchQuery(query)

    result = (
        current_db.annotate(rank=SearchRank(vector, query))
        .filter(rank__gt=0)
        .order_by("-rank")
    )

    result = result.annotate(
        headline=SearchHeadline(
            "name",
            query,
            start_sel='<span style="background-color: yellow;">',
            stop_sel="</span>",
        ),
    )

    result = result.annotate(
        bodyline=SearchHeadline(
            "description",
            query,
            start_sel='<span style="background-color: yellow;">',
            stop_sel="</span>",
        ),
    )

    return result


@dataclass
class GetUserModel:
    username: str

    def get_user_model(self):
        return get_user_model().objects.get(username=self.username)
