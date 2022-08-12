from ninja import Schema

class SignleCategoryInputSchema(Schema):
    category: str
    webhook: str

class AllCategoriesInputSchema(Schema):
    webhook: str

class MessageSchema(Schema):
    msg: str
