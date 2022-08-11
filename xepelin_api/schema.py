from ninja import Schema

class SignleCategoryInputSchema(Schema):
    category: str
    webhook: str

class AllCategoriesInputSchema(Schema):
    webhook: str

class Message(Schema):
    message: str

class BorrameSchema(Schema):
    link: str
    email: str