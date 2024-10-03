from ninja import Schema


class FiltersProductsSchema(Schema):
    is_available: bool = None
    is_discount: bool = None
    is_sorting: bool = None
    query: bool = None
    slug: bool = None
