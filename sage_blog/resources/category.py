from import_export import fields, resources

from sage_blog.utils.import_export.errors import DataProcessingError
from sage_blog.utils.import_export.widget import ForeignKeyNullableWidget
from sage_blog.utils.import_export.exclude_fields import get_language_specific_fields
from sage_blog.models import PostCategory


class PostCategoryResource(resources.ModelResource):

    @classmethod
    def get_error_result_class(cls):
        return DataProcessingError

    class Meta:
        model = PostCategory
        base_language_fields = ["title",]
        exclude = ("id",) + get_language_specific_fields(
            PostCategory,
            base_language_fields
        )
        import_id_fields = ("title",)
