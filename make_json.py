def make_json(session, reponse):

    return make_response(jsonify({

        'session' : session,

        'response' : response
    }))
