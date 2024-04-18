#import os
from flask import Flask, request, jsonify, render_template
from sql_connection import get_sql_connection
import json

import products_dao
import uom_dao
import order_dao

#template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__))) # Creo direccion absoluta para luego usarlo y acceder a archivos en mi directorio
#template_dir = os.path.join(template_dir, 'ui') # Agrego las dos carpetas que necesito para llegar a mi carpeta de templates

#app = Flask(__name__, template_folder=template_dir) # Inicializo la aplicación de Flask

app = Flask(__name__)

connection = get_sql_connection()

@app.route('/getProducts', methods=['GET'])
def get_products():
    response = products_dao.get_all_products(connection)
    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*') # Header for security measurements, but here we just add it
    
    return response
    #return render_template('index.html', data=response)

@app.route('/getUOM', methods=['GET'])
def get_uom():
    response = jsonify(uom_dao.get_uoms(connection))
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


@app.route('/deleteProduct', methods=['POST'])
def delete_product():
    return_id = products_dao.delete_product(connection, request.form['product_id'])
    response = {
        'product_id': return_id
    }
    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*' )
    
    return response

@app.route('/insertOrder', methods=['POST'])
def insert_order():
    request_payload = json.loads(request.form['data'])
    order_id = order_dao.insert_order(connection, request_payload)
    response = jsonify({
        'order_id': order_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

@app.route('/getAllOrders', methods=['GET'])
def get_all_orders():
    response = jsonify(order_dao.get_all_orders(connection))
    response.headers.add('Access-Control-Allow-Origin', '*')
    
    return response

@app.route('/insertProduct', methods=['POST'])
def insert_product():
    request_payload = json.loads(request.form['data'])
    product_id = products_dao.insert_new_product(connection, request_payload)
    response = jsonify({
        'product_id': product_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

if __name__ == "__main__":
    print("Starting Python Flask Server For Grocery Store App")
    app.run(port=5000)