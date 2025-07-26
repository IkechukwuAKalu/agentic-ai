import datetime
from typing import Dict, Any

def call_competitor_pricing_api(product_name: str, date: datetime.date) -> Dict[str, Any]:
    data = get_competitor_pricing_data()

    data_by_product_name_and_date = {
        (item["product"], item["date"]): item for item in data
    }
    
    try:
        return data_by_product_name_and_date[(product_name, date.strftime("%Y-%m-%d"))]
    except KeyError:
        print(f"No data found for product {product_name} and date {date}")
        return None


def get_competitor_pricing_data():
    return [
        {
            "product": "Product 1",
            "date": "2024-01-10",
            "our_price": 60.97,
            "competitor_sales": {},
            "competitor_a_price": 56.88,
            "competitor_b_price": 62.23,
            "competitor_c_price": 51.8,
        },
        {
            "product": "Product 1",
            "date": "2024-01-11",
            "our_price": 60.97,
            "competitor_sales": {},
            "competitor_a_price": 59.65,
            "competitor_b_price": 72.47,
            "competitor_c_price": 72.5,
        },
        {
            "product": "Product 1",
            "date": "2024-01-12",
            "our_price": 60.97,
            "competitor_sales": {
                "CompetitorB": {
                    "original_price": 69.24,
                    "sale_price": 50.55,
                    "discount_percentage": 27,
                },
                "CompetitorC": {
                    "original_price": 49.92,
                    "sale_price": 39.44,
                    "discount_percentage": 21,
                },
            },
            "competitor_a_price": 65.4,
            "competitor_b_price": 50.55,
            "competitor_c_price": 39.44,
        },
        {
            "product": "Product 1",
            "date": "2024-01-13",
            "our_price": 60.97,
            "competitor_sales": {},
            "competitor_a_price": 72.13,
            "competitor_b_price": 57.54,
            "competitor_c_price": 51.1,
        },
        {
            "product": "Product 1",
            "date": "2024-01-14",
            "our_price": 60.97,
            "competitor_sales": {},
            "competitor_a_price": 72.36,
            "competitor_b_price": 70.04,
            "competitor_c_price": 61.04,
        },
        {
            "product": "Product 1",
            "date": "2024-01-15",
            "our_price": 60.97,
            "competitor_sales": {},
            "competitor_a_price": 68.52,
            "competitor_b_price": 59.63,
            "competitor_c_price": 73.03,
        },
        {
            "product": "Product 1",
            "date": "2024-01-16",
            "our_price": 60.97,
            "competitor_sales": {
                "CompetitorA": {
                    "original_price": 53.84,
                    "sale_price": 44.69,
                    "discount_percentage": 17,
                }
            },
            "competitor_a_price": 44.69,
            "competitor_b_price": 57.69,
            "competitor_c_price": 70.51,
        },
        {
            "product": "Product 2",
            "date": "2024-01-10",
            "our_price": 35.34,
            "competitor_sales": {},
            "competitor_a_price": 34.57,
            "competitor_b_price": 42.01,
            "competitor_c_price": 42.02,
        },
        {
            "product": "Product 2",
            "date": "2024-01-11",
            "our_price": 35.34,
            "competitor_sales": {
                "CompetitorB": {
                    "original_price": 40.13,
                    "sale_price": 29.29,
                    "discount_percentage": 27,
                },
                "CompetitorC": {
                    "original_price": 28.93,
                    "sale_price": 22.85,
                    "discount_percentage": 21,
                },
            },
            "competitor_a_price": 37.91,
            "competitor_b_price": 29.29,
            "competitor_c_price": 22.85,
        },
        {
            "product": "Product 2",
            "date": "2024-01-12",
            "our_price": 35.34,
            "competitor_sales": {},
            "competitor_a_price": 41.81,
            "competitor_b_price": 33.35,
            "competitor_c_price": 29.62,
        },
        {
            "product": "Product 2",
            "date": "2024-01-13",
            "our_price": 35.34,
            "competitor_sales": {},
            "competitor_a_price": 41.94,
            "competitor_b_price": 40.6,
            "competitor_c_price": 35.38,
        },
        {
            "product": "Product 2",
            "date": "2024-01-14",
            "our_price": 35.34,
            "competitor_sales": {},
            "competitor_a_price": 39.71,
            "competitor_b_price": 34.56,
            "competitor_c_price": 42.33,
        },
        {
            "product": "Product 2",
            "date": "2024-01-15",
            "our_price": 35.34,
            "competitor_sales": {
                "CompetitorA": {
                    "original_price": 31.21,
                    "sale_price": 25.9,
                    "discount_percentage": 17,
                }
            },
            "competitor_a_price": 25.9,
            "competitor_b_price": 33.44,
            "competitor_c_price": 40.87,
        },
        {
            "product": "Product 2",
            "date": "2024-01-16",
            "our_price": 35.34,
            "competitor_sales": {},
            "competitor_a_price": 33.86,
            "competitor_b_price": 28.92,
            "competitor_c_price": 41.03,
        },
        {
            "product": "Product 3",
            "date": "2024-01-10",
            "our_price": 81.13,
            "competitor_sales": {
                "CompetitorB": {
                    "original_price": 92.14,
                    "sale_price": 67.26,
                    "discount_percentage": 27,
                },
                "CompetitorC": {
                    "original_price": 66.42,
                    "sale_price": 52.47,
                    "discount_percentage": 21,
                },
            },
            "competitor_a_price": 87.02,
            "competitor_b_price": 67.26,
            "competitor_c_price": 52.47,
        },
        {
            "product": "Product 3",
            "date": "2024-01-11",
            "our_price": 81.13,
            "competitor_sales": {},
            "competitor_a_price": 95.98,
            "competitor_b_price": 76.56,
            "competitor_c_price": 68.0,
        },
        {
            "product": "Product 3",
            "date": "2024-01-12",
            "our_price": 81.13,
            "competitor_sales": {},
            "competitor_a_price": 96.29,
            "competitor_b_price": 93.2,
            "competitor_c_price": 81.22,
        },
        {
            "product": "Product 3",
            "date": "2024-01-13",
            "our_price": 81.13,
            "competitor_sales": {},
            "competitor_a_price": 91.17,
            "competitor_b_price": 79.35,
            "competitor_c_price": 97.18,
        },
        {
            "product": "Product 3",
            "date": "2024-01-14",
            "our_price": 81.13,
            "competitor_sales": {
                "CompetitorA": {
                    "original_price": 71.64,
                    "sale_price": 59.46,
                    "discount_percentage": 17,
                }
            },
            "competitor_a_price": 59.46,
            "competitor_b_price": 76.76,
            "competitor_c_price": 93.83,
        },
        {
            "product": "Product 3",
            "date": "2024-01-15",
            "our_price": 81.13,
            "competitor_sales": {},
            "competitor_a_price": 77.73,
            "competitor_b_price": 66.39,
            "competitor_c_price": 94.19,
        },
        {
            "product": "Product 3",
            "date": "2024-01-16",
            "our_price": 81.13,
            "competitor_sales": {
                "CompetitorA": {
                    "original_price": 80.32,
                    "sale_price": 63.45,
                    "discount_percentage": 21,
                }
            },
            "competitor_a_price": 63.45,
            "competitor_b_price": 87.76,
            "competitor_c_price": 81.93,
        },
        {
            "product": "Product 4",
            "date": "2024-01-10",
            "our_price": 48.52,
            "competitor_sales": {},
            "competitor_a_price": 57.4,
            "competitor_b_price": 45.79,
            "competitor_c_price": 40.67,
        },
        {
            "product": "Product 4",
            "date": "2024-01-11",
            "our_price": 48.52,
            "competitor_sales": {},
            "competitor_a_price": 57.59,
            "competitor_b_price": 55.74,
            "competitor_c_price": 48.58,
        },
        {
            "product": "Product 4",
            "date": "2024-01-12",
            "our_price": 48.52,
            "competitor_sales": {},
            "competitor_a_price": 54.52,
            "competitor_b_price": 47.45,
            "competitor_c_price": 58.12,
        },
        {
            "product": "Product 4",
            "date": "2024-01-13",
            "our_price": 48.52,
            "competitor_sales": {
                "CompetitorA": {
                    "original_price": 42.85,
                    "sale_price": 35.57,
                    "discount_percentage": 17,
                }
            },
            "competitor_a_price": 35.57,
            "competitor_b_price": 45.91,
            "competitor_c_price": 56.11,
        },
        {
            "product": "Product 4",
            "date": "2024-01-14",
            "our_price": 48.52,
            "competitor_sales": {},
            "competitor_a_price": 46.49,
            "competitor_b_price": 39.7,
            "competitor_c_price": 56.33,
        },
        {
            "product": "Product 4",
            "date": "2024-01-15",
            "our_price": 48.52,
            "competitor_sales": {
                "CompetitorA": {
                    "original_price": 48.04,
                    "sale_price": 37.95,
                    "discount_percentage": 21,
                }
            },
            "competitor_a_price": 37.95,
            "competitor_b_price": 52.48,
            "competitor_c_price": 49.0,
        },
        {
            "product": "Product 4",
            "date": "2024-01-16",
            "our_price": 48.52,
            "competitor_sales": {
                "CompetitorB": {
                    "original_price": 50.93,
                    "sale_price": 45.84,
                    "discount_percentage": 10,
                },
                "CompetitorC": {
                    "original_price": 51.01,
                    "sale_price": 40.3,
                    "discount_percentage": 21,
                },
            },
            "competitor_a_price": 41.82,
            "competitor_b_price": 45.84,
            "competitor_c_price": 40.3,
        },
        {
            "product": "Product 5",
            "date": "2024-01-10",
            "our_price": 26.95,
            "competitor_sales": {},
            "competitor_a_price": 31.99,
            "competitor_b_price": 30.96,
            "competitor_c_price": 26.98,
        },
        {
            "product": "Product 5",
            "date": "2024-01-11",
            "our_price": 26.95,
            "competitor_sales": {},
            "competitor_a_price": 30.29,
            "competitor_b_price": 26.36,
            "competitor_c_price": 32.28,
        },
        {
            "product": "Product 5",
            "date": "2024-01-12",
            "our_price": 26.95,
            "competitor_sales": {
                "CompetitorA": {
                    "original_price": 23.8,
                    "sale_price": 19.75,
                    "discount_percentage": 17,
                }
            },
            "competitor_a_price": 19.75,
            "competitor_b_price": 25.5,
            "competitor_c_price": 31.17,
        },
        {
            "product": "Product 5",
            "date": "2024-01-13",
            "our_price": 26.95,
            "competitor_sales": {},
            "competitor_a_price": 25.82,
            "competitor_b_price": 22.05,
            "competitor_c_price": 31.29,
        },
        {
            "product": "Product 5",
            "date": "2024-01-14",
            "our_price": 26.95,
            "competitor_sales": {
                "CompetitorA": {
                    "original_price": 26.68,
                    "sale_price": 21.08,
                    "discount_percentage": 21,
                }
            },
            "competitor_a_price": 21.08,
            "competitor_b_price": 29.15,
            "competitor_c_price": 27.21,
        },
        {
            "product": "Product 5",
            "date": "2024-01-15",
            "our_price": 26.95,
            "competitor_sales": {
                "CompetitorB": {
                    "original_price": 28.29,
                    "sale_price": 25.46,
                    "discount_percentage": 10,
                },
                "CompetitorC": {
                    "original_price": 28.33,
                    "sale_price": 22.38,
                    "discount_percentage": 21,
                },
            },
            "competitor_a_price": 23.23,
            "competitor_b_price": 25.46,
            "competitor_c_price": 22.38,
        },
        {
            "product": "Product 5",
            "date": "2024-01-16",
            "our_price": 26.95,
            "competitor_sales": {
                "CompetitorA": {
                    "original_price": 27.28,
                    "sale_price": 24.01,
                    "discount_percentage": 12,
                },
                "CompetitorB": {
                    "original_price": 24.9,
                    "sale_price": 19.42,
                    "discount_percentage": 22,
                },
                "CompetitorC": {
                    "original_price": 30.56,
                    "sale_price": 23.53,
                    "discount_percentage": 23,
                },
            },
            "competitor_a_price": 24.01,
            "competitor_b_price": 19.42,
            "competitor_c_price": 23.53,
        },
    ]