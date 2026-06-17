"""Advanced syntax: async, decorators, match/case, generators."""

import asyncio
from functools import wraps


def retry(times):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(times):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt == times - 1:
                        raise
        return wrapper
    return decorator


def log_calls(logger):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger.info(f"calling {func.__name__}")
            result = func(*args, **kwargs)
            logger.info(f"called {func.__name__}")
            return result
        return wrapper
    return decorator


async def fetch_user_data(db, user_id):
    async with db.connect() as conn:
        user = await conn.query("SELECT * FROM users WHERE id = ?", user_id)
        orders = await conn.query("SELECT * FROM orders WHERE user_id = ?", user_id)
    return {"user": user, "orders": orders}


async def fetch_product_data(db, product_id):
    async with db.connect() as conn:
        product = await conn.query("SELECT * FROM products WHERE id = ?", product_id)
        reviews = await conn.query("SELECT * FROM reviews WHERE product_id = ?", product_id)
    return {"product": product, "reviews": reviews}


def classify_http(status):
    match status:
        case 200 | 201 | 204:
            return "success"
        case 301 | 302 | 307:
            return "redirect"
        case 400 | 401 | 403 | 404:
            return "client_error"
        case 500 | 502 | 503:
            return "server_error"
        case _:
            return "unknown"


def classify_exit(code):
    match code:
        case 0:
            return "ok"
        case 1 | 2:
            return "error"
        case 130 | 131:
            return "interrupted"
        case _:
            return "unknown"
