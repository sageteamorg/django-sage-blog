"""
Post Tag Translation
"""
from modeltranslation.translator import TranslationOptions, register

from sage_blog.models import PostTag


@register(PostTag)
class PostTagTranslationOptions(TranslationOptions):
    """
    Post Tag Translation Option
    """

    fields = ("title",)
