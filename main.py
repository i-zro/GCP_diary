from flask import Flask, redirect, url_for, request, render_template, make_response, session, escape, Response
import csv
import json
from datetime import datetime
from functools import wraps
import sys
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import hashlib
import sys
import os
import time
from pytz import timezone
from nlp.analysis import *
import web
from web.db import get_naver, get_twitter
from jinja2 import Environment, FileSystemLoader
from flask import Flask, render_template, redirect, url_for
import shutil
import os
import datetime

fmt = "%Y-%m-%d %H:%M:%S %Z%z"
KST = datetime.datetime.now(timezone('Asia/Seoul'))
fmt = "%Y/%m/%d %H:%M:%S"

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


def render_maker_anger(list_n, list_t, sender, sertime, diary =""):
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('webpage_anger.html')
    output = template.render(naver=list_n, twitter=list_t)
    filename = './templates/'+str(sender)+sertime+'.html'
    print(filename)
    with open(filename,'w', -1, 'utf-8') as fh:
        fh.write(output)
def render_maker_happy(list_n, list_t, sender, sertime, diary =""):
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('webpage_happy.html')
    output = template.render(naver=list_n, twitter=list_t)
    filename = './templates/'+str(sender)+sertime+'.html'
    print(filename)
    with open(filename,'w', -1, 'utf-8') as fh:
        fh.write(output)
def render_maker_sad(list_n, list_t, sender, sertime, diary =""):
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('webpage_sad.html')
    output = template.render(naver=list_n, twitter=list_t)
    filename = './templates/'+str(sender)+sertime+'.html'
    print(filename)
    with open(filename,'w', -1, 'utf-8') as fh:
        fh.write(output)
def render_maker_neutral(list_n, list_t, sender, sertime, diary =""):
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('webpage_neutral.html')
    output = template.render(naver=list_n, twitter=list_t)
    filename = './templates/'+str(sender)+sertime+'.html'
    print(filename)
    with open(filename,'w', -1, 'utf-8') as fh:
        fh.write(output)
def render_maker_anxious(list_n, list_t, sender, sertime, diary =""):
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('webpage_anxious.html')
    output = template.render(naver=list_n, twitter=list_t)
    filename = './templates/'+str(sender)+sertime+'.html'
    print(filename)
    with open(filename,'w', -1, 'utf-8') as fh:
        fh.write(output)
def render_maker(list_n, list_t, sender, sertime, diary =""):
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('webpage.html')
    output = template.render(naver=list_n, twitter=list_t)
    filename = './templates/'+str(sender)+sertime+'.html'
    print(filename)
    with open(filename,'w', -1, 'utf-8') as fh:
        fh.write(output)

@app.route('/show/<username>/<sertime>')
def show(username, sertime):
    filename = str(username) + sertime + '.html'
    return render_template(filename, sertime=sertime)

@app.route('/sad/<username>/<sertime>')
def sad_show(username, sertime):
    list_n = get_naver('슬픔')
    list_t = get_twitter('슬픔')
    render_maker_sad(list_n=list_n, list_t=list_t, sender = username, sertime = sertime)
    return redirect(url_for('show', username=username, sertime=sertime))

@app.route('/neutral/<username>/<sertime>')
def neutral_show(username, sertime):
    list_n = get_naver('중립')
    list_t = get_twitter('중립')
    render_maker_neutral(list_n=list_n, list_t=list_t, sender = username, sertime = sertime)
    return redirect(url_for('show', username=username, sertime=sertime))

@app.route('/happy/<username>/<sertime>')
def happy_show(username, sertime):
    list_n = get_naver('행복')
    list_t = get_twitter('행복')
    render_maker_happy(list_n=list_n, list_t=list_t, sender = username, sertime = sertime)
    return redirect(url_for('show', username=username, sertime=sertime))

@app.route('/anxious/<username>/<sertime>')
def anxious_show(username, sertime):
    list_n = get_naver('불안')
    list_t = get_twitter('불안')
    render_maker_anxious(list_n=list_n, list_t=list_t, sender = username, sertime = sertime)
    return redirect(url_for('show', username=username, sertime=sertime))

@app.route('/angry/<username>/<sertime>')
def angry_show(username, sertime):
    list_n = get_naver('분노')
    list_t = get_twitter('분노')
    render_maker_anger(list_n=list_n, list_t=list_t, sender = username, sertime = sertime)
    return redirect(url_for('show', username=username, sertime=sertime))

# 나중에 옮길것 위에꺼

