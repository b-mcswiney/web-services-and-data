from django.db import models
from django.conf import settings

# Create your models here.
class Story(models.Model):
    id = models.AutoField(primary_key=True)
    headline = models.CharField(max_length=64)
    category = models.CharField(max_length=10,
                                choices=(("pol", "pol"),
                                         ("art", "art"),
                                         ("art", "tech"),
                                         ("trivia", "trivia")))
    region = models.CharField(max_length=2,
                              choices=(("uk","uk"),
                                       ("eu", "eu"),
                                       ("w", "w")))
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    details = models.TextField(max_length=128)

    def __str__(self):
        return self.headline
