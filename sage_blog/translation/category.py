"""
Post Category Translation
"""
from modeltranslation.translator import TranslationOptions, register

from sage_blog.models import PostCategory


@register(PostCategory)
class PostCategoryTranslationOptions(TranslationOptions):
    """
    Post Category Translation Option
    """

    fields = ("title",)
