import pymongo
import pprint
import nltk
import pyaudio
from nltk.tokenize import word_tokenize,sent_tokenize
from pymongo import MongoClient
import speech_recognition as sr
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render,render_to_response
from .forms import usernameform,textinputform
import pocketsphinx
from nltk.stem import WordNetLemmatizer

#global collection
#global command
#global name
def feedback(request):
	print("in feeedback")
	#collection = mongoconnections()
	client = MongoClient('localhost',27017)
	database = client['mydb']
	collection = database.feedback
	#request.session['collection'] = collection
	if request.method == 'POST':
		print("inside post method")
		form = usernameform(data =request.POST)
		if form.is_valid():
			name = form.cleaned_data['username']
			#try:
			if request.session.test_cookie_worked():
				request.session['username'] = name


			
			#	request.session.save()
			#except:
			#	print("\n\nerror in session")
			username = collection.find_one({"username":name})
			if username:
				print("===existing user===")
				return render(request,'spchrcgntn/selection.html')

			else:
				print("===new user===")
				insertion = collection.insert_one({"username":name})
				return render(request,'spchrcgntn/selection.html')
				
		else:
			return render(request,'spchrcgntn/feedback.html',{'form':form})
	else:
		form = usernameform()
	request.session.set_test_cookie()
	return render(request,'spchrcgntn/feedback.html',{'form':form})



def typeselection(request):
	return render(request,'spchrcgntn/selection.html')

def speechinput(request):
	return render(request,'spchrcgntn/speechinput.html')
def spprocess(request):
	recognizer = sr.Recognizer()
	print("\nEntered spprocess")
	with sr.Microphone() as source:
		recognizer.adjust_for_ambient_noise(source)
		print('\n listening voice now')
		audio = recognizer.listen(source,phrase_time_limit = 10)
		try:
			print('\nrecognizing voice')
			command = recognizer.recognize_google(audio,)
		except:
			command = "couldn't recognize you"
		#collection = getcollection()
		#name = getusername()
		client = MongoClient('localhost',27017)
		database = client['mydb']
		collection = database.feedback
		name = request.session['username']
		collection.update_one({"username":name},{'$set':{"rawtext":command}})
		_objects = tokenizingwords(command)
		collection.update_one({"username":name},{'$set':{"objects":_objects}})
		return render(request,'spchrcgntn/successpage.html',{'command':command})

def textinput(request):
	if request.method == 'POST':
		form = textinputform(request.POST)
		if form.is_valid():
			command = form.cleaned_data['feedback']
			#collection = getcollection()
			#name = getusername()
			client = MongoClient('localhost',27017)
			database = client['mydb']
			collection = database.feedback
			name = request.session['username']
			collection.update_one({"username":name},{'$set':{"rawtext":command}})
			_objects = tokenizingwords(command)
			collection.update_one({"username":name},{'$set':{"objects":_objects}})
			return render(request,'spchrcgntn/successpage.html',{'command':command})

		else:
			return render(request,'spchrcgntn/textinput.html',{'form':form})

	else:
		form = textinputform()
	return render(request,'spchrcgntn/textinput.html',{'form':form})
def successpage(request):
	process()
	return render(request,'spchrcgntn/successpage.html',{'command':command})






def tokenizingwords(command):
	stop_words = set(stopwords.words('english'))
	word_tokens = word_tokenize(command)
	filtered_words = []
	for word in word_tokens:
		if word not in stop_words:
			filtered_words.append(word)
	#ps = PorterStemmer()
	lemmatizer = WordNetLemmatizer()
	stem_words = []
	for word in filtered_words:
		stem_words.append(lemmatizer.lemmatize(word,pos='v'))
	finalwords = {}
	for word in stem_words:
		if word not in finalwords.keys():
			finalwords[word] = 1

		else:
			finalwords[word]+=1
	return str(finalwords)



