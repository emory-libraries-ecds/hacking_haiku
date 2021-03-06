from django.db import models
from django.utils.safestring import mark_safe 
from django_date_extensions import fields as ddx
from haiku.apps.geo.models import Structure, City, Area, Province
from haiku.apps.people.models import Person
from adminsortable.models import Sortable


class KigoManager(models.Manager):
     def get_by_natural_key(self, japanese):
        return self.get(japanese=japanese)

     
class Kigo(models.Model):

    objects = KigoManager()

    SEASON_CHOICES = (
        ('Fall', 'Fall'),
        ('Spring', 'Spring'),
        ('Summer', 'Summer'),
        ('Winter', 'Winter'),
        ('New Year', 'New Year')

    )

    japanese = models.CharField(max_length=50)
    english = models.CharField(max_length=50, blank=True)
    romanization = models.CharField(max_length=50, blank=True)
    season = models.CharField(max_length=10, choices=SEASON_CHOICES, blank=True)
    notes = models.TextField(blank=True)

    # generate natural key
    def natural_key(self):
        return (self.japanese)
    
    def __unicode__(self):
        return self.japanese

    class Meta:
        ordering = ['japanese']

        
class WorkManager(models.Manager):
     def get_by_natural_key(self, english_title):
        return self.get(english_title=english_title)

     
class Work(models.Model):

    objects = WorkManager()

    japanese_title = models.CharField(max_length=255, blank=True)
    english_title = models.CharField(max_length=255)
    romanized_title = models.CharField(max_length=255, blank=True)
    authors = models.ManyToManyField(Person, blank=True, null=True, verbose_name='Author(s)')
    japanese_date = models.CharField(max_length=255, blank=True)
    roman_date = ddx.ApproximateDateField(blank=True, null=True, help_text=mark_safe('YYYY, MM/YYYY, DD/MM/YYYY<br>Visit <a href="http://keisan.casio.jp/exec/system/1239884730" target="_blank">Keisan website</a> to convert'))
    notes = models.TextField(blank=True)

    # generate natural key
    def natural_key(self):
        return (self.english_title)
    
    def __unicode__(self):
        return self.english_title

    def dates_converted(self):
        if self.japanese_date != None and self.japanese_date != '' and \
          self.roman_date == None or self.roman_date == '':             
            return False
        else:
            return True
    dates_converted.boolean = True
    dates_converted.short_description = 'JCal'
    
    class Meta:
        ordering = ['english_title']

        
class VerseManager(models.Manager):
     def get_by_natural_key(self, japanese_text):
        return self.get(japanese_text=japanese_text)

     
class Verse(Sortable):

    objects = VerseManager()

    class Meta(Sortable.Meta):
        pass

    japanese_text = models.CharField(max_length=255)
    english_text = models.TextField(blank=True)
    romanization = models.TextField(blank=True)
    author = models.ForeignKey(Person, blank=True, null=True)
    work = models.ForeignKey(Work, blank=True, null=True)
    other_works = models.ManyToManyField(Work, related_name='other_works', verbose_name='Additional Publications', null=True, blank=True)
    japanese_date = models.CharField(max_length=255, blank=True)
    roman_date = ddx.ApproximateDateField(blank=True, null=True, help_text=mark_safe('YYYY, MM/YYYY, DD/MM/YYYY<br>Visit <a href="http://keisan.casio.jp/exec/system/1239884730" target="_blank">Keisan website</a> to convert'))
    kigo = models.ForeignKey(Kigo, blank=True, null=True)
    genre = models.CharField(max_length=255, blank=True)
    encounters = models.ManyToManyField(Person, related_name='encounters', blank=True, null=True)
    structures = models.ManyToManyField(Structure, blank=True, null=True)
    cities = models.ManyToManyField(City, blank=True, null=True)
    provinces = models.ManyToManyField(Province, blank=True, null=True)
    areas = models.ManyToManyField(Area, blank=True, null=True, help_text=mark_safe('Non-province areas such as lakes and mountains<br>'))
    allusions = models.ManyToManyField(Work, related_name='allusions', blank=True, null=True)
    notes = models.TextField(blank=True)

    # generate natural key
    def natural_key(self):
        return (self.japanese_text)
    
    def __unicode__(self):
        return self.romanization

    def dates_converted(self):
        if self.japanese_date != None and self.japanese_date != '' and \
          self.roman_date == None or self.roman_date == '':             
            return False
        else:
            return True
    dates_converted.boolean = True
    dates_converted.short_description = 'JCal'


    

        
class AltVerseManager(models.Manager):
     def get_by_natural_key(self, japanese_text):
        return self.get(japanese_text=japanese_text)

     
class AltVerse(models.Model):
    '''Alternate form of a verse'''

    objects = AltVerseManager()

    japanese_text = models.TextField()
    english_text = models.TextField(blank=True)
    romanization = models.TextField(blank=True)
    verse = models.ForeignKey(Verse)

    # generate natural key
    def natural_key(self):
        return (self.japanese_text)
    
    def __unicode__(self):
        return self.japanese_text

    class Meta:
       ordering = ['japanese_text']

       
        
