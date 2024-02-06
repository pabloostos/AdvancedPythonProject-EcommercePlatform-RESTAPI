# ========================================================================================================================
# Advanced Programming in Python: Group Assignment: Group 5
# Team members: Felipe Fischel, Ayça Basaran, Federico Barca, Luca Conti, Pablo Ostos
# ========================================================================================================================

# Import neccessary libraries
from flask import Flask, jsonify, request
from sqlalchemy import create_engine, text
from sqlalchemy.engine.row import RowMapping
from sqlalchemy.exc import SQLAlchemyError

# Start app with Flask from flask library
app = Flask(__name__)
# Creating engine to access the "store.db" database 
engine = create_engine("sqlite:///store.db")

# We create a function to execute the query and return a JSON response
# as this is used in all exercies.

def execute_query(query):
    try:
        with engine.connect() as conn:
            result = conn.execute(query)

            # For INSERT queries, return json with status code 201
            if result.rowcount > 0:
                success_message = {"Success": "Query executed successfully"}
                return jsonify(success_message), 201

            # For SELECT queries, return json with status code 200
            result = result.mappings().all()
            if result:
                return jsonify([dict(row) for row in result]), 200

            # In case the result doesn't exist
            error_message = {"Error": "No results found"}
            return jsonify(error_message), 404

    except Exception as e:
        # In case there's an error with the Query
        error_message = {"Error": str(e)}
        return jsonify(error_message), 500

# ========================================================================================================================
# EXERCISE 1: Create an endpoint in the API (api.py) to list all warehouses. 
# ========================================================================================================================
@app.route("/api/warehouses", methods=["GET"])
def get_warehouses():
    # Query: returning all warehouses
    all_warehouses_query = text("""
        SELECT * 
        FROM warehouses;
        """)
        
    result = execute_query(all_warehouses_query)
    return result

# ========================================================================================================================
# EXERCISE 2: Create an endpoint in the API to show the stock of all products in a particular warehouse.
# ========================================================================================================================
@app.route("/api/stock/warehouse/<int:warehouse_id>", methods=["GET"])
def get_stock_in_warehouse(warehouse_id):
    # Query: returning stock information for a particular warehouse
    stock_query = text(f"""
        SELECT * 
        FROM stock 
        WHERE warehouse_id = {warehouse_id};
        """)
    
    result = execute_query(stock_query)
    return result

# ========================================================================================================================
# EXERCISE 3: Create an endpoint in the API to show the stock of one particular products in a particular warehouse.
# ========================================================================================================================
@app.route("/api/stock/warehouse/<int:warehouse_id>/product/<int:product_id>", methods=["GET"])
def get_warehouse_products(warehouse_id, product_id):
    # Query: returning stock information for a particular product in a particular warehouse
    get_warehouse_products_query = text(f"""
        SELECT * 
        FROM stock 
        WHERE warehouse_id = {warehouse_id} 
        AND product_id = {product_id};""")
    
    result = execute_query(get_warehouse_products_query)
    return result

# ========================================================================================================================
# EXERCISE 4: Create an endpoint in the API to create a sale.
# ========================================================================================================================
@app.route("/api/create-sale", methods=["POST"])
def create_sale():
    # Fetching sale information from client
    sale = request.get_json()

    # Query: inserting sale information into sales table
    sales_query = text(f"""
        INSERT INTO sales (product_id)
        VALUES ({sale["product_id"]});
        """)
    
    result = execute_query(sales_query)
    return result

# ========================================================================================================================
# EXERCISE 5: Create an endpoint in the API to list all products.
# ========================================================================================================================
@app.route("/api/products", methods = ["GET"])
def get_products(): 
    # Query: returning all information in products table    
    all_products_query = text(f"""
        SELECT * 
        from products;
        """)

    result = execute_query(all_products_query)
    return result

# ========================================================================================================================
# EXERCISE 6: Create an endpoint in the API to return all sales by a particular product.
# This returns a JSON object with the following keys: 'id', 'name', 'price', 'total_sales', 'gross_sales'. 
# ========================================================================================================================
@app.route("/api/sales/product/<int:product_id>", methods=["GET"])
def get_sales_product(product_id):
    # Query: joins tables 'products' and 'sales' and returns fields: 'product_id', 'name', 'price', 'COUNT(product_id)', 'SUM(price)'
    query = text(f"""
        SELECT product_id, name, price, COUNT(product_id), SUM(price)  
        FROM sales s
        INNER JOIN products p on s.product_id = p.id
        WHERE product_id = {product_id};
        """)
    
    # Connecting to database and executing query 
    with engine.connect() as conn:
        result = conn.execute(query).mappings().all()

        # Cleaning data to obtain the desired structure
        json_momoa = {
            "id": result[0]["product_id"],
            "name": result[0]["name"],
            "price": result[0]["price"],
            "total_sales": result[0]["COUNT(product_id)"],
            "gross_sales": result[0]["SUM(price)"]
        }

        return jsonify(json_momoa), 200


# ========================================================================================================================
# EXTRA: Create an endpoint in the API to create a product. 
# ========================================================================================================================
@app.route("/api/create-product", methods=["POST"])
def create_product():
    # Fetching new product information form user 
    new_product = request.get_json()
    # Query: inserting product information into products table
    query = text(f"""INSERT INTO products (name, price)
                     VALUES ("{new_product["name"]}", {new_product["price"]});""")
                     
    # Connecting to database and executing query                  
    with engine.connect() as conn:
        conn.execute(query)
        return "Product created", 201

app.run(debug=True, port=8080)
