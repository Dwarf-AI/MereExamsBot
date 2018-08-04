def make_json(session, type, reponse):

    return make_response(jsonify({

        'session' : req['session'],

        'type' : type,

        'response': response
    }))
