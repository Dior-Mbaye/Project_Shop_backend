from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
from flask_marshmallow import Marshmallow
import os

#init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

#Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Init db
db = SQLAlchemy(app)

#Init ma
ma = Marshmallow(app)

#Class Vente ------------------------------------------------------------------------
#Vente Class/Model
class Vente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom_vente = db.Column(db.String(20))
    id_vet = db.Column(db.Integer, db.ForeignKey('vetement.id'),nullable=False)
    
    def __init__(self,nom_vente,id_vet):
        self.nom_vente = nom_vente
        self.id_vet = id_vet

# Vente
class venteSchema(ma.Schema):
    class Meta :
        fields = ('id', 'nom_vente','id_vet')

#Init schema
vente_schema = venteSchema()
ventes_schema = venteSchema(many=True )

#Create Vente
@app.route('/vente',methods=['POST'])
def add_vente():
    nom_vente = request.json['nom_vente']
    id_vet = request.json['id_vet']
    new_vente = Vente(nom_vente,id_vet)
    db.session.add(new_vente)
    db.session.commit()
    return vente_schema.jsonify(new_vente)

#Get all Ventes
@app.route('/vente',methods=['GET'])
def get_ventes():
    all_ventes = Vente.query.all()
    result = ventes_schema.dump(all_ventes)
    return jsonify(result)

#Get single vente
@app.route('/vente/<id>',methods=['GET'])
def get_vente(id):
    vente = Vente.query.get(id)
    return vente_schema.jsonify(vente)

#Update Vente
@app.route('/vente/<id>',methods=['PUT'])
def update_vente(id):
    vente = Vente.query.get(id)
    nom_vente = request.json['nom_vente']
    id_vet = request.json['id_vet']

    vente.nom_vente = nom_vente
    vente.id_vet = id_vet
    db.session.commit()
    return vente_schema.jsonify(vente)

#Delete vente
@app.route('/vente/<id>',methods=['DELETE'])
def delete_vente(id):
    vente = Vente.query.get(id)
    db.session.delete(vente)
    db.session.commit()
    return vente_schema.jsonify(vente)

#Class Vetement --------------------------------------------------------------------------
#Vetement Class/Model
class Vetement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20))
    description = db.Column(db.String(100))
    price = db.Column(db.Integer)
    color = db.Column(db.String(10))
    nbre = db.Column(db.Integer)
    id_cat = db.Column(db.Integer, db.ForeignKey('categorie.id'),nullable=False)
    ventes = db.relationship('Vente', lazy='select',backref=db.backref('vente', lazy='joined'))

    def __init__(self,title,description,price,color,nbre,id_cat):
        self.title = title
        self.description = description
        self.price = price
        self.color = color
        self.nbre = nbre
        self.id_cat = id_cat

# Vetement
class vetementSchema(ma.Schema):
    class Meta :
        fields = ('id', 'title', 'description', 'price', 'color','nbre','id_cat')

#Init schema
vetement_schema = vetementSchema()
vetements_schema = vetementSchema(many=True )

#Create Vetement
@app.route('/vetement',methods=['POST'])
def add_vetement():
    title = request.json['title']
    description = request.json['description']
    price = request.json['price']
    color = request.json['color']
    nbre = request.json['nbre']
    id_cat = request.json['id_cat']
    new_vetement = Vetement(title,description,price,color,nbre,id_cat)
    db.session.add(new_vetement)
    db.session.commit()
    return vetement_schema.jsonify(new_vetement)

#Get all vetements
@app.route('/vetement',methods=['GET'])
def get_vetements():

    #vetementList = Vetement.query.join(Categorie, Vetement.id_cat==Categorie.id).add_columns(Vetement.id, Categorie.nom_cat,Vetement.title, Categorie.id, Vetement.categorie)
    #vetementList = Vetement.query.join(Categorie, Vetement.id_cat == Categorie.id).all()
    all_vetements = Vetement.query.all()
    result = vetements_schema.dump(all_vetements)
    return jsonify(result)

#Get single vetement
@app.route('/vetement/<id>',methods=['GET'])
def get_vetement(id):
    vetement = Vetement.query.get(id)
    return vetement_schema.jsonify(vetement)

