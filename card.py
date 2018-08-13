from collections import defaultdict
import json
from flask import Flask, request, make_response, jsonify
import numpy as np
import pandas as pd
import requests
import random
import mysql.connector as sql
import re

def make_card(row):
    db_connection = sql.connect(host='localhost', database='newmerexamsdb', user='root', password='9871039775')
    df = pd.read_sql(f'select cpfilename from college_pics1 where cid="{row.cid.values[0]}" and pictype="logo";', con=db_connection)
    row_dict = str(row.drop(['old_me_name','old_me_city'],1).applymap(str).to_dict(orient='records')[0]).rstrip('}').lstrip('{')
    
    if df.values.size == 0:
        card_str = f'{{{{\
            "img_url" : "https://www.mereexams.com/assets/images/college-default-image.png",\
            {row_dict}\
        }}}}'
    else:
        card_str = f'{{{{\
            "img_url" : "https://content.mereexams.com/pictures/{row.cid.values[0]}/{df.values[0][0]}",\
            {row_dict}\
        }}}}'
    card_str = re.sub("\\t", '', card_str)
    return re.sub("'", '"', card_str)