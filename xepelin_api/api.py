from ninja import NinjaAPI
from xepelin_api.schema import SignleCategoryInputSchema, AllCategoriesInputSchema, MessageSchema
from xepelin_api.single_category_scrapper import single_category_scrapper_function
from xepelin_api.gspread_uploader import upload_posts_to_google_spread_sheet
from xepelin_api.all_categories_scrapper import all_categories_scrapper_function
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

api = NinjaAPI()

@api.post("/category_scrapper", response={200: MessageSchema, 422: MessageSchema})
def single_category_scrapper_endpoint(request, data: SignleCategoryInputSchema):
    blog_categories_dict = json.loads(os.environ.get("BLOG_CATEGORIES"))
    if data.category in blog_categories_dict:
        posts_list = single_category_scrapper_function(blog_categories_dict[data.category])
        upload_posts_to_google_spread_sheet(posts_list)
        response = requests.post(data.webhook, json={"link": os.environ.get("GSPREAD_LINK"), "email": os.environ.get("EMAIL")})
        if response.status_code != 200:
            return 200, MessageSchema(msg="Scrapper executed but unable to notify")
        return 200, MessageSchema(msg="Scrapper executed successfully")
    else:
        return 422, MessageSchema(msg="Invalid category name")
    

@api.post("/all_categories_scrapper_v1", response={200: MessageSchema, 422: MessageSchema})
def all_categories_scrapper_endpoint_v1(request, data: AllCategoriesInputSchema):
    blog_categories_dict = json.loads(os.environ.get("BLOG_CATEGORIES"))
    all_posts_list = []
    for category in blog_categories_dict:
        category_posts_list = single_category_scrapper_function(blog_categories_dict[category])
        all_posts_list += category_posts_list
    upload_posts_to_google_spread_sheet(all_posts_list)
    response = requests.post(data.webhook, json={"link": os.environ.get("GSPREAD_LINK"), "email": os.environ.get("EMAIL")})
    if response.status_code != 200:
        return 200, MessageSchema(msg="Scrapper executed but unable to notify")
    return 200, MessageSchema(msg="Scrapper executed successfully")


@api.post("/all_categories_scrapper_v2", response={200: MessageSchema, 422: MessageSchema})
def all_categories_scrapper_endpoint_v2(request, data: AllCategoriesInputSchema):
    all_categories_scrapper_function()
    response = requests.post(data.webhook, json={"link": os.environ.get("GSPREAD_LINK"), "email": os.environ.get("EMAIL")})
    if response.status_code != 200:
        return 200, MessageSchema(msg="Scrapper executed but unable to notify")
    return 200, MessageSchema(msg="Scrapper executed successfully")