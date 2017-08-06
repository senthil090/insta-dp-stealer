import requests
from flask import Flask, render_template,redirect
from bs4 import BeautifulSoup
import json

app = Flask(__name__)

@app.route('/')
def index():
	return "Use the following API /userName (example):: https://insta-stealer.herokuapp.com/senthilkumar_s_"

@app.route('/<user>')
def stealPhoto(user):
	try:
		url = "https://instagram.com/"+user
		page = requests.get(url)
	except:
		return "Not Found"

	if page:
		htmlPage = BeautifulSoup(page.content)
		tag = htmlPage.select("script")
		for data in tag:
			if data.getText().find("window._sharedData") != -1:
				instaDetails = scrap_dp_link(data.getText()).replace("https://scontent-iad3-1.cdninstagram.com/","https://instagram.fmaa2-1.fna.fbcdn.net/");
				##return instaDetails;
				return redirect(instaDetails.replace("/s","/m"),code=302)

	return user


def scrap_dp_link(text):
	string_length = text.find("=")
	textData = text[string_length+1:len(text)-1]
	textJson = json.loads(textData)
	dpData = textJson["entry_data"]["ProfilePage"][0];
	dpDataLink = dpData["user"]["profile_pic_url_hd"]
	return dpDataLink

if __name__ == '__main__':
    app.run(debug=True)