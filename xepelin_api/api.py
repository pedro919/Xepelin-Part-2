from ninja import NinjaAPI
from xepelin_api.schema import SignleCategoryInputSchema, AllCategoriesInputSchema, Message, BorrameSchema
from xepelin_api.scraper import blog_scraper
from xepelin_api.gspread_uploader import upload_posts_to_google_spread_sheet
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

api = NinjaAPI()

@api.get("/hello")
def hello(request):
    return "Hello world"

@api.post("/category_scrapper", response={200: Message, 201: Message, 422: Message})
def single_category_scraper_endpoint(request, data: SignleCategoryInputSchema):
    blog_categories_dict = json.loads(os.environ.get("BLOG_CATEGORIES"))
    if data.category in blog_categories_dict:
        posts_list = blog_scraper(blog_categories_dict[data.category])
        upload_posts_to_google_spread_sheet(posts_list)
        response = requests.post(data.webhook, json={"link": os.environ.get("GSPREAD_LINK"), "email": os.environ.get("EMAIL")})
        if response.status_code != 200:
            return 200, {"message": "Invalid webhook URL"}
        return 200, {"message": "Scraper executed successfully"}
    else:
        return 422, {"message": "Invalid category name"}
    

@api.post("/all_categories_scrapper", response={200: Message, 201: Message, 422: Message})
def single_category_scraper_endpoint(request, data: AllCategoriesInputSchema):
    blog_categories_dict = json.loads(os.environ.get("BLOG_CATEGORIES"))
    all_posts_list = []
    for category in blog_categories_dict:
        category_posts_list = blog_scraper(blog_categories_dict[category])
        all_posts_list += category_posts_list
    upload_posts_to_google_spread_sheet(all_posts_list)
    response = requests.post(data.webhook, json={"link": os.environ.get("GSPREAD_LINK"), "email": os.environ.get("EMAIL")})
    if response.status_code != 200:
        return 200, {"message": "Invalid webhook URL"}
    return 200, {"message": "Scraper executed successfully"}


@api.post('borrame')
def borrame(request, data: BorrameSchema):
    return data
