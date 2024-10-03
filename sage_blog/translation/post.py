"""
Post Category Translation
"""
from modeltranslation.translator import TranslationOptions, register

from sage_blog.models import Post


@register(Post)
class PostTranslationOptions(TranslationOptions):
    """
    Post Category Translation Option
    """

    fields = ("title", "description", "summary", "alternate_text")
