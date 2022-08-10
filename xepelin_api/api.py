from ninja import NinjaAPI
from xepelin_api.schema import InputSchema, Message, BorrameSchema
import requests

api = NinjaAPI()

@api.get("/hello")
def hello(request):
    return "Hello world"

@api.post("/hello2", response={200: Message, 201: Message})
def blog_scraper_endpoint(request, data: InputSchema):
    response = requests.post(data.webhook, json={"gspread_link": "hola", "email": "pirioja@uc.cl"})
    if response.status_code != 200:
        return 201, {"message": "Invalid webhook URL"}
    return 200, {"message": data.category}

@api.post('borrame')
def borrame(request, data: BorrameSchema):
    return data
