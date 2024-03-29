import requests
import sys
import os
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash, json, jsonify


from classified import discovery
username = discovery.username
password = discovery.password
environment_id = 'system'
collection_id = 'news-en'

"""   --------------for discovery------------------
from classified import discovery
username = discovery.username
password = discovery.password
environment_id = 'system'
collection_id = 'news-en'
"""

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

    """
    my_query = discovery.query(environment_id,
                               collection_id,
                               count=10,
                               natural_language_query='composite')
    
    data = my_query.result  # encoding fixed mbcs is the correct one
    """
    my_query = discovery.query(environment_id,
                               collection_id,
                               count=40,
                               natural_language_query='composite')

    data = my_query.result  # encoding fixed mbcs is the correct one
    # index_num = len(data['results'][1]['enriched_text']['entities'])

    # index_res = len(data['results'])

    #  index_num = len(request.json['results'][1]['enriched_text']['entities'])

    count = 0
    label_count = 0

    for j in range(len(data['results'])):
        articles.append(data['results'][j]['title'])
        date = data['results'][j]['publication_date']
        summary = data['results'][j]['text']
        sentiment = data['results'][j]['enriched_text']['sentiment']['document']['score']
        source = data['results'][j]['url']
        type = 'Article'
        document_id = data['results'][j]['id']
        name = data['results'][j]['title']
        category = data['results'][j]['enriched_text']['categories'][0]['label']

        nodes.append(
            {'date': date, 'summary': summary, 'sentiment': sentiment, 'source': source, 'type': type,
             'label': name[0:15],
             'documentID': document_id, 'category': category, 'id': j, 'level': 1})
        count += 1
    concepts = []
    for j in range(len(articles)):
        entities = data['results'][j]['enriched_text']['entities']
        label_count += len(entities)
        # print(label_count)
        # word = request.json['results'][1]['enriched_text']['entities'][i]['text']
        concepts.append([])
        for k in range(len(data['results'][j]['enriched_text']['concepts'])):
            concepts[j].append(data['results'][j]['enriched_text']['concepts'][k]['text'])


        for i in range(len(entities)):
            # print(words[i])

            if entities[i]['relevance'] > 0.05:
                type_rel = entities[i]['type']  # type of extracted nodes
                relevance = entities[i]['relevance']
                if type_rel == 'Person' or type_rel == 'Location' or type_rel == 'Organization' or type_rel == 'Company':
                    if j != 0:
                        if entities[i]['text'] not in words:
                            words.append(entities[i]['text'])
                            nodes.append({'id': count, 'label': words[-1], 'level': 2, 'type': type_rel, 'relevance': relevance})
                            # print(words[-1])
                            # print(nodes[-1])
                            links.append({'source': count, 'target': j})
                            count += 1
                        else:
                            conn_source = words.index(entities[i]['text'])
                            # print(words[conn_source])
                            links.append({'source': len(data['results']) + conn_source, 'target': j})
                            # print(links[-1])

                    else:
                        words.append(entities[i]['text'])
                        nodes.append({'id': count, 'label': words[-1], 'level': 2, 'type': type_rel , 'relevance': relevance})
                        # print(nodes[-1])
                        links.append({'source': count, 'target': j})
                        count += 1
        # print(articles[j])
        print("-----------------------------------------")
    # print(nodes)
    # print(links)
    print(concepts)
    return render_template('cloud.html', nodes=json.dumps(nodes, indent=2), links=json.dumps(links, indent=2),
                           articles=json.dumps(articles, indent=2), concepts=json.dumps(concepts, indent=2))


port = os.getenv('VCAP_APP_PORT', '8000')

if __name__ == '__main__':
    app.run(port=int(port), debug=True)
