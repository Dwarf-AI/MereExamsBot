def college_func(session, cid, detail):
    row = college_table.loc[college_tabe.cid == cid]
    college_name = row.name.value

    possible_chips = ['about', 'contact', 'address', 'reviews', 'photos'] - detail
    chips = random.sample(possible_chips, 3)
    if detail in ['photos','reviews']:
        if str(row.place_id.value) == 'nan':
            return make_response(jsonify({
                'session' : session,
                'messages' :[
                    {'text': f"Sorry, I don't have any {detail} for {college_name}"},
                    {'text': 'What else you want to know?'},
                    {'chips': chips}
                ]
            }))
        else:
            url = "https://maps.googleapis.com/maps/api/place/details/json"

            querystring = {"key":"AIzaSyAO7ow2BD4c3BmFonOUjVshoAgf_P5ZhYo","placeid":str(row.place_id.value)}

            headers = {
                'cache-control': "no-cache",
                'postman-token': "fe1605ac-5a86-7b9f-4074-ca50dc58dbc5"
            }
            response = requests.request("POST", url, headers=headers, params=querystring)
            response = response.json()

            if detail == 'photos':
                photos_json_list = response.result.photos
                photos_url_list = []
                for photo_json in photos_json_list:
                    ref = photo_json.photo_reference
                    photos_url_list.append(f"https://maps.googleapis.com/maps/api/place/photo?photoreference={ref}&key=AIzaSyAO7ow2BD4c3BmFonOUjVshoAgf_P5ZhYo")

                return make_response(jsonify({
                    'session' : session,
                    'messages' :[
                        {'text': f"Here are some photos for {college_name}"},
                        {'photos': photos_url_list}
                        {'text': 'What else you want to know?'},
                        {'chips': chips}
                    ]
                }))
            else:
                return make_response(jsonify({
                    'session' : session,
                    'messages' :[
                        {'text': f"Here are reviews for {college_name}"},
                        {'reviews': response.result.reviews}
                        {'text': 'What else you want to know?'},
                        {'chips': chips}
                    ]
                }))


    elif detail == 'contact'
        if str(row.website.value) == 'nan' and str(row.phone.value) == 'nan':
            return make_response(jsonify({
                'session' : session,
                'messages' :[
                    {'text': f"Sorry, I don't have any {detail} for {college_name}"},
                    {'text': 'What else you want to know?'},
                    {'chips': chips}
                ]
            }))
        else:
            if str(row.website.value) == 'nan':
                return make_response(jsonify({
                    'session' : session,
                    'message' : [
                        {'text': f'You can contact {college_name} at {row.phone.value}'}
                        {'text': 'What else you want to know?'},
                        {'chips': chips}
            ]

            
            elif str(row.phone.value) == 'nan':
                return make_response(jsonify({
                    'session' : session,
                    'message' : [
                        {'text': f'You can find {college_name} at {row.website.value}'},
                        {'text': 'Anything else I can do for you?'},
                        {'chips': chips}
            ]

            else:
                return make_response(jsonify({
                    'session' : session,
                    'message' : [
                        {'text': f'I found these contact details for {college_name}\nPhone: {row.phone.value}\nWebsite: {row.website.value}'},
                        {'text': 'Anything else I can do for you?'},
                        {'chips': chips}
                    ]
                }))