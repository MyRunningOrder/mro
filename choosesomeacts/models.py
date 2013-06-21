from django.db import models
# Create your models here.

class Artist(models.Model):
	Name = models.CharField(max_length=150)
	HomepageURL = models.CharField(max_length=250, blank=True)
	FacebookURL = models.CharField(max_length=250, blank=True)
	SoundCloudURL = models.CharField(max_length=250, blank=True)
	DateTimeAdded = models.DateTimeField(auto_now_add = True)
	DateTimeLastEdited = models.DateTimeField(auto_now = True)
	def __unicode__(self):
		return self.Name
	
class ArtistDescription(models.Model):
	Artist = models.ForeignKey('Artist')
	Language = models.CharField(max_length=50)
	Text = models.CharField(max_length=1000)
	DateTimeAdded = models.DateTimeField(auto_now_add = True)
	DateTimeLastEdited = models.DateTimeField(auto_now = True)
	def __unicode__(self):
		return self.Artist.Name + " (" + self.Language + "): " + self.Text

class ArtistSample(models.Model):
	Artist = models.ForeignKey('Artist')
	PastedString = models.CharField(max_length=1000, blank=True)
	EmbedCode = models.CharField(max_length=1000, blank=True)
	DateTimeAdded = models.DateTimeField(auto_now_add = True)
	DateTimeLastEdited = models.DateTimeField(auto_now = True)
	def __unicode__(self):
		return self.EmbedCode

class Festival(models.Model):
	Name = models.CharField(max_length=150)
	URL = models.CharField(max_length=250, blank=True)
	DateTimeAdded = models.DateTimeField(auto_now_add = True)
	DateTimeLastEdited = models.DateTimeField(auto_now = True)
	def __unicode__(self):
		return self.Name

class FestivalEdition(models.Model):
	Festival = models.ForeignKey('Festival')
	Year = models.IntegerField(default=666)
	Location = models.CharField(max_length=150)
	FromDate = models.DateField()
	ToDate = models.DateField()
	DateTimeAdded = models.DateTimeField(auto_now_add = True)
	DateTimeLastEdited = models.DateTimeField(auto_now = True)
	def __unicode__(self):
		return self.Festival.Name + " " + self.Location + " " + str(self.Year)

class Stage(models.Model):
	Festival = models.ForeignKey('Festival')
	Name = models.CharField(max_length=150)
	def __unicode__(self):
		return self.Festival.Name + " Stage: " + self.Name
	
class RunningOrderEntry(models.Model):
	FestivalEdition = models.ForeignKey('FestivalEdition')
	Stage = models.ForeignKey('Stage')
	Artist = models.ForeignKey('Artist')
	FromDateTime = models.DateTimeField()
	ToDateTime = models.DateTimeField()
	def __unicode__(self):
		return self.Artist.Name + " playing at " + self.FestivalEdition.Festival.Name + " on stage " + self.Stage.Name
	
