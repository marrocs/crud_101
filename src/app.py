"""TODO: usar um unico idioma"""

from flask import Flask, render_template, request, jsonify
import os, re, datetime
from config import db
from flask_sqlalchemy import SQLAlchemy
from config.classes import *


app = Flask(__name__)


if not os.path.isfile('../config/database.db'):
    db.connect()


def isValidMail(email):
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9]+(\.[A-Z|a-z]{2,})+')

    if re.fullmatch(regex,email):
        return True
    else:
        return False

@app.route("/")
def hello_world():
    return "<p>Home</p>"


# --- Routes and methods to alterate INVENTORY ---
@app.route("/inventory", methods=['POST']) # OK
def post_order():
    req_data = request.get_json()
    email = req_data['email']

    if not isValidMail(email):
        return jsonify({
            'status': '422',
            'res': 'failure',
            'error': 'Invalid email format'
        })
    
    name = req_data['name']
    quantity = req_data['quantity']
    inventory = [i.serialize() for i in db.view_inventory()]

    # Caso produto ja exista em estoque. Atualiza quantidade
    for i in inventory:
        if i['name'] == name:
            product = Product(
                i['id'],
                i['name'], 
                quantity
                )
            print('Product updated: ', product.serialize())
            db.update_product(product)
            new_products = [p.serialize() for p in db.view_inventory()]
            print('products in inventory: ', new_products)
            
            return jsonify({
                'res': product.serialize(),
                'status': '200',
                'msg': f'Success updating the product named {name}'
            })
            
        
    product = Product(db.getNewId(), name, req_data['quantity'])
    db.insert_product(product)
    print('New product added: ', product.serialize())

    return jsonify({
        'res': product.serialize(),
        'status': '200',
        'msg': 'Success creating a new book!'
    })


@app.route("/inventory", methods=['GET']) # OK
def get_inventory():
    content_type = request.headers.get('Content-Type')
    products = [p.serialize() for p in db.view_inventory()]

    if (content_type == 'application/json'):
        json = request.json
        print(json)
        for p in products:
            if p['id'] == int(json['id']):
                return jsonify({
                    'res': p,
                    'status': '200',
                    'msg': 'Success getting all products from inventory'
                })
        return jsonify({
            'error': f'Error. Product with id "{json["id"]}" not found',
            'res': '',
            'status': '404'
            })
    else:
        return jsonify({
            'res': products,
            'status': '200',
            'msg': 'Sucess getting all products from inventory.',
            'number_of_products': len(products)
             })


@app.route("/inventory/<id>", methods=['GET']) # OK
def get_product_by_id(id):
    req_args = request.view_args
    inventory = [p.serialize() for p in db.view_inventory()]

    if req_args:
        for p in inventory:
            if p['id'] == int(req_args['id']):
                return jsonify({
                    'res': p,
                    'status': '200',
                    'msg': 'Success getting book by ID'
                })
        return jsonify({
            'error': f"Error. Product with id '{req_args['id']}' was not found",
            'res': '',
            'status': '404'
        })
    else:
        return jsonify({
            'res': inventory,
            'status': '200',
            'msg': 'Success getting product by ID',
            'number_of_products': len(inventory)
        })


@app.route("/inventory", methods=['PUT']) # OK
def put_product():
    req_data = request.get_json()
    name = req_data['name']
    quantity = req_data['quantity']
    the_id = req_data['id']
    
    products = [p.serialize() for p in db.view_inventory()]

    for p in products:
        if p['id'] == the_id:
            product = Product(
                the_id, 
                name, 
                quantity
                )
            print('Product updated: ', product.serialize())
            db.update_product(product)
            new_products = [p.serialize() for p in db.view_inventory()]
            print('products in inventory: ', new_products)
            return jsonify({
                'res': product.serialize(),
                'status': '200',
                'msg': f'Success updating the product named {name}'
            })
    return jsonify({
        'res': f'Error. Failed to update Product named {name}',
        'status': '404'
    })


@app.route("/inventory", methods=['DELETE']) # OK
def delete_all_products():
    req_data = request.get_json()
    email = req_data['email']

    if not isValidMail(email):
        return jsonify({
            'status': '422',
                'res': 'failure',
                'error': 'Invalid email format'
        })
    
    db.delete_all_products()
    print(f'All products deleted by {email}')

    return jsonify({
        'res': 'All products has been deleted',
        'status': '200'
    })


