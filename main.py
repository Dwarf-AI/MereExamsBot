from collections import defaultdict
import json
from flask import Flask, request, make_response, jsonify
app = Flask(__name__)
log = app.logger

def course_detail(sess):

    """
    Return Course_details if Course and Specialization known.
    """

    if 'Course_Name' in sess.keys() and 'Specialization' in sess.keys() and 'College_detail' in sess.keys():
        return make_response(jsonify({'fulfillmentText': f'{sess["College_detail"]} of {sess["Course_Name"]} in {sess["Specialization"]} in {sess["CollegeName"]} is answer'}))

    elif 'Course_Name' in sess.keys() and 'Specialization' in sess.keys() and 'College_detail' not in sess.keys():
        return make_response(jsonify({'fulfillmentText': f'What you want to know about {sess["Specialization"]} in {sess["Course_Name"]}'}))

    elif 'Course_Name' in sess.keys() and 'Specialization' not in sess.keys() and 'College_detail' in sess.keys():
        return make_response(jsonify({'fulfillmentText': f'Choose specialization in {sess["Course_Name"]}'}))

    elif 'Course_Name' not in sess.keys() and 'Specialization' in sess.keys() and 'College_detail' in sess.keys():
        return make_response(jsonify({'fulfillmentText': f'Choose course in {sess["Specialization"]}'}))

    elif 'Course_Name' not in sess.keys() and 'Specialization' not in sess.keys() and 'College_detail' in sess.keys():
        return make_response(jsonify({'fulfillmentText': f'Select a course whose {sess["College_detail"]} you want to know'}))
    elif 'Course_Name' in sess.keys() and 'Specialization' not in sess.keys() and 'College_detail' not in sess.keys():
        return make_response(jsonify({'fulfillmentText': f'Select a specialization in {sess["Course_Name"]}'}))
    else:
        return make_response(jsonify({'fulfillment':'Not found'}))


def course_list(sess):
    if 'UniversityName' in sess.keys():
        return make_response(jsonify({'fulfillmentText': f'Select a college in {sess["UniversityName"]}'}))

    elif 'Course_Name' in sess.keys():
        return make_response(jsonify({'fulfillmentText': f'Select Universities offering {sess["Course_Name"]}'}))

    elif 'CityName' in sess.keys():
        return make_response(jsonify({'fulfillmentText': f'Select Course you want to pursue in {sess["CityName"]}'}))

    elif 'StateName' in sess.keys():
        return make_response(jsonify({'fulfillmentText': f'Select city in {sess["StateName"]}'}))

    elif 'Specialization' in sess.keys():
        return make_response(jsonify({'fulfillmentText': f'Select location of college where you wanna pursue {sess["Specialization"]}'}))
    
    elif 'Ownership' in sess.keys():
        return make_response(jsonify({'fulfillmentText': f'Select Select Course you wanna take in {sess["Ownership"]}'}))
    else:
        return make_response(jsonify({'fulfillment':'Not found'}))

@app.route('/', methods=["POST"])
def webhook():

    global user_sessions

    """This method handles the http requests for the Dialogflow webhook
    """
    req = request.get_json(silent=True, force=True)

 # Check if the request is correct
    try:
        action = req.get('queryResult').get('action')
    except AttributeError:
        return 'json error'

# Retrieve parameters and store in session_id of user.
    params_update = req["queryResult"]["parameters"].keys()
    for param in params_update:
        print(req["queryResult"]["parameters"][param])
        if req["session"] in user_sessions.keys():
            user_sessions[req["session"]][param] = req["queryResult"]["parameters"][param]
        else:
            user_sessions[req["session"]] = defaultdict()
        sess = user_sessions[req["session"]]     #shortcut to access parameters

    if action == 'College_info':
        if 'CollegeName' in sess.keys():
            if 'College_detail' in sess.keys():
                if sess["College_detail"] == 'Course_info':
                    course_detail(sess)
                else:
                    return make_response(jsonify({'fulfillmentText': f'What you want to know : about, admission, contact'}))

            answer = course_detail(sess)
            if answer == None:
                return make_response(jsonify({'fulfillmentText': f'Select a college'}))
            else:
                return make_response(jsonify({'fulfillmentText': f'{answer}'}))

        else:
            course_list(sess)

    if action == 'list':
        course_list(sess)


if __name__ == '__main__':
    user_sessions = defaultdict()
    app.run(debug=True)

