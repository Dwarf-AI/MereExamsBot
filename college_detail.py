def college_func(session, cid, detail):
    row = college_table.loc[college_tabe.cid == cid]
    college_name = row.name.value

    if detail in ['photos   ','reviews']:
        if str(row.place_id.value) == 'nan':
            possible_chips = ['about', 'contact', 'address', 'reviews', 'photos'] - detail
            chips = set(random.sample(possible_chips, 3))
            make_response(jsonify({

                'session' : session,

                'messages' :[
                    {'text': f"Sorry, I don't have any {detail} for {college_name}"},
                    {'text': 'What else you want to know?'},
                    {'chips': chips}
                ]
            }))
            return make_json(session,{})

        else:
            url = "https://maps.googleapis.com/maps/api/place/details/json"

            querystring = {"key":"AIzaSyAO7ow2BD4c3BmFonOUjVshoAgf_P5ZhYo","placeid":str(row.place_id.value)}

            headers = {
                'cache-control': "no-cache",
                'postman-token': "fe1605ac-5a86-7b9f-4074-ca50dc58dbc5"
            }
            response = requests.request("POST", url, headers=headers, params=querystring)
            response = response.json()



    if detail in ['address','photo','contact','reviews']:
        if cid not in google_table[1].values:
            if detail in ['photo','reviews']:

            else:
                # https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference=&key=YOUR_API_KEY


        if detail == 'address':

        elif detail == 'photo':

        elif detail == 'contact':

        elif detail == 'reviews':

    else:
