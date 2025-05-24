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
    image_urls: list[HttpUrl] = Field(
        ..., description="List of URLs for product images"
    )
    rating: ProductRating = Field(
        ..., description="Nested object containing average rating and number of votes"
    )
    price: int = Field(..., description="Product price in Iranian Toman")
    category: str = Field(..., description="Product Category")


class DigikalaSearchToolInput(BaseModel):
    query: str = Field(..., description="Keyword or product name to search.")
    min_price: int | None = Field(
        ..., description="Minimum price in Iranian Toman, or None."
    )
    max_price: int | None = Field(
        ..., description="Maximum price in Iranian Toman, or None."
    )


class DigikalaSearchToolOutput(BaseModel):
    search_results: list[SearchResultProduct] = Field(
        ..., description="A list of products"
    )
