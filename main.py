from collections import defaultdict
import json
from flask import Flask, request, make_response, jsonify
import numpy as np
import pandas as pd
import requests
import random
from extract_college_detail import *
from card import *
college_table = pd.read_csv('all_institution_merged.csv',index_col=0,engine='python')
course_table = pd.read_csv('data/all_institutions_course_ids_live_new.csv',index_col=0,engine='python')

app = Flask(__name__)
log = app.logger

def course_detail(sess):

    """
    Return Course_details if Course and Specialization known.
    """
    if 'Course_Name' in sess.keys() and 'Specialization' in sess.keys() and 'Course_detail' in sess.keys():
        return make_response(jsonify({'fulfillmentText': f'{sess["Course_detail"]} of {sess["Course_Name"]} in {sess["Specialization"]} in {sess["CollegeName"]} is answer'}))

    elif 'Course_Name' in sess.keys() and 'Specialization' in sess.keys() and 'Course_detail' not in sess.keys():
        return make_response(jsonify({'fulfillmentText': f'What you want to know about {sess["Specialization"]} in {sess["Course_Name"]}'}))

    elif 'Course_Name' in sess.keys() and 'Specialization' not in sess.keys() and 'Course_detail' in sess.keys():
        return make_response(jsonify({'fulfillmentText': f'Choose specialization in {sess["Course_Name"]}'}))

    elif 'Course_Name' not in sess.keys() and 'Specialization' in sess.keys() and 'Course_detail' in sess.keys():
        return make_response(jsonify({'fulfillmentText': f'Choose course in {sess["Specialization"]}'}))

    elif 'Course_Name' not in sess.keys() and 'Specialization' not in sess.keys() and 'Course_detail' in sess.keys():
        return make_response(jsonify({'fulfillmentText': f'Select a course whose {sess["Course_detail"]} you want to know'}))
    elif 'Course_Name' in sess.keys() and 'Specialization' not in sess.keys() and 'Course_detail' not in sess.keys():
        return make_response(jsonify({'fulfillmentText': f'Select a specialization in {sess["Course_Name"]}'}))
    else:
        return None

def clg_list(sess, param):
    #User_desire

    if 'User_desire' in sess.keys():
        urge = sess['User_desire']

        if urge == 'university':
            return make_response(jsonify({'fulfillmentText': f'follwing universities are there according to your param'}))
        elif urge == 'colleges':
            return make_response(jsonify({'fulfillmentText': f'follwing colleges are there according to your param'}))
        elif urge == 'courses':
            return make_response(jsonify({'fulfillmentText': f'follwing courses are there according to your param'}))
        elif urge == 'specialization':
            return make_response(jsonify({'fulfillmentText': f'follwing specialization are there according to your param'}))

    else:

        if 'UniversityName' in param:
            return make_response(jsonify({'fulfillmentText': f'Select a college in {sess["UniversityName"]}'}))

        elif 'Course_Name' in param:
            #print('hmm')
            return make_response(jsonify({'fulfillmentText': f'Select Universities offering {sess["Course_Name"]}'}))

        elif 'CityName' in param:
            return make_response(jsonify({'fulfillmentText': f'Select Course you want to pursue in {sess["CityName"]}'}))

        elif 'StateName' in param:
            return make_response(jsonify({'fulfillmentText': f'Select city in {sess["StateName"]}'}))

        elif 'Specialization' in param:
            return make_response(jsonify({'fulfillmentText': f'Select location of college where you wanna pursue {sess["Specialization"]}'}))

        elif 'Ownership' in param:
            return make_response(jsonify({'fulfillmentText': f'Select Select Course you wanna take in {sess["Ownership"]}'}))
        elif 'Course_detail' in param:
            return make_response(jsonify({'fulfillmentText': f'Please type any university or college name you wanna take in'}))
        else:
            return make_response(jsonify({'fulfillment':'Not found'}))

@app.route('/', methods=["POST"])
def webhook():
    global college_table
    """This method handles the http requests for the Dialogflow webhook
    """
    req = request.get_json(silent=True, force=True)


    session= req['session']
    global user_sessions

 # Check if the request is correct
    try:
        action = req.get('queryResult').get('action')
    except AttributeError:
        return 'json error'

    if action == 'bot_functionality':
        return make_response(jsonify({'fulfillmentText':f"{{\
                'session' : {session},\
                'messages' : [\
                    {{'text'}} : {{'I can provide you info about 40K+ colleges in India'}},\
                ]\
            }}"}))

    if req["queryResult"]["parameters"]['CollgeName1']:
        req["queryResult"]["parameters"]['CollegeName'] = req["queryResult"]["parameters"].pop('CollgeName1')
    elif req["queryResult"]["parameters"]['CollegeName2']:
        req["queryResult"]["parameters"]['CollegeName'] = req["queryResult"]["parameters"].pop('CollegeName2')

# Retrieve parameters and store in session_id of user.
    params_update = req["queryResult"]["parameters"].keys()

    params_update = list(params_update)

    # print(req["queryResult"]["parameters"])

    rmv_list = []

    for param in params_update:
        if req['queryResult']['parameters'][param] == '':
            rmv_list.append(param)
            continue

        #print(req["queryResult"]["parameters"][param])
        if req["session"] in user_sessions.keys():
            user_sessions[req["session"]][param] = req["queryResult"]["parameters"][param]
        else:
            #print(f'new:{param}')
            user_sessions[req["session"]] = defaultdict()
            user_sessions[req['session']][param] = req['queryResult']['parameters'][param]

    for param in rmv_list:
        params_update.remove(param)

    #print(params_update)
    #print(user_sessions)
    sess = user_sessions[req["session"]]     #shortcut to access parameters
    print(sess)




    if action == 'College_info':
        if 'CollegeName' in sess.keys():
            if 'College_detail' in params_update:
                if sess["College_detail"] == 'Course_info':
                    answer = course_detail(sess)
                    if answer == None:
                        return make_response(jsonify({'fulfillment': f'all courses in {sess["CollegeName"]} '}))
                    else:
                        return answer
                else:
                    return college_func(session,sess['CollegeName'], sess['College_detail'], college_table)

            elif 'Specialization' in params_update or 'Course_detail' in params_update or 'Course_Name' in params_update:
                answer = course_detail(sess)
                return answer

            else:

                if 'College_detail' in sess.keys():
                    if sess["College_detail"] == 'Course_info':
                        answer = course_detail(sess)
                        if answer == None:
                            return make_response(jsonify({'fulfillment': f'all courses in {sess["CollegeName"]} '}))
                        else:
                            return answer
                    else:
                        return college_func(session,sess['CollegeName'], sess['College_detail'], college_table)

                answer = course_detail(sess)

                if answer == None:
                    cid = sess['CollegeName']
                    row = college_table.loc[college_table.cid == cid]
                    card_str = make_card(row)
                    return make_response(jsonify({'fulfillmentText': f'{{\
                                                     "messages" : [\
                                                             {{"card":"{card_str}"}}]\
                                                 }}'}))
                else:
                    return answer

        else:
            return clg_list(sess, params_update)

    if action == 'list':
        print('list')
        return clg_list(sess, params_update)


if __name__ == '__main__':
    user_sessions = defaultdict()

    app.run(port='4000', debug=True)
