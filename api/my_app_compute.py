from flask import Flask, jsonify, request
import pymongo
import json
from bson import json_util
from bson.objectid import ObjectId

app = Flask(__name__)

# MongoDB connection
client = pymongo.MongoClient('mongodb://raiabril:J4v5f7o3@raicluster-shard-00-00-quqjq.mongodb.net:27017,raicluster-shard-00-01-quqjq.mongodb.net:27017,raicluster-shard-00-02-quqjq.mongodb.net:27017/test?ssl=true&replicaSet=RaiCluster-shard-0&authSource=admin')

def toJson(data):
    return json.dumps(data, default=json_util.default)

@app.route('/')
def getHello():
    return "Go to address/api/v0.1/"

@app.route('/api/v0.1/')
def get():
    cur = client.mydb.bitcoin.find({},{'_id':False}).limit(10)
#    return str(json.dumps({'results': list(cur)}, 
#        default = json_util.default,
#        indent = 4))
    json_results = []
    for result in cur:
        json_results.append(result)
#    return toJson(json_results)
#    print(list(json_results))
    return jsonify({'bitcoin':json_results})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
