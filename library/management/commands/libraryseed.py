from random import choice
from django.core.management.base import BaseCommand
from library.helpers.utils import get_max_ids, create_category, create_subcategories, get_mocked_nicknames, create_books
from library.models.category import Category
from library.models.book import Book


class Command(BaseCommand):
    help = 'Seed DB for library application.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--categories', '-cc',
            type=int,
            help='Number of categories to seed.',
            default=5
        )

        parser.add_argument(
            '--subcategories', '-sc',
            type=int,
            help='Number of subcategories to seed.',
            default=20
        )

        parser.add_argument(
            '--books', '-bk',
            type=int,
            help='Number of books to seed.',
            default=100
        )

    def handle(self, *args, **options):
        mocked_nicknames = get_mocked_nicknames()
        print('mocked_nicknames', mocked_nicknames)

        categories_count = options.get('categories')
        subcategories_count = options.get('subcategories')
        books_count = options.get('books')
        category_max_id, subcategory_max_id, book_max_id = get_max_ids()

        # categories = []
        # for index in range(categories_count):
        #     category = create_category(category_max_id, index)
        #     categories.append(category)
        # --- OR: list comprehension (see below)
        categories = [
            create_category(category_max_id, index, choice(mocked_nicknames))
            for index in range(categories_count)
        ]

        subcategories = create_subcategories(categories, subcategory_max_id, subcategories_count, mocked_nicknames)
        books = create_books(subcategories, book_max_id, books_count, mocked_nicknames)
        # subcategories = create_foreign_key_objects(Subcategory, categories, subcategory_max_id, subcategories_count, mocked_nicknames)
        # books = create_foreign_key_objects(Book, subcategories, book_max_id, books_count, mocked_nicknames)
