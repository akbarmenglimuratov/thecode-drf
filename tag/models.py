from django.db import models

class Tag(models.Model):
	name = models.CharField(max_length = 20)
	slug = models.SlugField(max_length = 30)

	class Meta:
		app_label = 'tag'

	def __str__(self):
		return self.name

	def save(self,*args, **kwargs):
		from django.utils.text import slugify
		self.slug = slugify(self.name)
		super(Tag, self).save(*args, **kwargs)
