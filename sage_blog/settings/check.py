from django.conf import settings
from django.core.checks import Error, Warning as CheckWarning
from django.core.checks import register
from django.db import OperationalError, connection


@register()
def check_postgres_extensions(app_configs, **_kwargs):
    errors = []
    warnings = []

    # Check the DATABASE engine
    database_engine = settings.DATABASES["default"]["ENGINE"]
    if "postgresql" in database_engine:
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1 FROM pg_extension WHERE extname='pg_trgm';")
                result = cursor.fetchone()
                if not result:
                    errors.append(
                        Error(
                            "pg_trgm extension is not installed",
                            hint="Run `CREATE EXTENSION pg_trgm;` in your PSQL database.",
                            id="postgres.E001",
                        )
                    )
        except OperationalError as error:
            errors.append(
                Error(
                    f"Error checking pg_trgm extension: {error}",
                    hint="Ensure your database is running and accessible.",
                    id="postgres.E002",
                )
            )
    else:
        warnings.append(
            CheckWarning(
                "Database engine is not PostgreSQL.",
                hint="PostgreSQL improves search in `django-sage-blog`, but it's optional.",
                id="postgres.W001",
            )
        )

    return errors + warnings

@register()
def check_required_settings(app_configs, **_kwargs):
    errors = []
    warnings = []

    # Check LANGUAGE_CODE
    if not hasattr(settings, "LANGUAGE_CODE"):
        errors.append(
            Error(
                "LANGUAGE_CODE setting is missing.",
                hint="Add LANGUAGE_CODE in your settings file.",
                id="settings.E001",
            )
        )
    
    # Check LANGUAGES
    if not hasattr(settings, "LANGUAGES"):
        errors.append(
            Error(
                "LANGUAGES setting is missing.",
                hint="Add LANGUAGES in your settings file.",
                id="settings.E002",
            )
        )

    # Check CKEDITOR_5_STORAGE_BACKEND
    if not hasattr(settings, "CKEDITOR_5_STORAGE_BACKEND"):
        errors.append(
            Error(
                "CKEDITOR_5_STORAGE_BACKEND setting is missing.",
                hint="Add CKEDITOR_5_STORAGE_BACKEND in your settings file.",
                id="settings.E003",
            )
        )

    # Check MODELTRANSLATION_CUSTOM_FIELDS
    if not hasattr(settings, "MODELTRANSLATION_CUSTOM_FIELDS"):
        errors.append(
            Error(
                "MODELTRANSLATION_CUSTOM_FIELDS setting is missing.",
                hint="Add MODELTRANSLATION_CUSTOM_FIELDS in your settings file.",
                id="settings.E004",
            )
        )
    elif settings.MODELTRANSLATION_CUSTOM_FIELDS != "django_ckeditor_5.fields.CKEditor5Field":
        errors.append(
            Error(
                "MODELTRANSLATION_CUSTOM_FIELDS is not set to 'django_ckeditor_5.fields.CKEditor5Field'.",
                hint="Set MODELTRANSLATION_CUSTOM_FIELDS to 'django_ckeditor_5.fields.CKEditor5Field' in your settings file.",
                id="settings.E005",
            )
        )

    return errors + warnings
