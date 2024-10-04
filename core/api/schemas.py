from ninja import Schema


class PingResponseSchema(Schema):
    result: bool
