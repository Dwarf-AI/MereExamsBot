def college_table(session, cid, detail):
    college_name = college_table.loc[college_table.cid==cid,'name'].values[0]

    if detail in ['address','photo','contact','reviews']:
        if cid not in google_table[1].values:
            if detail in ['photo','reviews']:
                return make_json(session,{'text': f'Sorry, we don\'t have any {detail} for {college_name} })
            else:
                # https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference=&key=YOUR_API_KEY

        url = "https://maps.googleapis.com/maps/api/place/details/json"

        querystring = {"key":"AIzaSyAO7ow2BD4c3BmFonOUjVshoAgf_P5ZhYo","placeid":'ChIJM7k39sBPXDkRiU6Om4PD_e8'}

        headers = {
            'cache-control': "no-cache",
            'postman-token': "fe1605ac-5a86-7b9f-4074-ca50dc58dbc5"
        }
        response = requests.request("POST", url, headers=headers, params=querystring)

        if detail == 'address':

        elif detail == 'photo':

        elif detail == 'contact':

        elif detail == 'reviews':

    else:
