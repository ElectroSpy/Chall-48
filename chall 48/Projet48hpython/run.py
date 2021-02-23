import os
from sys import stderr

from flask import Flask, render_template, request, url_for, redirect
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from dotenv import load_dotenv



app = Flask(__name__)

load_dotenv()
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
print(os.getenv("MONGO_URI"), file=stderr)
mongo = PyMongo(app)

passionfroid = mongo.db.passionfroid

@app.route('/', methods=['GET', 'POST'])
def index():
    type = passionfroid.find().distinct('type')
    tag = passionfroid.find().distinct('tag')
    if request.method == "POST":
        selected_type = request.form.getlist("type")
        selected_tag = request.form.getlist("tag")
        recherche = request.form.get("recherche")
        if recherche:
            recherche = str.capitalize(recherche)
            passionfroids = passionfroid.find({"nom": {"$regex": recherche}})
        elif not selected_tag and not selected_type and not recherche:
            passionfroids = passionfroid.find().sort("nom", 1)
        elif not selected_tag:
            passionfroids = passionfroid.find(
                {"type": {"$in": selected_type}}
            ).sort("nom", 1)
        elif not selected_type:
            passionfroids = passionfroid.find(
                {"tag": {"$in": selected_tag}}
            ).sort("nom", 1)
        else:
            passionfroids = passionfroid.find(
                {"$and": [
                    {"type": {"$in": selected_type}},
                    {"tag": {"$in": selected_tag}},
                ]}
            ).sort("nom", 1)
        countProduits = passionfroids.count()
        return render_template('index.html', passionfroids=passionfroids, type=type, tag=tag, countProduits=countProduits)
    else:
        passionfroids = passionfroid.find().sort("nom", 1)
        countProduits = passionfroids.count()
        return render_template('index.html', passionfroids=passionfroids, type=type, tag=tag, countProduits=countProduits)


@app.route('/detail/<id>', methods=['GET'])
def detail(id):
    solo_passionfroid = passionfroid.find_one({'_id': ObjectId(id)})
    return render_template('detail.html', solo_passionfroid=solo_passionfroid)


@app.route('/add_Produits', methods=['GET'])
def page_add_Produits():
    return render_template('add_Produits.html')

@app.route('/add', methods=['POST'])
def add_Produits():
    nom = request.form.get('nom')
    type = request.form.get('type')
    tag = request.form.get('tag')
    image = request.form.getlist('image[]')
    passionfroid.insert_one({'nom': nom,'type': type, 'tag': tag,'image': image,})
    return redirect(url_for('index'))


@app.route('/passionfroid_delete/<id>', methods=['POST'])
def delete_Produits(id):
    passionfroid.delete_one({'_id': ObjectId(id)})
    return redirect(url_for('index'))


@app.route('/passionfroid/<id>/add_image', methods=['POST'])
def add_image_Produits(id):
    solo_passionfroid = passionfroid.find_one({'_id': ObjectId(id)})
    solo_passionfroid['image'].append(request.form.get('image[]'))
    passionfroid.replace_one({'_id': ObjectId(id)}, solo_passionfroid)
    return redirect(url_for('detail', id=id))

@app.route('/passionfroid/<id>/delete_image', methods=['POST'])
def delete_image_Produits(id):
    image = request.form.getlist('image[]')
    passionfroid.delete_one({'image': image})
    return redirect(url_for('detail', id=id))



@app.route('/passionfroid_update/<id>', methods=['POST'])
def update_Produits(id):
    nom = request.form.get('nom')
    type = request.form.get('type')
    tag = request.form.get('tag')
    image = request.form.getlist('image[]')

    updated_passionfroid = passionfroid.find_one({'_id': ObjectId(id)})

    updated_passionfroid["nom"] = nom

    updated_passionfroid["type"] = type
    updated_passionfroid["tag"] = tag
    updated_passionfroid["image"] = image

    passionfroid.replace_one({'_id': ObjectId(id)}, updated_passionfroid)
    return redirect(url_for('detail', id=id))


@app.route('/testmoche', methods=['GET'])
def index_test():
    passionfroids = passionfroid.find()
    return render_template('index_test.html', passionfroids=passionfroids)


@app.route('/passionfroid/<id>', methods=['GET'])
def detail_Produits_test(id):
    solo_passionfroid = passionfroid.find_one({'_id': ObjectId(id)})
    return render_template('detail_test.html', solo_passionfroid=solo_passionfroid)

@app.route('/style/<type>', methods=['GET'])
def type_Produits(type):
    typeFiltre = passionfroid.find().distinct('type')
    tag = passionfroid.find().distinct('tag')
    passionfroids = passionfroid.find({'type': type}).sort("nom", 1)
    countProduits = passionfroids.count()
    return render_template("index.html", passionfroids=passionfroids, type=typeFiltre, tag=tag, countProduits=countProduits)

@app.route('/style/<type>/desc', methods=['GET'])
def type_Produits_desc(type):
    typeFiltre = passionfroid.find().distinct('type')
    tag = passionfroid.find().distinct('tag')
    passionfroids = passionfroid.find({'type': type}).sort("nom", -1)
    countProduits = passionfroids.count()
    return render_template("index.html", passionfroids=passionfroids, type=typeFiltre, tag=tag, countProduits=countProduits)

@app.route('/tag/<tag>', methods=['GET'])
def tag_Produits(tag):
    typeFiltre = passionfroid.find().distinct('type')
    tagFiltre = passionfroid.find().distinct('tag')
    passionfroids = passionfroid.find({'tag': tag}).sort("nom", 1)
    countProduits = passionfroids.count()
    return render_template("index.html", passionfroids=passionfroids, type=typeFiltre, tag=tagFiltre, countProduits=countProduits)

@app.route('/desc/', methods=['GET', 'POST'])
def index_desc():
    type = passionfroid.find().distinct('type')
    tag = passionfroid.find().distinct('tag')
    passionfroids = passionfroid.find().sort("nom", -1)
    countProduits = passionfroids.count()
    return render_template('index.html', passionfroids=passionfroids, type=type, tag=tag,countProduits=countProduits)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
