"""
FAQ Model Definition
"""

from django.db import models
from django.utils.translation import gettext_lazy as _

from sage_tools.mixins.models.base import TimeStampMixin


class PostFaq(TimeStampMixin):
    """
    FAQ Model.

    Represents a Frequently Asked Question (FAQ) entry. Each entry consists of a
    question and its corresponding answer. This model is useful for managing
    common queries that users might have, providing a quick and accessible resource
    for both site visitors and administrators.
    """

    question = models.CharField(
        _("Question"),
        max_length=150,
        help_text=_(
            "Enter the FAQ question. Keep it clear and concise to aid easy understanding."
        ),
        db_comment="The question of the FAQ. Limited to 80 characters.",
    )

    answer = models.TextField(
        _("Answer"),
        help_text=_(
            "Provide a detailed answer to the FAQ question. Aim for clarity and completeness."
        ),
        db_comment="Detailed answer to the FAQ question. Limited to 180 characters.",
    )

    post = models.ForeignKey(
        "Post",
        on_delete=models.CASCADE,
        related_name="faqs",
        verbose_name=_("Post"),
        help_text=_("Choose the post of the faq."),
        db_comment="The post to which the faq belongs.",
    )

    class Meta:
        """Meta Information"""

        verbose_name = _("FAQ")
        verbose_name_plural = _("FAQ")
        db_table = "sage_post_faqs"
        db_table_comment = "Table storing frequently asked questions and their answers for user reference."

    def __str__(self):
        """Cast to String"""
        return str(self.question)

    def __repr__(self):
        """Object Representation"""
        return f"<FAQ: {self.question}>"
