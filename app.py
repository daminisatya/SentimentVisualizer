import os,binascii
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, Blueprint
from flask import send_from_directory
import datetime, chartkick
import json
from pprint import pprint
import logging
from loklak import Loklak
from collections import Counter

app = Flask(__name__)
ck = Blueprint('ck_page', __name__, static_folder=chartkick.js(), static_url_path='/static')
app.register_blueprint(ck, url_prefix='/ck')
app.jinja_env.add_extension("chartkick.ext.charts")

@app.route('/visualize', methods=['POST'])
def visualize():
	q = request.form['q']
	l = Loklak()
	data = l.search(q)
	statuses = data['statuses']
	emotions = []
	languages = []
	countries = []
	for status in statuses:
		try:
			emotion = status['classifier_emotion']
			language = status['classifier_language']
			place = status['place_country']
			emotions.append(emotion)
			languages.append(language)
			countries.append(place)
		except:
			pass
	pprint(emotions)
	pprint(languages)
	pprint(countries)
	try:
		languageDict = dict(list(Counter(languages).items()))
		pprint(languageDict)
	except:
		pass
	try:
		emotionDict = dict(list(Counter(emotions).items()))
		pprint(emotionDict)
	except:
		pass
	try:
		countryDict = dict(list(Counter(countries).items()))
		pprint(countryDict)
	except:
		pass
	languageInfo = {}
	emotionInfo = {}
	countryInfo = {}
	for key, value in languageDict.iteritems():
		languageInfo[str(key)] = value
	for key, value in emotionDict.iteritems():
		emotionInfo[str(key)] = value
	for key, value in countryDict.iteritems():
		countryInfo[str(key)] = value
	return render_template('result.html', q=q, languages=languageInfo, emotions=emotionInfo, country=countryInfo, statuses=statuses)

@app.route('/')
def home():
	return render_template('index.html')
@app.route('/about')
def about():
	return render_template('loklak.html')
if __name__ == '__main__':
    app.debug = True
    app.secret_key=os.urandom(24)
    # app.permanent_session_lifetime = datetime.timedelta(seconds=200)
    app.run()