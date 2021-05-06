from django.db import models
from django.db.models.fields.related import RelatedField, ManyToManyRel
from django.utils.translation import gettext_lazy as _
from .models import Tag

class _TaggableManager(models.Manager):
    # TODO investigate whether we can use a RelatedManager instead of all this stuff
    # to take advantage of all the Django goodness
    def __init__(self, through, model, instance, prefetch_cache_name):
        super().__init__()
        self.through = through
        self.model = model
        self.instance = instance
        self.prefetch_cache_name = prefetch_cache_name

class TagManager(RelatedField):
	many_to_many = True
	many_to_one = False
	one_to_many = False
	one_to_one = False
    
	def __init__(
		self, 
		verbose_name=_("Tags"),
		help_text=_("A comma-separated list of tags."),
		through=None,
		blank=False,
		related_name=None,
		to=None,
		manager=_TaggableManager):

		self.through = through or Tag

		rel = ManyToManyRel(self, to, related_name=related_name, through=self.through)
		super().__init__(
			verbose_name=verbose_name,
			help_text=help_text,
			blank=blank,
			null=True,
			serialize=False,
			rel=rel
		)

	def __get__(self, instance, model):
		if instance is not None and instance.pk is None:
			raise ValueError(
			"%s objects need to have a primary key value "
			"before you can access their tags." % model.__name__
			)
		return self.manager(
			through=self.through,
			model=model,
			instance=instance,
			prefetch_cache_name=self.name,
		)
