import logging

from import_export import results


logger = logging.getLogger(__name__)


class DataProcessingError(results.Error):
    """
    A custom error class that extends the 'results.Error' class.

    This class provides a simplified error representation with redacted traceback
    information.

    Args:
        error (str): The error message.
        traceback (str, optional): The traceback information (default is None).
        row (int, optional): The row number where the error occurred (default is None).
    """

    def __init__(self, error=None, traceback=None, row=None, number=None):
        super().__init__(error, traceback, row)
        custom_traceback = traceback.rpartition("DETAIL:")[2] if traceback else "No traceback available"
        logger.error(
            "Error occurred at row %s: %s\nTraceback: %s", row, error, custom_traceback
        )
        self.error = (
            "An error occurred while processing the data. Please check your input."
        )
        self.traceback = custom_traceback
        self.row = []
        self.number = number
