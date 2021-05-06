from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.conf import settings
from django.urls import reverse
from tag.models import Tag

User = get_user_model()

class BaseQNA(models.Model):

	description = models.TextField()
	author = models.ForeignKey(
		User, 
		on_delete = models.CASCADE, 
		related_name="%(app_label)s_%(class)s_related",)
	created = models.DateTimeField(default = timezone.now)

	class Meta:
		abstract = True

class BaseVote(models.Model):
	upvote = models.ManyToManyField(
		User, 
		blank = True, 
		related_name = "%(app_label)s_%(class)s_up")
	downvote = models.ManyToManyField(
		User, 
		blank = True, 
		related_name = "%(app_label)s_%(class)s_down")

	class Meta:
		abstract = True

class Question(BaseQNA, BaseVote):

	title = models.CharField(max_length = 250)
	slug = models.SlugField(max_length = 250)
	tag = models.ManyToManyField(Tag, related_name = "tagged")
	follower = models.ManyToManyField(
		User, 
		blank = True,
		related_name = "followers")
	favorite = models.ManyToManyField(
		User,
		blank = True,
		related_name = "favorited_users")

	def save(self,*args, **kwargs):
		from django.utils.text import slugify
		self.slug = slugify(self.title)
		super(Question,self).save(*args, **kwargs)

	def __str__(self):
		return str(self.pk) + '_' + self.title


class Answer(BaseQNA, BaseVote):

	accepted = models.BooleanField(default = False)
	question = models.ForeignKey(
		Question,
		on_delete = models.CASCADE,
		related_name = "answered_question",
		null = True)

class Comment(BaseQNA, BaseVote):
	question = models.ForeignKey(
		Question,
		on_delete = models.CASCADE,
		related_name = "commented_question",
		null = True)