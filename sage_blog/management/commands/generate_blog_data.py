import logging
import timeit
from typing import TextIO

from colorama import init
from django.core.management.base import BaseCommand

from sage_blog.repository.generator import DataGeneratorLayer

logger = logging.getLogger(__name__)

init(autoreset=True)


class Command(BaseCommand):
    help = "Load a list of example data into the database"

    def handle(self, *args, **kwargs):
        logger.info("Generate Data for Blog")
        DGL = DataGeneratorLayer()

        self.show_warning_msg("create categories")
        start = timeit.default_timer()
        DGL.create_post_categories(11)
        stop = timeit.default_timer()
        self.show_success_msg("create categories finished in: " + str(stop - start))

        self.show_warning_msg("create tags")
        start = timeit.default_timer()
        DGL.create_tags(
            total=25,
        )
        stop = timeit.default_timer()
        self.show_success_msg("create tags finished in: " + str(stop - start))

        self.show_warning_msg("create posts")
        start = timeit.default_timer()
        DGL.create_posts(
            total=50,
        )
        stop = timeit.default_timer()
        self.show_success_msg("create posts finished in: " + str(stop - start))

        self.show_warning_msg("create FAQ")
        start = timeit.default_timer()
        DGL.create_faqs(
            total=50,
        )
        stop = timeit.default_timer()
        self.show_success_msg("create FAQ finished in: " + str(stop - start))

        logger.info("Data Generation Finished")

    def show_success_msg(self, msg: str) -> TextIO:
        """
        Display a success message on the console.

        Args:
        - msg (str): The success message.

        Returns:
        TextIO: The output stream.
        """
        self.stdout.write(self.style.SUCCESS(msg))

    def show_warning_msg(self, msg: str) -> TextIO:
        """
        Display a warning message on the console.

        Args:
        - msg (str): The warning message.

        Returns:
        TextIO: The output stream.
        """
        self.stdout.write(self.style.WARNING(msg))

    def show_error_msg(self, msg: str) -> TextIO:
        """
        Display an error message on the console.

        Args:
        - msg (str): The error message.

        Returns:
        TextIO: The output stream.
        """
        self.stdout.write(self.style.ERROR(msg))
