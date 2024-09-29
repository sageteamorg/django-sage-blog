from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget

from sage_blog.utils.import_export.errors import DataProcessingError
from sage_blog.utils.import_export.exclude_fields import get_language_specific_fields

from sage_blog.models import PostFaq, Post


class PostFaqResource(resources.ModelResource):

    post = fields.Field(
        column_name="post",
        attribute="post",
        widget=ForeignKeyWidget(Post, "title"),
    )

    @classmethod
    def get_error_result_class(cls):
        return DataProcessingError

    class Meta:
        model = PostFaq
        base_language_fields = ["question", "answer"]
        exclude = ("id",) + get_language_specific_fields(
            PostFaq,
            base_language_fields
        )
        import_id_fields = ("question",)
