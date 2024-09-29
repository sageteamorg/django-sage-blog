from import_export import widgets


class ForeignKeyNullableWidget(widgets.ForeignKeyWidget):
    """pass"""

    # pylint: disable=W1113
    def clean(self, value, row=None, *args, **kwargs):
        if value:
            return super().clean(value)
        return None