@app.route("/inventory/<id>", methods=['DELETE']) # OK
def delete_order_by_id(id):
    req_args = request.view_args
    print('req_args:', req_args)
    products = [p.serialize() for p in db.view_inventory()]
    if req_args:
        for p in products:
            if p['id'] == int(req_args['id']):
                db.delete_product(p['id'])
                updated_orders = [p.serialize() for p in db.view_inventory()]
                print('update_products: ', updated_orders)
                
                return jsonify({
                    "res": updated_orders,
                    "number_of_products": len(updated_orders)
                    })
    else:
        return jsonify({
            "error": f"Error. No book ID was sent",
            "res": "",
            "status": "404"
            })


# --- Routes and methods to alterate CLIENT ---
@app.route("/clients", methods=['POST']) # OK
def post_client():
    req_data = request.get_json()
    email = req_data['email']

    if not isValidMail(email):
        return jsonify({
            'status': '422',
            'res': 'failure',
            'error': 'Invalid email format'
        })
    
    id = req_data['id']
    name = req_data['name']
    client = [i.serialize() for i in db.view_clients()]

    # Caso cliente ja exista no BD. Atualiza nome
    for i in client:
        if i['id'] == id:
            client = Client(
                i['id'],
                name
                )
            print('Client updated: ', client.serialize())
            db.update_client(client)
            new_clients = [c.serialize() for c in db.view_clients()]
            print('Clients in DB: ', new_clients)
            
            return jsonify({
                'res': client.serialize(),
                'status': '200',
                'msg': f'Success updating the client named {name}'
            })
            
        
    client = Client(db.getNewId(), name)
    db.insert_client(client)
    print('New client added: ', client.serialize())

    return jsonify({
        'res': client.serialize(),
        'status': '200',
        'msg': 'Success registering a new client!'
    })


@app.route("/clients", methods=['GET']) # OK
def get_clients():
    content_type = request.headers.get('Content-Type')
    clients = [c.serialize() for c in db.view_clients()]

    if (content_type == 'application/json'):
        json = request.json
        print(json)
        for c in clients:
            if c['id'] == int(json['id']):
                return jsonify({
                    'res': c,
                    'status': '200',
                    'msg': 'Success getting all clients from client'
                })
        return jsonify({
            'error': f'Error. Client with id "{json["id"]}" not found',
            'res': '',
            'status': '404'
            })
    else:
        return jsonify({
            'res': clients,
            'status': '200',
            'msg': 'Sucess getting all clients from client.',
            'number_of_clients': len(clients)
             })


@app.route("/clients/<id>", methods=['GET']) # OK
def get_client_by_id(id):
    req_args = request.view_args
    client = [c.serialize() for c in db.view_clients()]

    if req_args:
        for c in client:
            if c['id'] == int(req_args['id']):
                return jsonify({
                    'res': c,
                    'status': '200',
                    'msg': 'Success getting client by ID'
                })
            
        return jsonify({
            'error': f"Error. Client with id '{req_args['id']}' was not found",
            'res': '',
            'status': '404'
        })
    else:
        return jsonify({
            'res': client,
            'status': '200',
            'msg': 'Success getting client by ID',
            'number_of_clients': len(client)
        })


@app.route("/clients", methods=['PUT']) # acho que aqui vai dar ruim
def put_client():
    req_data = request.get_json()
    name = req_data['name']
    the_id = req_data['id']
    
    clients = [c.serialize() for c in db.view_clients()]

    for c in clients:
        if c['id'] == the_id:
            client = Client(
                the_id, 
                name, 
                )
            print('Client updated: ', client.serialize())
            db.update_product(client)
            new_products = [c.serialize() for c in db.view_clients()]
            print('clients in client: ', new_products)
            return jsonify({
                'res': client.serialize(),
                'status': '200',
                'msg': f'Success updating the client named {name}'
            })
    return jsonify({
        'res': f'Error. Failed to update Client named {name}',
        'status': '404'
    })


@app.route("/clients", methods=['DELETE']) # OK
def delete_all_clients():
    req_data = request.get_json()
    email = req_data['email']

    if not isValidMail(email):
        return jsonify({
            'status': '422',
                'res': 'failure',
                'error': 'Invalid email format'
        })
    
    db.delete_all_clients()
    print(f'All clients deleted by {email}')

    return jsonify({
        'res': 'All clients has been deleted',
        'status': '200'
    })


@app.route("/clients/<id>", methods=['DELETE']) # OK
def delete_order_by_id(id):
    req_args = request.view_args
    print('req_args:', req_args)
    clients = [c.serialize() for c in db.view_clients()]
    if req_args:
        for c in clients:
            if c['id'] == int(req_args['id']):
                db.delete_client(c['id'])
                updated_clients = [c.serialize() for c in db.view_clients()]
                print('update_clients: ', updated_clients)
                
                return jsonify({
                    "res": updated_clients,
                    "number_of_clients": len(updated_clients)
                    })
    else:
        return jsonify({
            "error": f"Error. No client ID was sent",
            "res": "",
            "status": "404"
            })



