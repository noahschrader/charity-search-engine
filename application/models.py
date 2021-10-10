from django.db import models

# Create your models here.


class Charities(models.Model):
    cnURL = models.URLField     # Charity Navigator URL
    mission = models.TextField  # Mission
    URL = models.URLField       # Website URL
    tagLine = models.TextField
    name = models.CharField(max_length=200)     # Charity Name
    state = models.CharField(max_length=2)      # State Charity is Located In
    city = models.CharField(max_length=50)      # City Charity is Located In
    zip = models.IntegerField       # Zip Code Charity is Located In
    add1 = models.CharField(max_length=200)     # Charity's First Address Line
    add2 = models.CharField(max_length=200)     # Charity's Second Address Line
    category = models.CharFiels(max_length=100)     # Charity's Category