#Update Vetement
@app.route('/vetement/<id>',methods=['PUT'])
def update_vetement(id):
    vetement = Vetement.query.get(id)
    title = request.json['title']
    description = request.json['description']
    price = request.json['price']
    color = request.json['color']
    nbre = request.json['nbre']
    id_cat = request.json['id_cat']

    vetement.title = title
    vetement.description = description
    vetement.price = price
    vetement.color = color
    vetement.nbre = nbre
    vetement.id_cat = id_cat
    db.session.commit()
    return vetement_schema.jsonify(vetement)

#Delete vetement
@app.route('/vetement/<id>',methods=['DELETE'])
def delete_vetement(id):
    vetement = Vetement.query.get(id)
    db.session.delete(vetement)
    db.session.commit()
    return vetement_schema.jsonify(vetement)

#Class Catégories ------------------------------------------------------------------------
#Catégories Class/Model
class Categorie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom_cat = db.Column(db.String(20))
    id_profil = db.Column(db.Integer, db.ForeignKey('profil.id'),nullable=False)
    vetements = db.relationship('Vetement', lazy='select',backref=db.backref('categorie', lazy='joined'))

    def __init__(self,nom_cat,id_profil):
        self.nom_cat = nom_cat
        self.id_profil = id_profil

# Catégorie
class categorieSchema(ma.Schema):
    class Meta :
        fields = ('id', 'nom_cat','id_profil')

#Init schema
categorie_schema = categorieSchema()
categories_schema = categorieSchema(many=True )

#Create Catégorie
@app.route('/categorie',methods=['POST'])
def add_categorie():
    nom_cat = request.json['nom_cat']
    id_profil = request.json['id_profil']
    new_categorie = Categorie(nom_cat,id_profil)
    db.session.add(new_categorie)
    db.session.commit()
    return categorie_schema.jsonify(new_categorie)

#Get all Categories
@app.route('/categorie',methods=['GET'])
def get_categories():
    all_categories = Categorie.query.all()
    result = categories_schema.dump(all_categories)
    return jsonify(result)

#Get single categorie
@app.route('/categorie/<id>',methods=['GET'])
def get_categorie(id):
    categorie = Categorie.query.get(id)
    return categorie_schema.jsonify(categorie)

#Update Categorie
@app.route('/categorie/<id>',methods=['PUT'])
def update_categorie(id):
    categorie = Categorie.query.get(id)
    nom_cat = request.json['nom_cat']
    id_profil = request.json['id_profil']

    categorie.nom_cat = nom_cat
    categorie.id_profil = id_profil
    db.session.commit()
    return categorie_schema.jsonify(categorie)

#Delete categorie
@app.route('/categorie/<id>',methods=['DELETE'])
def delete_categorie(id):
    categorie = Categorie.query.get(id)
    db.session.delete(categorie)
    db.session.commit()
    return categorie_schema.jsonify(categorie)

#Class Profil ------------------------------------------------------------------------
#Profil Class/Model
class Profil(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom_profil = db.Column(db.String(20))
    categories = db.relationship('Categorie', lazy='select',backref=db.backref('profil', lazy='joined'))

    def __init__(self,nom_profil):
        self.nom_profil = nom_profil

# Profil
class profilSchema(ma.Schema):
    class Meta :
        fields = ('id', 'nom_profil')

#Init schema
profil_schema = profilSchema()
profils_schema = profilSchema(many=True )

#Create Profil
@app.route('/profil',methods=['POST'])
def add_profil():
    nom_profil = request.json['nom_profil']
    new_profil = Profil(nom_profil)
    db.session.add(new_profil)
    db.session.commit()
    return profil_schema.jsonify(new_profil)

#Get all Profil
@app.route('/profil',methods=['GET'])
def get_profils():
    all_profils = Profil.query.all()
    result = profils_schema.dump(all_profils)
    return jsonify(result)

#Get single profil
@app.route('/profil/<id>',methods=['GET'])
def get_profil(id):
    profil = Profil.query.get(id)
    return profil_schema.jsonify(profil)

#Update Profil
@app.route('/profil/<id>',methods=['PUT'])
def update_profil(id):
    profil = Profil.query.get(id)
    nom_profil = request.json['nom_profil']

    profil.nom_profil = nom_profil
    db.session.commit()
    return profil_schema.jsonify(profil)

#Delete profil
@app.route('/profil/<id>',methods=['DELETE'])
def delete_profil(id):
    profil = Profil.query.get(id)
    db.session.delete(profil)
    db.session.commit()
    return profil_schema.jsonify(profil)

if __name__ =='__main__':
    app.run(debug=True)
