from collections import defaultdict
import json
from flask import Flask, request, make_response, jsonify
import numpy as np
import pandas as pd
import requests
import random
def college_func(session, cid, detail, college_table):
    row = college_table.loc[college_table.cid == cid]
    college_name = row['name'].values[0]

    possible_chips = list(['about', 'contact', 'address', 'reviews', 'photos'])

    if detail in possible_chips:
        possible_chips.remove(detail)
        
    chips = random.sample(possible_chips, 3)

    if detail == 'about':
        prgh = ''
        if str(row.year_of_establishment.values[0]) != 'nan':
            prgh = college_name + ' was established in ' + str(int((row.year_of_establishment.values[0]))) + '. '
        if str(row.management_type.values[0]) != 'nan':
            prgh += 'This college is ' + str(row.management_type.values[0]) + '. '
        if str(row.area.values[0]) != 'nan':
            prgh += 'It has ' + str(row.area.values[0]) + ' acres of land.'
        columns = list(filter(lambda x: str(row[x].values[0]) == 'True', row.columns))
        if len(columns)>0:
            prgh += ' College contains major facilities like '
            for element in columns[:-1]:
                element = str(element).replace('_',' ')
                prgh += element + ', '
            prgh += str(columns[-1]).replace('_',' ') + '.'
        if prgh == '':
            return make_response(jsonify({'fulfillmentText':f"{{\
                'session' : {session},\
                'messages' : [\
                    {{'cid' :{cid}}},\
                    {{'text': 'Sorry, I can't help you with this for {college_name}'}},\
                    {{'text': 'What else you want to know?'}},\
                    {{'chips': {chips}}}\
                ]\
            }}"}))
        else:
            return make_response(jsonify({'fulfillmentText':f"{{\
                'session' : {session},\
                'messages' : [\
                    {{'cid' :{cid}}},\
                    {{'text': {prgh}}},\
                    {{'text': 'What else you want to know?'}},\
                    {{'chips': {chips}}}\
                ]\
            }}"}))


    elif detail in ['photos','reviews']:
        if str(row.place_id.values[0]) == 'nan':
            return make_response(jsonify({'fulfillmentText':f"{{\
                'session' : {session},\
                'messages' : [\
                    {{'cid' :{cid}}},\
                    {{'text': 'Sorry, I do not have any {detail} for {college_name}'}},\
                    {{'text': 'What else you want to know?'}},\
                    {{'chips': {chips}}}\
                ]\
            }}"
}))
        else:
            url = "https://maps.googleapis.com/maps/api/place/details/json"

            querystring = {"key":"AIzaSyAO7ow2BD4c3BmFonOUjVshoAgf_P5ZhYo","placeid":str(row.place_id.values[0])}

            headers = {
                'cache-control': "no-cache",
                'postman-token': "fe1605ac-5a86-7b9f-4074-ca50dc58dbc5"
            }
            response = requests.request("POST", url, headers=headers, params=querystring)
            response = response.json()

            if detail == 'photos':
                photos_json_list = response['result']['photos']
                photos_url_list = []
                for photo_json in photos_json_list:
                    ref = photo_json['photo_reference']
                    photos_url_list.append(f'https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={ref}&key=AIzaSyAO7ow2BD4c3BmFonOUjVshoAgf_P5ZhYo')

                return make_response(jsonify({'fulfillmentText':f"{{\
                    'session' : {session},\
                    'messages' : [\
                        {{'cid' :{cid}}},\
                        {{'text': 'Here are some photos for {college_name}'}},\
                        {{'photos': {photos_url_list}}},\
                        {{'text': 'What else you want to know?'}},\
                        {{'chips': {chips}}}\
                    ]\
                }}"
}))
            else:
                return make_response(jsonify({'fulfillmentText':f"{{\
                    'session' : {session},\
                    'messages' : [\
                        {{'cid' :{cid}}},\
                        {{'text': 'Here are reviews for {college_name}'}},\
                        {{'reviews': {response['result']['reviews']} }},\
                        {{'text': 'What else you want to know?'}},\
                        {{'chips': {chips}}}\
                    ]\
                }}"
}))

    elif detail == 'address':
        if str(row.place_id.values[0]) == 'nan':
            return make_response(jsonify({'fulfillmentText':f"{{\
                'session' : {session},\
                'messages' : [\
                    {{'cid' :{cid}}},\
                    {{'text': 'Address for {college_name} is {str(row.address.values[0])}'}},\
                    {{'text': 'What else you want to know?'}},\
                    {{'chips': {chips}}}\
                ]\
            }}"
}))
        else:
            return make_response(jsonify({'fulfillmentText':f"{{\
                'session' : {session},\
                'messages' : [\
                    {{'cid' :{cid}}},\
                    {{'text': 'Address for {college_name} is {row.address.values[0]}'}},\
                    {{'map':{{'lat':{row.lat.values[0]},'lng':{row.lng.values[0]}}}}},\
                    {{'text': 'What else you want to know?'}},\
                    {{'chips': {chips}}}\
                ]\
            }}"
            }))

    elif detail == 'contact':
        print('loda')
        if str(row.website.values[0]) == 'nan' and str(row.phone.values[0]) == 'nan':
            return make_response(jsonify({'fulfillmentText':f"{{\
                'session' : {session},\
                'messages' : [\
                    {{'cid' :{cid}}},\
                    {{'text': 'Sorry, I don't have any {detail} for {college_name}'}},\
                    {{'text': 'What else you want to know?'}},\
                    {{'chips': {chips}}}\
                ]\
            }}"
}))
        else:
            if str(row.website.values[0]) == 'nan':
                return make_response(jsonify({'fulfillmentText':f"{{\
                    'session' : {session},\
                    'message' : [\
                        {{'cid' :{cid}}},\
                        {{'text': f'You can contact {college_name} at {row.phone.values[0]}'}},\
                        {{'text': 'What else you want to know?'}},\
                        {{'chips': {chips}}}\
            ]\
            }}"
            }))


            elif str(row.phone.values[0]) == 'nan':
                return make_response(jsonify({'fulfillmentText':f"{{\
                    'session' : {session},\
                    'message' : [\
                        {{'cid' :{cid}}},\
                        {{'text': f'You can find {college_name} at {row.website.values[0]}'}},\
                        {{'text': 'Anything else I can do for you?'}},\
                        {{'chips': {chips}}}\
            ]\
            }}"
}))

            else:

                return make_response(jsonify({'fulfillmentText':f"{{\
                    'session' : {session},\
                    'message' : [\
                        {{'cid' :{cid}}},\
                        {{'text': 'I found these contact details for {college_name}\nPhone: {row.phone.values[0]}\nWebsite: {row.website.values[0]}'}},\
                        {{'text': 'Anything else I can do for you?'}},\
                        {{'chips': {chips}}}\
                    ]\
                }}"

                                             }))

    else:
        val = str(row[f'{detail}'].values[0])
        if val == 'nan':
            return make_response(jsonify({'fulfillmentText':f"{{\
                'session' : {session},\
                'messages' : [\
                    {{'cid' :{cid}}},\
                    {{'text': 'Sorry, I don't have any {detail} for {college_name}'}},\
                    {{'text': 'What else you want to know?'}},\
                    {{'chips': {chips}}}\
                ]\
            }}"
}))
        elif val == 'True':
            return make_response(jsonify({'fulfillmentText':f"{{\
                'session' : {session},\
                'messages' : [\
                    {{'cid' :{cid}}},\
                    {{'text': 'As much as I remember {detail} is there in {college_name}'}},\
                    {{'text': 'What else you want to know?'}},\
                    {{'chips': {chips}}}\
                ]\
            }}"
}))
        elif val == 'False':
            return make_response(jsonify({'fulfillmentText':f"{{\
                'session' : {session},\
                'messages' : [\
                    {{'cid' :{cid}}},\
                    {{'text': 'As much as I remember {detail} is not there in {college_name}'}},\
                    {{'text': 'What else you want to know?'}},\
                    {{'chips': {chips}}}\
                ]\
            }}"
}))
        else:
            return make_response(jsonify({'fulfillmentText':f"{{\
                'session' : {session},\
                'messages' : [\
                    {{'cid' :{cid}}},\
                    {{'text': '{detail} for {college_name} is {val}'}},\
                    {{'text': 'What else you want to know?'}},\
                    {{'chips': {chips}}}\
                ]\
            }}"
}))