def as_json(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        res = f(*args, **kwargs)
        res = json.dumps(res, ensure_ascii=False).encode('utf8')
        return Response(res, content_type='application/json; charset=utf-8')
    return decorated_function

@app.route('/')
def hello():
    return 'Hello'

@app.route('/db', methods=['POST'])
@as_json
def getdb():
    email = request.form['email']
    return read_db(email)

@app.route('/send', methods=['POST'])
def receive():
    receive = request.form['text']
    print(receive)
    return receive
fmtt="%Y%MYd%H%M%S"
cred = credentials.Certificate("./serviceAccountKey.json")
firebase_admin.initialize_app(cred)
@app.route('/chat', methods=['POST'])
def index():
    time = request.form['timestamp']
    diary = request.form['diary']
    email = request.form['email']
    print(email)
    final = to_fire_answer(diary, False, 'izero3127@gmail.com', 'link')
    fire_calender(final, email)
    total_diary(email)
    return time, email
  


# 파이어 베이스 답변
def to_fire_answer(diary, isMe, sender, link):
    db = firestore.client()

    users_ref = db.collection("messages").order_by('createdOn')
    docs = users_ref.stream()
    result = []
    for doc in docs:
        if doc.to_dict()['isMe'] == True and doc.to_dict()['sender'] == sender:
            result.append(doc.to_dict())
            
    final = result[-1]
    
    
    emotion = sentence_sentiment(str(diary))
                                 
    if emotion == '슬픔':
        link = 'http://13.209.152.251:52674/sad/{0}/{1}'.format(sender, 1)
    elif emotion =='행복':
        link = 'http://13.209.152.251:52674/happy/{0}/{1}'.format(sender, 1)
    elif emotion =='분노':
        link = 'http://13.209.152.251:52674/angry/{0}/{1}'.format(sender, 1)
    elif emotion =='중립':
        link = 'http://13.209.152.251:52674/neutral/{0}/{1}'.format(sender, 1)
    else:
        link = 'http://13.209.152.251:52674/anxious/{0}/{1}'.format(sender, 1)
                                 
    doc_ref = db.collection(u'messages')
    doc_ref.add({
        u'diary': str(sentence_sentiment(str(diary))[0]),
        u'isMe': bool(isMe),
        u'sender': str(sender),
        u'timestamp': str(KST.strftime(fmt)),
        u'createdOn': firestore.SERVER_TIMESTAMP,
        u'emotion': str(emotion),
        u'link': str(link)
    })

    return final

def fire_calender(final, email):
    db = firestore.client()
    doc2_ref = db.collection(u'answers')
    doc2_ref.add({
        u'diary': final['diary'],
        u'sender': str(email),
        u'timestamp': str(KST.strftime(fmt)),
        u'y': str(int(KST.strftime("%Y"))),
        u'm': str(int(KST.strftime("%m"))),
        u'd': str(int(KST.strftime("%d"))),
        u't': str(KST.strftime("%H:%M:%S")),
        u'createdOn': firestore.SERVER_TIMESTAMP,
        u'type': str(sentence_sentiment(final['diary'])[0])
    })    
    
# 파이어 베이스 답변
def total_diary(sender):
    db = firestore.client()

    users_ref = db.collection("answers").order_by('createdOn')
    docs = users_ref.stream()
    result = []
    for doc in docs:
        if doc.to_dict()['sender'] == sender:
            result.append(doc.to_dict())
            # result[doc.to_dict()['type']] += 1
    total = len(result)
    
    data = {
        u'sender':str(sender),
        u'total': int(total)
    }
    e = u'{}'.format(sender)
    doc_ref = db.collection(u'total').document(e).set(data)

# 감성분석
def sentence_sentiment(sentence):
    data = {
        'title': 'Test',
        'text': sentence,
        'stickers': []
    }
    response = TextAnalysis(data)
    b = response.text_analysis()
    if response[0] == 1:
        return('슬픔')
    if response[1] == 1:
        return('중립')
    if response[2] == 1:
        return('행복')
    if response[3] == 1:
        return('불안')
    if response[4] == 1:
        return('분노')
    if response[5] == 1:
        return('예외')

    print(b)
    feel = ""
    word_list = []
    if b['feel'][0][0] == 1 or b['feel'][0][0] == 3:
        feel = "행복"
    elif b['feel'][0][0] == 2:
        feel = "슬픔"
    elif b['feel'][0][0] == 4:
        feel = "지루"
    elif b['feel'][0][0] == 5:
        feel = "분노"
    elif b['feel'][0][0] == 6:
        feel = "공포"
    else:
        feel = "중립"
    print(feel)
    for num, i in enumerate(b['word_count']):
        word_list.append(i[0])
        if num>=2:
            break
    return feel, word_list


if __name__ == '__main__':
    app.run(debug=True)
