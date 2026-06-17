"""Large function clones (30+ lines each) — tests scalability."""

def build_user_profile_csv(users):
    header = "id,name,email,age,country,active"
    rows = [header]
    for user in users:
        status = "yes" if user.active else "no"
        row = f"{user.id},{user.name},{user.email},{user.age},{user.country},{status}"
        rows.append(row)
    for i in range(len(rows)):
        if i > 0:
            rows[i] = rows[i].replace("None", "")
    content = "\n".join(rows)
    with open("users.csv", "w") as f:
        f.write(content)
    print(f"Exported {len(users)} users")
    return len(users)


def build_product_inventory_csv(products):
    header = "sku,name,price,stock,category,discontinued"
    rows = [header]
    for product in products:
        disc = "yes" if product.discontinued else "no"
        row = f"{product.sku},{product.name},{product.price},{product.stock},{product.category},{disc}"
        rows.append(row)
    for i in range(len(rows)):
        if i > 0:
            rows[i] = rows[i].replace("None", "")
    content = "\n".join(rows)
    with open("products.csv", "w") as f:
        f.write(content)
    print(f"Exported {len(products)} products")
    return len(products)
