from django.db import models
from django.utils import timezone
import datetime

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text

class Suggestion(models.Model):
    name = models.CharField(max_length=100)
    text = models.CharField(max_length=500)
    def __str__(self):
        return self.suggestion_text


#class SuggestionList(models.Model):
#    name = models.CharField(max_length=1000)
#    def __str__(self):
#        return self.suggestion_text

#    suggestion_text = models.CharField(max_length=5q00)
#    def __str__(self):
#        return self.suggestion_text