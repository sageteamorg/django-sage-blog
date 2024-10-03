"""
PostFaq Translation
"""
from modeltranslation.translator import TranslationOptions, register

from sage_blog.models import PostFaq


@register(PostFaq)
class PostFaqTranslationOptions(TranslationOptions):
    """
    PostFaq Translation Option
    """

    fields = (
        "question",
        "answer",
    )
