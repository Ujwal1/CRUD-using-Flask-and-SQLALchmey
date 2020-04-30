from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy  
from flask_marshmallow import Marshmallow
import os

# from PyQt5.QtCore import *
# from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui, QtWidgets
import sys

# app=QApplication.instance() # checks if QApplication already exists 
# if not app: # create QApplication if it doesnt exist 
#      app = QApplication(sys.argv)
        
#INIT app
app = Flask(__name__)
basedir = os.path.abspath('')
#database
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///' + os.path.join(basedir,'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
#init db 
db = SQLAlchemy(app)
#init ma


ma = Marshmallow(app)

#Product classmodel
class Product(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Integer)
    qty = db.Column(db.Integer)
    
    def __init__(self,name,description,price,qty):
        self.name = name
        self.description= description
        self.price = price
        self.qty = qty
        

# Product schema
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id','name','description','price','qty')
        
#INit schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

#create a product
@app.route('/product',methods=['POST'])
def add_product():
    
    if request.method == 'POST':
        #print('received data: ',request.json)
        content = request.json
        nname = content['name']
        ndescription = content['description']
        nprice = content['price']
        nqty = content['qty']
        new_product = Product(nname,ndescription,nprice,nqty)
        db.session.add(new_product)
        db.session.commit()
        #data = request.data
        data = {'message':'Product Added'}
        response = jsonify(data)
        response.status_code = 202
        return  response
    else:
        data = {'message' : "Error Not Working"}
        response = jsonify(data)
        response.status_code = 406
        return  response

#get all products 
@app.route('/product',methods=['GET'])
def get_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result.data)

#get single products 
@app.route('/product/<id>',methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    return product_schema.jsonify(product)
     
@app.route('/product/<id>',methods=['PUT'])
def update_product(id):
    
    if request.method == 'PUT':
        #print('received data: ',request.json)
        product = Product.query.get(id)
        content = request.json
        nname = content['name']
        ndescription = content['description']
        nprice = content['price']
        nqty = content['qty']
        product.name = nname
        product.description = ndescription
        product.price = nprice
        product.qty = nqty
        db.session.commit()
        #data = request.data
        data = {'message':'Product Added'}
        response = jsonify(data)
        response.status_code = 202
        return  response
    else:
        data = {'message' : "Error Not Working"}
        response = jsonify(data)
        response.status_code = 406
        return  response

#delete  products 
@app.route('/product/<id>',methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    return product_schema.jsonify(product)


#run server 
if __name__ == '__main__':
    app.run(debug=False)

# app=QtGui.QApplication.instance() # checks if QApplication already exists 
# if not app: # create QApplication if it doesnt exist 
#      app = QtGui.QApplication(sys.argv)