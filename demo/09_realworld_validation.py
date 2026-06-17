"""Realistic validation logic — common patterns across domains."""

import re


def validate_user_data(data):
    errors = []
    if not data.get("email"):
        errors.append("email is required")
    elif not re.match(r"[^@]+@[^@]+\.[^@]+", data["email"]):
        errors.append("invalid email format")
    if not data.get("name") or len(data["name"]) < 2:
        errors.append("name must be at least 2 characters")
    if data.get("age") is not None:
        if not isinstance(data["age"], int) or data["age"] < 18:
            errors.append("age must be 18 or older")
    if data.get("phone") and not re.match(r"^\+?1?\d{10}$", data["phone"]):
        errors.append("invalid phone number")
    return errors


def validate_product_data(data):
    errors = []
    if not data.get("sku"):
        errors.append("sku is required")
    elif not re.match(r"^[A-Z]{2}-\d{4}$", data["sku"]):
        errors.append("invalid sku format")
    if not data.get("title") or len(data["title"]) < 3:
        errors.append("title must be at least 3 characters")
    if data.get("price") is not None:
        if not isinstance(data["price"], (int, float)) or data["price"] <= 0:
            errors.append("price must be positive")
    if data.get("upc") and not re.match(r"^\d{12}$", data["upc"]):
        errors.append("invalid upc format")
    return errors
