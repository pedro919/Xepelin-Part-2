from ninja import Schema

class InputSchema(Schema):
    category: str
    webhook: str

class Message(Schema):
    message: str

class BorrameSchema(Schema):
    gspread_link: str
    email: str