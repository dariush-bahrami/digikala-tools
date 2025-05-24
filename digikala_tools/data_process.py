from .pydantic_models import ProductRating, SearchResultProduct


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
