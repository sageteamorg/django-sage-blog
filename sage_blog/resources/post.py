from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget

from sage_blog.utils.import_export.errors import DataProcessingError
from sage_blog.utils.import_export.exclude_fields import get_language_specific_fields
from sage_blog.models import PostCategory, PostTag, Post


class PostResource(resources.ModelResource):

    category = fields.Field(
        column_name="category",
        attribute="category",
        widget=ForeignKeyWidget(PostCategory, "title"),
    )

    tags = fields.Field(
        column_name="tags",
        attribute="tags",
        widget=ManyToManyWidget(PostTag, field="title", separator=";"),
    )

    @classmethod
    def get_error_result_class(cls):
        return DataProcessingError

    class Meta:
        model = Post
        base_language_fields = ["title", "summary", "description"]
        exclude = ("id",) + get_language_specific_fields(Post, base_language_fields)
        import_id_fields = ("title",)
