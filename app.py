from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
import requests
import helpers

with open('data/TierList.json', encoding="utf-8") as json_file:
  tier_list_data = json.load(json_file)

with open('data/HeroTypes.json', encoding="utf-8") as json_file:
  hero_types_data = json.load(json_file)

with open('data/Champions.json', encoding="utf-8") as json_file:
  champions_data = json.load(json_file)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  content = db.Column(db.String(200), nullable=False)
  date_created = db.Column(db.DateTime, default=datetime.now())

  def __repre__(self):
    return '<Task %r>' % self.id

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/hello')
def hello():
  return 'Hello Flask!'

@app.route('/json')
def serve_json():
  data = {
    "message": "This is a JSON response " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "status": "success"
  }
  return jsonify(data)

@app.route('/search', methods=['GET'])
def search():
  query = request.args.get('query')

  if query == None:
    return "No query provided!"
  
  local_data = helpers.findChampionsInList(query, champions_data)
  if len(local_data):
    return local_data[0]
  
  results = helpers.findChampionsInList(query, tier_list_data)

  if len(results) == 0:
    return "No results for \"" + str(query) + "\""
  if len(results) > 1:
    return "Multiple search results for \"" + str(query.lower()) + "\": " + json.dumps(results)
  if len(results) == 1:
    hero_id = int(results[0]['heroId'])
    model_id = int(hero_id / 10) * 10
    forms_list = requests.get('https://hellhades.com/wp-json/hh-api/v3/raid/forms/' + str(model_id)).json()
    # forms_list = [{"heroid": "4716", "form": "1", "role": "Support", "model": "4710", "rarity": "Legendary", "health": "126", "attack": "82", "defense": "117", "speed": "110", "critrate": "0.15", "critdamage": "0.50", "critheal": "0.50", "accuracy": "0", "resistance": "40", "ignoredef": "0.00", "skills": "47101,47102,47103,47105,47106,47104"}]
    hero_form = next((x for x in forms_list if x['heroid'] == str(hero_id)), None)
  if hero_form == None:
    return "Hero Form not found!"
  else:
    hero_type = next((x for x in hero_types_data if x['id'] == hero_id), None)

  if hero_type == None:
    return "Hero Type not found!"
  
  helpers.fetchImageAndSave('https://hellhades.com/wp-content/plugins/rsl-assets/assets/champbyIds/' + model_id + '.png', 'Avatars/' + results[0]['champion'].replace(" ", "") + '.png')

  champion = results[0]
  champion["rarity"] = hero_form["rarity"]
  champion["skills"] = hero_form["skills"]
  champion["faction"] = hero_type["faction"]
  champion["modalId"] = model_id

  return "Found \"" + results[0]['champion'] + "\"<br>HeroId: " + str(hero_id) + "<br><br>Forms: " + json.dumps(forms_list) + "<br><br>Hero Form: " + json.dumps(hero_form) + "<br><br>Image:<br><img src=\"" + str(model_id) + ".png\" /><br><br>Champion: " + json.dumps(champion)

if __name__ == '__main__':
  app.run(port=3000, debug=True)