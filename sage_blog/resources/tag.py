from import_export import resources

from sage_blog.utils.import_export.errors import DataProcessingError
from sage_blog.utils.import_export.exclude_fields import get_language_specific_fields
from sage_blog.models import PostTag


class PostTagResource(resources.ModelResource):
    @classmethod
    def get_error_result_class(cls):
        return DataProcessingError

    class Meta:
        model = PostTag
        base_language_fields = ["title",]
        exclude = ("id",) + get_language_specific_fields(
            PostTag,
            base_language_fields
        )
        import_id_fields = ("title",)
