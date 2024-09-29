from django.conf import settings

def get_language_specific_fields(model, base_fields):
    """
    Constructs a list of language-specific fields to exclude from import/export
    based on the available languages in the settings.

    :param model: The model class for which the fields are being generated.
    :param base_fields: A list of base field names to which language codes are appended.
    :return: A tuple of field names to exclude.
    """
    language_code = settings.LANGUAGE_CODE  # Default language code
    languages = settings.LANGUAGES  # List of all languages
    exclude_fields = []

    for lang_code, _ in languages:
        if lang_code != language_code:
            for base_field in base_fields:
                exclude_fields.append(f"{base_field}_{lang_code}")

    return tuple(exclude_fields)
