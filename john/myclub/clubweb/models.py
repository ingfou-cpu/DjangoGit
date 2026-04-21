from django.db import models
# venue = Lieu fr
class Venue(models.Model):
    name = models.CharField('Venue name', max_length=100)
    address = models.CharField('Venue address', max_length=100)
    zip_code = models.CharField('zip code', max_length=15)
    phone = models.CharField('contact phone', max_length=20, blank=True)
    web = models.URLField('website address', blank=True)
    email_address = models.EmailField('email address', blank=True)
    def __str__(self):
        return self.name

class MyClubuser(models.Model):
    first_name = models.CharField('First name', max_length=100)
    last_name = models.CharField('Last name', max_length=100)
    email = models.EmailField('Email address', blank=True)
    def __str__(self):
        return self.first_name + ' ' + self.last_name
        #return f"{self.first_name} {self.last_name}"

# Event = evenement # ForeignKey= clé étrangère one to many # ManyToManyField = plusieurs à plusieurs fr
class Event(models.Model):
    name = models.CharField('Event name', max_length=100)
    event_date = models.DateTimeField('Event date and time')
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, blank=True, null=True)
    manager = models.CharField('Event manager', max_length=60)
    description = models.TextField('Event description', blank=True)
    attendees = models.ManyToManyField(MyClubuser, blank=True) # participants
    def __str__(self):
        return self.name
    

    