# --- Routes and methods to alterate ORDER ---
@app.route("/orders", methods=['POST']) # OK
def post_order():
    req_data = request.get_json()
    email = req_data['email']

    if not isValidMail(email):
        return jsonify({
            'status': '422',
            'res': 'failure',
            'error': 'Invalid email format'
        })
    
    client_id = req_data['client_id']
    items = req_data['items']
    order = [i.serialize() for i in db.view_orders()]

    # Caso produto ja exista em estoque. Atualiza quantidade
    for i in order:
        if i['client_id'] == client_id:
            order = Order(
                i['id'],
                i['client_id'], 
                items
                )
            print('Order updated: ', order.serialize())
            db.update_product(order)
            new_products = [p.serialize() for p in db.view_orders()]
            print('orders in order: ', new_products)
            
            return jsonify({
                'res': order.serialize(),
                'status': '200',
                'msg': f'Success updating the order named {client_id}'
            })
            
        
    order = Order(db.getNewId(), client_id, req_data['items'])
    db.insert_product(order)
    print('New order added: ', order.serialize())

    return jsonify({
        'res': order.serialize(),
        'status': '200',
        'msg': 'Success creating a new order!'
    })


@app.route("/orders", methods=['GET']) # OK
def get_orders():
    content_type = request.headers.get('Content-Type')
    orders = [p.serialize() for p in db.view_orders()]

    if (content_type == 'application/json'):
        json = request.json
        print(json)
        for p in orders:
            if p['id'] == int(json['id']):
                return jsonify({
                    'res': p,
                    'status': '200',
                    'msg': 'Success getting all orders from order'
                })
        return jsonify({
            'error': f'Error. Order with id "{json["id"]}" not found',
            'res': '',
            'status': '404'
            })
    else:
        return jsonify({
            'res': orders,
            'status': '200',
            'msg': 'Sucess getting all orders from order.',
            'number_of_products': len(orders)
             })


@app.route("/orders/<id>", methods=['GET']) # OK
def get_order_by_id(id):
    req_args = request.view_args
    order = [p.serialize() for p in db.view_orders()]

    if req_args:
        for p in order:
            if p['id'] == int(req_args['id']):
                return jsonify({
                    'res': p,
                    'status': '200',
                    'msg': 'Success getting book by ID'
                })
        return jsonify({
            'error': f"Error. Order with id '{req_args['id']}' was not found",
            'res': '',
            'status': '404'
        })
    else:
        return jsonify({
            'res': order,
            'status': '200',
            'msg': 'Success getting order by ID',
            'number_of_products': len(order)
        })


@app.route("/orders", methods=['PUT']) # OK
def put_order():
    req_data = request.get_json()
    client_id = req_data['client_id']
    items = req_data['items']
    the_id = req_data['id']
    
    orders = [p.serialize() for p in db.view_orders()]

    for p in orders:
        if p['id'] == the_id:
            order = Order(
                the_id, 
                client_id, 
                items
                )
            print('Order updated: ', order.serialize())
            db.update_product(order)
            new_products = [p.serialize() for p in db.view_orders()]
            print('orders in order: ', new_products)
            return jsonify({
                'res': order.serialize(),
                'status': '200',
                'msg': f'Success updating the order named {client_id}'
            })
    return jsonify({
        'res': f'Error. Failed to update Order named {client_id}',
        'status': '404'
    })


@app.route("/orders", methods=['DELETE']) # OK
def delete_all_orders():
    req_data = request.get_json()
    email = req_data['email']

    if not isValidMail(email):
        return jsonify({
            'status': '422',
                'res': 'failure',
                'error': 'Invalid email format'
        })
    
    db.delete_all_products()
    print(f'All orders deleted by {email}')

    return jsonify({
        'res': 'All orders has been deleted',
        'status': '200'
    })


@app.route("/orders/<id>", methods=['DELETE']) # OK
def delete_order_by_id(id):
    req_args = request.view_args
    print('req_args:', req_args)
    orders = [p.serialize() for p in db.view_orders()]
    if req_args:
        for p in orders:
            if p['id'] == int(req_args['id']):
                db.delete_order(p['id'])
                updated_orders = [p.serialize() for p in db.view_orders()]
                print('update_orders: ', updated_orders)
                
                return jsonify({
                    "res": updated_orders,
                    "number_of_products": len(updated_orders)
                    })
    else:
        return jsonify({
            "error": f"Error. No book ID was sent",
            "res": "",
            "status": "404"
            })


if __name__ == '__main__':
    app.run(debug=True)