from collections import defaultdict
import json
from flask import Flask, request, make_response, jsonify
import numpy as np
import pandas as pd
import requests
import random
import re
from reply_gen import *

def college_func(session, cid, detail, college_table):
    row = college_table.loc[college_table.cid == cid]
    college_name = row["name"].values[0]

    possible_chips = list(["about", "contact", "address", "reviews", "photos"])

    if detail in possible_chips:
        possible_chips.remove(detail)

    chips = random.sample(possible_chips, 3)
    
    if detail == "about":
        prgh = "" # Paragraph
        if str(row.year_of_establishment.values[0]) != "nan":
            prgh = college_name + " was established in " + str(int((row.year_of_establishment.values[0]))) + ". "
        if str(row.management_type.values[0]) != "nan":
            prgh += "This college is " + str(row.management_type.values[0]) + ". "
        if str(row.area.values[0]) != "nan":
            prgh += "It has " + str(row.area.values[0]) + " acres of land."
        columns = list(filter(lambda x: str(row[x].values[0]) == "True", row.columns))
        if len(columns)>0:
            prgh += " College contains major facilities like "
            for element in columns[:-1]:
                element = str(element).replace("_"," ")
                prgh += element + ", "
            prgh += str(columns[-1]).replace("_"," ") + "."
        if prgh == "":


            #json
            json_dic = {
                "cid" : cid,
                "messages" : [
                    {"data": f"Sorry, I can\'t help you with this for {college_name}", "type" : "text"},
                    {"data": anything_else(), "type" : "text"},
                    {"data": chips , "type": "chips"}
                ]
            }
            
            json_str = json.dumps(json_dic)
            return make_response(jsonify({"fulfillmentText":json_str}))
        else:

            #json
            json_dic = {
                 'cid' : cid,
                 'messages' : [
                    {'data': prgh, 'type': 'text'},
                    {'data': anything_else(), 'type' : 'text'},
                    {'data': chips, 'type' : 'chips'}
                ]
            }
            json_str = json.dumps(json_dic)
            return make_response(jsonify({"fulfillmentText":json_str}))


    elif detail in ["photos","reviews"]:
        if str(row.place_id.values[0]) == "nan" or (row.place_id.values[0]) == "" :

            #json
            json_dic = {
                "cid" : cid,
                "messages" : [
                    {"data": f"Sorry, I do not have any {detail} for {college_name}", "type" : "text"},
                    {"data": anything_else(), "type" : "text"},
                    {"data": chips, "type" : "chips"}
                ]
            }
            json_str = json.dumps(json_dic)
            return make_response(jsonify({"fulfillmentText":json_str}))
        
        else:
            url = "https://maps.googleapis.com/maps/api/place/details/json"

            querystring = {"key":"AIzaSyAO7ow2BD4c3BmFonOUjVshoAgf_P5ZhYo","placeid":str(row.place_id.values[0])}

            headers = {
                "cache-control": "no-cache",
                "postman-token": "fe1605ac-5a86-7b9f-4074-ca50dc58dbc5"
            }
            response = requests.request("POST", url, headers=headers, params=querystring)
            response = response.json()

            if detail == "photos":
                photos_json_list = response["result"]["photos"]
                photos_url_list = []
                for photo_json in photos_json_list:
                    ref = photo_json["photo_reference"]
                    photos_url_list.append(f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={ref}&key=AIzaSyAO7ow2BD4c3BmFonOUjVshoAgf_P5ZhYo")

                #json
                json_dic = {
                    "cid" : cid,
                    "messages" : [
                        {"data" : f"Here are some photos for {college_name}", "type" : "text"},
                        {"data" : photos_url_list, "type" : "photos"},
                        {"data" : anything_else(), "type" : "text"},
                        {"data" : chips, "type" : "chips"}
                    ]
                }
                json_str = json.dumps(json_dic)
                return make_response(jsonify({"fulfillmentText":json_str}))
            else:
                #json
                json_dic = {
                    "cid" : cid,
                    "messages" : [
                        {"data" : f"Here are reviews for {college_name}", "type" : "text"},
                        {"data" : response["result"]["reviews"], "type" : "reviews"},
                        {"data" : anything_else(), "type" : "text"},
                        {"data" : chips, "type" : "chips"}
                    ]
                }
                json_str = json.dumps(json_dic)
                return make_response(jsonify({"fulfillmentText" : json_str}))

    elif detail == "address":
        if str(row.place_id.values[0]) == "nan":

            #json
            json_dic = {
                "cid" : cid,
                "messages" : [
                    {"data": detail_gen("Address",college_name, str(row.address.values[0])), "type" : "text"},
                    {"data": anything_else(), "type" : "text"},
                    {"data": chips, "type" : "chips"}
                ]
            }
            json_str = json.dumps(json_dic)
            return make_response(jsonify({"fulfillmentText" : json_str}))
        else:
            #json
            json_dic = {
                "cid" : cid,
                "messages" : [
                    {"data": detail_gen("Address",college_name, row.address.values[0]), "type" : "text"},
                    {"data": {
                        "lat": row.lat.values[0],
                        "lng": row.lng.values[0]
                        },
                     "type" : "map"
                    },
                    {"data": anything_else(), "type" : "text"},
                    {"data": chips, "type" : "chips"}
                ]
            }
            json_str = json.dumps(json_dic)
            return make_response(jsonify({"fulfillmentText" : json_str}))

    elif detail == "contact":
        if str(row.website.values[0]) == "nan" and str(row.phone.values[0]) == "nan":

            #json
            json_dic = {
                "cid" : cid,
                "messages" : [
                    {"data": f"Sorry, I don\'t have any {detail} for {college_name}", "type" : "text"},
                    {"data": anything_else(), "type" : "text"},
                    {"data": chips, "type" : "chips"}
                ]
            }

            json_str = json.dumps(json_dic)
            return make_response(jsonify({"fulfillmentText" : json_str}))
            
        else:
            if str(row.website.values[0]) == "nan":

                #json
                json_dic = {
                    "cid" : cid,
                    "messages" : [
                        {"data": f"You can contact {college_name} at {row.phone.values[0]}", "type" : "text"},
                        {"data": anything_else(), "type" : "text"},
                        {"data": chips, "type" : "chips"}
                    ]
                }

                json_str = json.dumps(json_dic)
                return make_response(jsonify({"fulfillmentText" : json_str}))

            elif str(row.phone.values[0]) == "nan":

                #json
                json_dic = {
                    "cid" : cid,
                    "messages" : [
                        {"data": f"You can find {college_name} at {row.website.values[0]}", "type" : "text"},
                        {"data": "Anything else I can do for you?", "type" : "text"},
                        {"data": chips, "type" : "chips"}
                    ]
                }

                json_str = json.dumps(json_dic)
                return make_response(jsonify({"fulfillmentText" : json_str}))
            
            else:

                #json
                json_dic = {
                    "cid" : cid,
                    "messages" : [
                        {"data": f"I found these contact details for {college_name}\nPhone: {row.phone.values[0]}\nWebsite: {row.website.values[0]}", "type" : "text"},
                        {"data": "Anything else I can do for you?", "type" : "text"},
                        {"data": chips, "type" : "chips"}
                    ]
                }

                json_str = json.dumps(json_dic)
                return make_response(jsonify({"fulfillmentText" : json_str}))
            
    else:
        val = str(row[f'{detail}'].values[0])
        if val == "nan":

            #json
            json_dic = {
                "cid" : cid,    
                "messages" : [
                    {"data": f"Sorry, I don\'t have any {detail} for {college_name}", "type" : "text"},
                    {"data": anything_else(), "type" : "text"},
                    {"data": chips, "type" : "chips"}
                ]
            }

            json_str = json.dumps(json_dic)
            return make_response(jsonify({"fulfillmentText" : json_str}))
        
        elif val == 'True':

            #json
            json_dic = {
                "cid" : cid,    
                "messages" : [
                    {"data": f"As much as I remember {detail} is there in {college_name}", "type" : "text"},
                    {"data": anything_else(), "type" : "text"},
                    {"data": chips, "type" : "chips"}
                ]
            }

            json_str = json.dumps(json_dic)
            return make_response(jsonify({"fulfillmentText" : json_str}))
            
        elif val == "False":

            #json
            json_dic = {
                "cid" : cid,
                "messages" : [
                    {"data": f"As much as I remember {detail} is not there in {college_name}", "type" : "text"},
                    {"data": anything_else(), "type" : "text"},
                    {"data": chips, "type" : "chips"}
                ]
            }

            json_str = json.dumps(json_dic)
            return make_response(jsonify({"fulfillmentText" : json_str}))
        
        else:

            #json
            json_dic = {
                    "cid" : cid,
                    "messages" : [
                    {"data": f"{detail} for {college_name} is {val}", "type" : "text"},
                    {"data": anything_else(), "type" : "text"},
                    {"data": chips, "type" : "chips"}
                ]
            }

            json_str = json.dumps(json_dic)
            return make_response(jsonify({"fulfillmentText" : json_str}))
            
