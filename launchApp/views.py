from django.shortcuts import render
import os



BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def home(request):
	with open(BASE_DIR+'\\static\\about.txt', 'r') as source:
		about = source.read()
	with open(BASE_DIR+'\\static\\privacy.txt', 'r') as source:
		privacy = source.read()
	with open(BASE_DIR+'\\static\\term.txt', 'r') as source:
		term = source.read()
	return render(request , 'home.html',{'about': about,'privacy':privacy, 'term':term})
