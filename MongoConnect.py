import pymongo
#import random
#import os
from mysql.connector import errorcode, Error
#from flask import Flask, request, jsonify,render_template
import Error as err

def connectmongo():
    try:
        client = pymongo.MongoClient('mongodb+srv://keerthana:root@pizzabot.kslha.mongodb.net/test')

        mydb = client['customers']

        return mydb
    except Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
            return False
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
            return False
        else:
            print(err)
            return False
'''app = Flask(__name__)
@app.route("/webhook/index")
def index():
    return render_template("index.html")

@app.route("/webhook", methods=["get", "post"])
def fetch():
    conn = connectmongo()
    print(f"Connection status : {conn}")
    req = request.get_json(silent=True, force=True)
    action = req.get('queryResult').get('action')
    return {'fulfillmentText': 'This is a response from webhook.'}
    print(req)
    if conn is False:
        return err.ReturnConnectionError()
    else:
        information=conn.pizza_customer
        rec=information.find_one({})
        #for rec in information.find({}):
            #print(rec)
            #information=conn.pizza_customer
        return rec

@app.route("/insert", method=["get","post"])
def insertquery():
    conn=connectmongo()
    print(f"Connection status : {conn}")
    if conn is False:
        return err.ReturnConnectionError()
    else:
        information=conn.pizza_customer
        order_id = random.randint(2, 1000)
        print(order_id)
        rec=information.insert_one({'firstname':'keerthana,'mobile_no':9090090090,'pincode':605001,'pizza_type':'BBQ Chicken pizza','pizza_size':'large','pizza_crust':'thin','_id':order_id,'status':'ordered'})
        return rec



if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    print("starting on port %d" % (port))
    app.run(debug=True, port=5000)
'''