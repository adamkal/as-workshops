from flask import Response, request, Flask
from pymongo import MongoClient
from bson.objectid import ObjectId
import json

app = Flask(__name__)
app.debug = True

#db access
client = MongoClient()
db = client.lunch

@app.route('/')
def home():
    #
    return 'Lunches App'

@app.route('/lunch/', methods=['GET'])
def index():
    # lists all lunches     
   
    items = [{
        '_id': str(item['_id']),
        'meal': item['meal'],
        'subscribers': item['subscribers'],
        'date': str(item['date'])
    } for item in db.data.find()]
     
    return Response(json.dumps(items), mimetype='application/json')
   
@app.route('/lunch/<post_id>/', methods=['GET'])
def show_lunch(post_id):
    # shows lunch with provided id
   
    items = [{
        '_id': str(item['_id']),
        'meal': item['meal'],
        'subscribers': item['subscribers'],
        'date': str(item['date'])
    } for item in db.data.find({'_id': ObjectId(post_id)})]
     
    return Response(json.dumps(items), mimetype='application/json')
   
@app.route('/lunch/', methods=['POST'])
def create_lunch(post_id):
    # creates lunch
    
    import datetime
    data = request.get_json()
   
    date = datetime.datetime.strptime(data['date'],"%Y-%m-%d")
   
    post = {
        "date": date,
        "meal": data['meal'],
        "subscribers": [],
        "updated": datetime.datetime.utcnow()
    }
          
    return Response(json.dumps({'status':'OK', 'id':str(db.data.insert(post))}))
    
@app.route('/lunch/<post_id>/hungry/', methods=['POST'])
def subscribe_lunch(post_id):
    # adds employee to lunch subscribers
   
    data = request.get_json()
    lunch = db.data.find({'_id': ObjectId(post_id)})[0]
    if data['employee'] not in lunch['subscribers']:
        lunch['subscribers'].append(data['employee'])
        db.data.save(lunch)
    else:
	    return Response(json.dumps({'status':'EMPLOYEE ALREADY SUBSCRIBES THIS LUNCH', 'lunch':lunch['subscribers']}))
    return Response(json.dumps({'status':'OK', 'lunch':lunch['subscribers']}))
    
@app.route('/lunch/<post_id>/hungry/<employee>/', methods=['DELETE'])
def unsubscribe_lunch(post_id, employee):
    # removes employee from lunch subscribers
    lunch = db.data.find({'_id': ObjectId(post_id)})[0]
    if employee in lunch['subscribers']:
        lunch['subscribers'].remove(employee)
        db.data.save(lunch)
    else:
	    return Response(json.dumps({'status':'EMPLOYEE DOES NOT SUBSCRIBES THIS LUNCH', 'lunch':lunch['subscribers']}))
    return Response(json.dumps({'status':'OK'}))

if __name__ == "__main__":
    app.run()
