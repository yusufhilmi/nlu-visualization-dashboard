import requests
import sys
import os
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash, json, jsonify

"""     --------  For Local Access   -------------
SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "static", "IBM_composite_query.json")
data = json.load(open(json_url, encoding="mbcs"))      #encoding fixed mbcs is the correct one 
print(str(data))
"""

app = Flask(__name__)


@app.route('/favicon.ico')
def favicon():
    return "malak"


@app.route('/trial', methods=['GET', 'POST'])
def trial():
    return render_template('cloud_2.html')


@app.route('/', methods=['GET', 'POST'])
def index():
    nodes = []
    links = []
    words = []
    articles = []

    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "static", "IBM_composite_query.json")
    data = json.load(open(json_url, encoding="mbcs"))  # encoding fixed mbcs is the correct one
    index_num = len(data['results'][1]['enriched_text']['entities'])

    # index_res = len(data['results'])

    #  index_num = len(request.json['results'][1]['enriched_text']['entities'])

    count = 0
    label_count = 0

    for j in range(len(data['results'])):
        articles.append(data['results'][j]['title'])
        # print(articles[j])
        nodes.append({'id': j, 'label': articles[j], 'level': 1})
        count += 1

    for j in range(len(articles)):
        label_count += len(data['results'][j]['enriched_text']['entities'])
        print(label_count)
            # word = request.json['results'][1]['enriched_text']['entities'][i]['text']
        for i in range(len(data['results'][j]['enriched_text']['entities'])):
            # print(words[i])
            if data['results'][j]['enriched_text']['entities'][i]['type'] == 'Location':
                words.append(data['results'][j]['enriched_text']['entities'][i]['text'])
                nodes.append({'id': count, 'label': words[-1], 'level': 2})
                print(nodes[-1])
                links.append({'source': count, 'target': j})
                count += 1
        print("-----------------------------------------")
    # print(nodes)
    # print(links)
    return render_template('cloud.html', nodes=json.dumps(nodes, indent=2), links=json.dumps(links, indent=2))


port = os.getenv('VCAP_APP_PORT', '8000')

if __name__ == '__main__':
    app.run(port=int(port), debug=True)
