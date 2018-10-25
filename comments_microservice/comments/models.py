from django.db import models
from vote.models import VoteModel

class Comment(VoteModel, models.Model):
    author = models.ForeignKey('auth.User', related_name='comments', on_delete=models.CASCADE)
    text = models.CharField(max_length=128)
    answerId = models.IntegerField(default=0)
    created = models.DateField(auto_now=False, null=True)
    edited = models.DateField(auto_now=False, null=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return str(self.id)
