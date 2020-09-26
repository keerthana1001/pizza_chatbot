import urllib
import json
import MongoConnect as connection
import Error as err
import os
from flask import Flask, request, make_response,render_template, jsonify
import random
import re
order_id=random.randint(1,100000)
app=Flask(__name__)
@app.route("/")
def index():
    return render_template("index.html")
@app.route("/webhook", methods=["get", "post"])
def webhook():
    req=request.json
    #print(req)
    #res=json.dumps(req,indent=4)
    #print(res)
    res = makeWebhookResult(req)
    res = json.dumps(res, indent=4)
    #print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return res

def makeWebhookResult(req):
    conn = connection.connectmongo()
    print(f"Connection status : {conn}")
    information = conn.pizza_customer
    if req.get("queryResult").get("action")=='getpincode':
        print(req)


        if conn is False:
            return err.ReturnConnectionError()
        else:

            result=req.get("queryResult")
            parameters=result.get("parameters")
            pincode=parameters.get('number-sequence')
            outputContext=result.get('outputContexts')
            oc1=outputContext[1]
            pizza_size=oc1.get('parameters').get('pizza-size')
            pizza_crust=oc1.get('parameters').get('pizza-crust')
            name=oc1.get('parameters').get('name')
            phoneno=oc1.get('parameters').get('phone-number')
            oc5=outputContext[5]
            pizza_type=oc5.get('parameters').get('pizza-type')
            print(oc5)
            print(pizza_size,pizza_crust,name,phoneno,pizza_type)
            information.insert_one({'name':name,'_id':order_id,'phone_number':phoneno,'pincode':pincode,'pizza_type':pizza_type,'pizza_size':pizza_size,'pizza_crust':pizza_crust,'status':'ordered'})
            speech="The total amount is Rs. 250. Your order will be delivered to "+pincode+" in 30 minutes. You have ordered "+pizza_type,pizza_size+" with "+pizza_crust+" crust. Your order id is "+str(order_id)+". Enter your order id to check status"
            
            return {"fulfillmentText":"This is response"}
            #return {"payload": {"google": {"expectUserResponse": True,"richResponse": {"items": [{"simpleResponse": {"textToSpeech": speech,"displayText": speech}}]}}}}
            #return {"fulfillmentMessages": [{"text": {"text": ["The total amount is Rs. 250. Your order will be delivered to "+pincode+" in 30 minutes. You have ordered "+pizza_type,pizza_size+" with "+pizza_crust+" crust. Your order id is "+str(order_id)+". Enter your order id to check status"]}}]}

    if req.get("queryResult").get("queryText")==str(order_id) or req.get("queryResult").get("queryText")==[r['_id']for r in information.find({'_id'})]:
        print(str(order_id))
        conn = connection.connectmongo()
        print(f"Connection status : {conn}")

        if conn is False:
            return err.ReturnConnectionError()
        else:
            information=conn.pizza_customer
            res=req.get("queryResult").get("queryText")
            res=int(res)
            print(res)
            for r in information.find({'_id':res}):
                status=r['status']
                print(status)
                return {"fulfillmentMessages": [{"text": {"text": [status]}}]}


if __name__ == "__main__":
    
    app.run()
