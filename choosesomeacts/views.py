# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from choosesomeacts.models import *
from bs4 import BeautifulSoup
import urllib2
import datetime
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login

class OverviewListItem(models.Model):
	Artist = models.ForeignKey('Artist')
	ArtistDescription = models.ForeignKey('ArtistDescription')
	Sample1 = models.ForeignKey('ArtistSample')
	Sample2 = models.ForeignKey('ArtistSample')
	Sample3 = models.ForeignKey('ArtistSample')
	def __unicode__(self):
		return self.Artist.Name
		
class SearchHelpListItem(models.Model):
	Artist = models.CharField(max_length=1000)
	ArtistDescription = models.CharField(max_length=1000)
	ArtistHomepage = models.CharField(max_length=1000)
	ArtistNumber = models.IntegerField()
	ArtistPreference = models.CharField(max_length=1000)
	def __unicode__(self):
		return self.Artist

def index(request):
	request.session.set_test_cookie()
	#request.session['testDingens'] = "hat geklappt"
	#print request.session['testDingens']
	return render(request, 'choosesomeacts/index.html')
		
def showActs(request):
	# generischer Ansatz fuer Daten, die aus der Datenbank kommen
	
	SelectedFestival = "Fusion"
	SelectedFestivalEditionYear = 2013
	SelectedFestivalEditionLocation = "Kulturkosmos Laerz"
		
	OverviewList = []
	ArtistList = Artist.objects.order_by('Name')
		
	for Entry in ArtistList:
		print Entry.Name
		
		DescList = ArtistDescription.objects.filter(Artist = Entry)[:1]
		if len(DescList) > 0:
			Desc = DescList[0]
			print Desc.Text
		else:
			Desc = ArtistDescription()
		
		TheSampleList = ArtistSample.objects.filter(Artist = Entry)[:3]
		if len(TheSampleList) > 0:
			Samp1 = TheSampleList[0]
			print Samp1.EmbedCode
		else:
			Samp1 = ArtistSample()
		
		if len(TheSampleList) > 1:
			Samp2 = TheSampleList[1]
			print Samp2.EmbedCode
		else:
			Samp2 = ArtistSample()
		
		if len(TheSampleList) > 2:
			Samp3 = TheSampleList[2]
			print Samp3.EmbedCode
		else:
			Samp3 = ArtistSample()
	
		OverviewListEntry = OverviewListItem(Artist = Entry, ArtistDescription = Desc, Sample1 = Samp1, Sample2 = Samp2, Sample3 = Samp3)
		OverviewList.append(OverviewListEntry)
	
	context = {'ArtistList': ArtistList,
	'OverviewList': OverviewList,
	'SelectedFestival': SelectedFestival,
	'SelectedFestivalEditionYear': SelectedFestivalEditionYear,
	'SelectedFestivalEditionLocation': SelectedFestivalEditionLocation}
	return render(request, 'choosesomeacts/actsoverview.html', context)
	
def showActsNew(request):
	# geht momentan nur fuer die Fusion, funktionert ueber das Crawlen der Website	
	ArtistNumber = 0
	TestCookieWorked = request.session.test_cookie_worked()
	#print "Test cookie worked? " + str(request.session.test_cookie_worked())
	#if request.session.__contains__('testDingens'):
		#print request.session['testDingens']
	
	SelectedFestival = "Fusion"
	SelectedFestivalEditionYear = 2013
	SelectedFestivalEditionLocation = "Kulturkosmos Laerz"
		
	SearchHelpList = []
	URLList = ["http://www.fusion-festival.de/de/2013/programm/live/", "http://www.fusion-festival.de/de/2013/programm/dj/", "http://www.fusion-festival.de/de/2013/programm/band/"]
	
	for URL in URLList:
		TempURL = urllib2.urlopen(URL)
		TempContent = TempURL.read()
		Soup = BeautifulSoup(TempContent)
	
		#show the site that is being crawled..
		#print Soup.title.string
	
		#find all divs that have act information
		FoundSomething = Soup.find_all("div", class_="inner border")
		#pop the first one as it is the page title
		FoundSomething.pop(0)
		for Entry in FoundSomething:
			ArtistNumber += 1
			NewEntry = SearchHelpListItem(Artist = Entry.h3.string, ArtistNumber = ArtistNumber)
			Entry.p.string
			NewEntry.ArtistDescription = Entry.p.string
			for a in Entry.findAll('a',href=True):
				NewEntry.ArtistHomepage = a['href']
				
			if request.session.__contains__("Artist_" + NewEntry.Artist):
				NewEntry.ArtistPreference = request.session["Artist_" + NewEntry.Artist]
				#print request.session["Artist_" + NewEntry.Artist]

			SearchHelpList.append(NewEntry)
	
	
	SearchHelpList.sort(key=lambda SearchHelpListItem: SearchHelpListItem.Artist)
	context = {'SearchHelpList': SearchHelpList,
	'SelectedFestival': SelectedFestival,
	'SelectedFestivalEditionYear': SelectedFestivalEditionYear,
	'SelectedFestivalEditionLocation': SelectedFestivalEditionLocation,
	'TestCookieWorked': TestCookieWorked}
	return render(request, 'choosesomeacts/actsoverview-searchhelp.html', context)

@csrf_exempt	
def update_session(request):
	if not request.is_ajax() or not request.method=='POST':
		return HttpResponseNotAllowed(['POST'])

	Artist = request.POST['Artist']
	Preference = request.POST['Preference']
	request.session["Artist_" + Artist] = Preference
	
	if request.user.is_authenticated():
		# missing: if user is logged in, sync session data and user data
		print "got an authed user"


	return HttpResponse('ok')
	
def showMyActs(request):
	SelectedFestival = "Fusion"
	SelectedFestivalEditionYear = 2013
	SelectedFestivalEditionLocation = "Kulturkosmos Laerz"
	
	YesList = []
	NoList = []
	MaybeList = []
	AllInSession = request.session.keys()
	
	for n in range(0, len(AllInSession)):
		if (str(AllInSession[n])[0:7] == "Artist_"):
			ArtistName = AllInSession[n][7:]
			Preference = request.session.__getitem__(AllInSession[n])
			if Preference == "yes":
				YesList.append(ArtistName)
			elif Preference == "no":
				NoList.append(ArtistName)
			elif Preference == "maybe":
				MaybeList.append(ArtistName)
	
	
	
	
	
	
	context = {'YesList': YesList,'NoList': NoList,'MaybeList': MaybeList,
	'SelectedFestival': SelectedFestival,
	'SelectedFestivalEditionYear': SelectedFestivalEditionYear,
	'SelectedFestivalEditionLocation': SelectedFestivalEditionLocation,}	
	return render(request, 'choosesomeacts/myacts.html', context)

def loginUserView(request):
	# this view basically shows the login-form if the user is not logged in
	print "here we could sign in a user.."
	return render(request, 'choosesomeacts/login.html')
	
def loginUserAndCopyData(request):
	#first case: create a new user
	# 1. create user
	# 2. copyy his session data into his user data
	
	#second case: try to log in a user
	
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(username, password)
	if user is not None:
		# the password verified for the user
		if user.is_active:
			login(request, user)
			print("User is valid, active and authenticated")
		else:
			print("The password is valid, but the account has been disabled!")
	else:
		# the authentication system was unable to verify the username and password
		print("The username and password were incorrect.")
	
	# if login fails, give feedback
	
	#if login successful, load user data into session data
	
	return render(request, 'choosesomeacts/login.html')