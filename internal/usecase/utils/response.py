from internal.usecase.utils import ResponseExample, ResponseSchema

HTTP_400_BAD_REQUEST = ResponseSchema(
    status_code=400,
    description='Bad request',
    example=ResponseExample(successful=False, detail='Bad request'),
)

HTTP_401_UNAUTHORIZED = ResponseSchema(
    status_code=401,
    description='Unauthorized',
    example=ResponseExample(successful=False, detail='Unauthorized'),
)

HTTP_403_FORBIDDEN = ResponseSchema(
    status_code=403,
    description='Forbidden',
    example=ResponseExample(successful=False, detail='Forbidden'),
)
HTTP_404_NOT_FOUND = ResponseSchema(
    status_code=404,
    description='Not found',
    example=ResponseExample(successful=False, detail='Not found'),
)
