from typing import List

from pydantic import BaseModel, Field, HttpUrl


class ProductRating(BaseModel):
    rate: float = Field(
        ..., description="Average user rating as a percentage (e.g., 89.6 means 89.6%)"
    )
    count: int = Field(..., description="Total number of user ratings for the product")


class SearchResultProduct(BaseModel):
    product_id: int = Field(..., description="Unique identifier of the product")
    title_fa: str = Field(..., description="Product title in Persian (Farsi)")
    title_en: str = Field(..., description="Product title in English")
    url: HttpUrl = Field(..., description="Direct URL to the product page")
    image_urls: List[HttpUrl] = Field(
        ..., description="List of URLs for product images"
    )
    rating: ProductRating = Field(
        ..., description="Nested object containing average rating and number of votes"
    )
    price: int = Field(..., description="Product price in Iranian Toman")
    category: str = Field(..., description="Product Category")


def process_search_result(search_resul: dict) -> list[SearchResultProduct]:
    BASE_URL = "https://www.digikala.com/"
    status = search_resul["status"]
    data = search_resul["data"]
    products = data["products"]
    processed_products = []
    for product in products:
        processed_products.append(
            SearchResultProduct(
                product_id=product["id"],
                title_fa=product["title_fa"],
                title_en=product["title_en"],
                url=BASE_URL + product["url"]["uri"],
                image_urls=product["images"]["main"]["url"],
                rating=ProductRating(**product["rating"]),
                # convert price to toman
                price=product["default_variant"]["price"]["selling_price"] // 10,
                category=product["data_layer"]["category"],
            )
        )
    return processed_products
