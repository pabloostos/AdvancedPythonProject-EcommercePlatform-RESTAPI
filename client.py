# Exercise 7: Create a function in client.py for each one of the previous exercises, calling the respective endpoint in the REST API.
#%%
import requests

# EXERCISE 1: list all warehouses.
def exercise_1():
    warehouses = requests.get("http://localhost:8080/api/warehouses").json()

    for warehouse in warehouses: 
        print(f"""
        id: {warehouse["id"]}
        location: {warehouse["location"]}
        """)

# EXERCISE 2: show the stock of all products in a particular warehouse.
def exercise_2(warehouse_id):

    stock_warehouse = requests.get(f"http://localhost:8080/api/stock/warehouse/{warehouse_id}").json()

    for stock in stock_warehouse: 
        print(f"""
        product_id: {stock["product_id"]}
        quantity: {stock["quantity"]}
        warehouse_id: {stock['warehouse_id']}
        """)

# EXERCISE 3: show the stock of one particular products in a particular warehouse.
def exercise_3(warehouse_id, product_id):

    stock_product_warehouse = requests.get(f"http://localhost:8080/api/stock/warehouse/{warehouse_id}/product/{product_id}").json()

    print(f"""
    product_id:{stock_product_warehouse[0]["product_id"]}
    quantity: {stock_product_warehouse[0]["quantity"]}
    warehouse_id: {stock_product_warehouse[0]['warehouse_id']}
    """)

# EXERCISE 4: creates a sale.
def exercise_4(sale):
    new_sale = requests.post("http://localhost:8080/api/create-sale", json = sale)

    if new_sale.status_code == 201:
        print("Sale created!")
    else: 
        print("Not possible to create sale!")
    
# EXERCISE 5: list all products.
def exercise_5():
    products = requests.get("http://localhost:8080/api/products").json()

    for product in products: 
        print(f"""
        id: {product["id"]}
        name: {product["name"]}
        price: {product['price']}
        """)

# EXERCISE 6: return all sales by a particular product.
# This returns a JSON object with the following keys: 'id', 'name', 'price', 'total_sales', 'gross_sales'. 
def exercise_6(product_id):

    product_sales = requests.get(f"http://localhost:8080/api/sales/product/{product_id}").json()

    print(f"""
    id: {product_sales["id"]}
    name: {product_sales["name"]}
    price: {product_sales['price']}
    gross_sales: {product_sales['gross_sales']}
    total_sales: {product_sales['total_sales']}
    """)


# EXTRA ;)
def extra():
    product = {
        'name' : 'crocs coolest shoes in the world',
        'price' : 89.99
    }

    new_product = requests.post("http://localhost:8080/api/create-product", json = product)

    if new_product.status_code == 201:
        print(new_product.text)
    else: 
        print("Not possible to create sale")

# ========================================================================================================================
# ========================================================================================================================

#%% Running exercise 1: 
# ========================================================================================================================
exercise_1()

#%% Running exercise 2: 
# ========================================================================================================================

warehouse_id = 2
exercise_2(warehouse_id)

#%% Running exercise 3:
# # ======================================================================================================================== 
warehouse_id = 2
product_id = 4

exercise_3(warehouse_id, product_id)

#%% Running exercise 4: 
# ========================================================================================================================
sale = {
    'product_id': 4
}

exercise_4(sale)

#%% Running exercise 5: 
# ========================================================================================================================
exercise_5()

#%% Running exercise 6: 
# ========================================================================================================================
product_id = 4

exercise_6(product_id)

# %%
