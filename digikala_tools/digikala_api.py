"""
digikala_api.py

This module provides a function to query the Digikala e-commerce API for product search results.
It allows filtering by availability, sorting, and pagination.

DISCLAIMER:
- This code is intended for educational or personal use only.
- Usage of Digikala's API is not officially documented or endorsed.
- Excessive or automated querying may violate Digikala's terms of service.
- Use responsibly and respect the target site's rate limits and robots.txt policies.
"""

import urllib.parse
from typing import Literal

import requests
from fake_useragent import UserAgent
from requests.exceptions import JSONDecodeError

# Mapping of human-readable sorting options to Digikala's internal sort ID
sorting_order_name_to_id = {
    "most_relevant": 22,
    "most_viewed": 4,
    "newest": 1,
    "best_selling": 7,
    "cheapest": 20,
    "most_expensive": 21,
    "fastest_shipping": 25,
    "buyers_choice": 27,
    "featured": 29,
}

# Type hint for allowed sorting options
SortingOrder = Literal[
    "most_relevant",
    "most_viewed",
    "newest",
    "best_selling",
    "cheapest",
    "most_expensive",
    "fastest_shipping",
    "buyers_choice",
    "featured",
]


def search_digikala(
    query: str,
    has_selling_stock: bool | None = True,
    sorting_order: SortingOrder | None = "most_relevant",
    min_price: int | None = None,
    max_price: int | None = None,
    page: int | None = 1,
    headers: dict | None = None,
) -> dict:
    """
    Search for products on Digikala using its public search API.

    All price values are in Iranian Rial (IRR).

    Args:
        query (str): The search keyword or product name.
        has_selling_stock (bool | None): If True, limits results to items currently available for sale.
            If False, includes all items. If None, the filter is not applied. Defaults to True.
        sorting_order (SortingOrder | None): Optional sorting method (e.g., best-selling, cheapest). Defaults to "most_relevant".
        min_price (int | None): Optional minimum price filter in TMN. Defaults to None.
        max_price (int | None): Optional maximum price filter in TMN. Defaults to None.
        page (int | None): Page number for pagination, starting from 1. Defaults to 1.
        headers (dict | None): Optional HTTP headers. If not provided, a random User-Agent may be used.

    Returns:
        dict: Parsed JSON response from Digikala's API.

    Raises:
        requests.HTTPError: If the HTTP request returns an error status.
        Exception: If the response cannot be parsed as valid JSON.
    """
    # Construct URL
    params = {}
    if has_selling_stock is not None:
        params["has_selling_stock"] = int(has_selling_stock)
    if max_price is not None:
        params["price[max]"] = max_price * 10  # convert toman to rial
    if min_price is not None:
        params["price[min]"] = min_price * 10  # convert toman to rial
    params["q"] = query
    if sorting_order is not None:
        params["sort"] = sorting_order_name_to_id[sorting_order]
    if page is not None:
        params["page"] = page
    encoded_params = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
    url = f"https://api.digikala.com/v1/search/?{encoded_params}"

    # GET Request
    if headers is None:
        headers = {"user-agent": UserAgent().random}
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    # Return Response
    try:
        return response.json()
    except JSONDecodeError:
        raise Exception(f"Returned data is not valid JSON: {response.content}")
