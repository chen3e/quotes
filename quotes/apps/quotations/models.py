from django.db import models
from apps.login_reg.models import *
import re

NAME_REGEX = re.compile(r'^[\sa-zA-Z.]+$')

class QuoteManager(models.Manager):
    def validator(self, postData):
        errors = {}
        if len(postData['author']) < 3:
            errors['author'] = "Author name must be more than 3 characters!"
        if not NAME_REGEX.match(postData['author']):
            errors["author"] = "Invalid author name"
        if len(postData['quote']) < 10:
            errors['quote'] = "Quotation must be more than 10 characters!"
        return errors

class Quote(models.Model):
    author = models.CharField(max_length = 45)
    quote = models.TextField()
    uploader = models.ForeignKey(User, related_name = "uploaded_quote")
    liked_users = models.ManyToManyField(User, related_name = "liked_quotes")
    objects = QuoteManager()