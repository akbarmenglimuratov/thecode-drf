from django.contrib import admin
from . import models

@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):

	list_display = ['id', 'title', 'author']
	prepopulated_fields = { 'slug': ('title',), }

	fieldsets = (
        ('Main', {'fields': ('title', 'description', 'tag') }),
        ('Info', {'fields': ('author', 'created') }),
        ('Additional info', {'fields': ('slug', 'upvote', 'downvote', 'favorite', 'follower') }),
    )

	add_fieldsets = (
		(None, {
		'fields': ('title', 'description', 'author')
		})
	)

@admin.register(models.Answer)
class AnswerAdmin(admin.ModelAdmin):
	list_display = ['id', 'author', 'accepted', 'question']
	fieldsets = (
        ('Main', {'fields': ('question','description') }),
        ('Info', {'fields': ('author', 'created') }),
        ('Additional info', {'fields': ('accepted','upvote', 'downvote') }),
    )


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
	list_display = ['id', 'author']

	fieldsets = (
        ('Main', {'fields': ('question','description') }),
        ('Info', {'fields': ('author', 'created') }),
        ('Additional info', {'fields': ('upvote', 'downvote') }),
    )