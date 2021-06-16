from db import get_naver, get_twitter
import db
from jinja2 import Environment, FileSystemLoader
from flask import Flask, render_template, redirect, url_for
import shutil
import os
import datetime
app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)