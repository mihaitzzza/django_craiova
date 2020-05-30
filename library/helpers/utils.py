from random import choice
from django.conf import settings
from django.db.models import Max
from library.models.category import Category, Subcategory
from library.models.book import Book


def get_mocked_nicknames():
    with open(f'{settings.BASE_DIR}/library/helpers/mocks/nicknames.txt') as mock_file:
        nicknames = mock_file.read().splitlines()

    return nicknames


def get_max_ids():
    all_categories = Category.objects.all()
    category_max_id = all_categories.aggregate(Max('id'))['id__max']
    category_max_id = 0

    all_subcategories = Subcategory.objects.all()
    subcategory_max_id = all_subcategories.aggregate(Max('id'))['id__max']
    subcategory_max_id = 0

    all_books = Book.objects.all()
    book_max_id = all_books.aggregate(Max('id'))['id__max']
    book_max_id = 0

    return category_max_id, subcategory_max_id, book_max_id


def create_category(category_max_id, index, mocked_name):
    category = Category(name=f'{mocked_name} {category_max_id + 1 + index}')
    category.save()

    return category


def create_subcategories(categories, subcategory_max_id, subcategories_count, available_mocked_names):
    subcategories = []
    subcategory_index = 0
    category_index = 0
    categories_count = len(categories)

    while subcategory_index < subcategories_count:
        mocked_name = choice(available_mocked_names)

        if category_index >= categories_count:
            category_index = 0

        current_category = categories[category_index]

        subcategory = Subcategory(
            name=f'{mocked_name} {subcategory_max_id + 1 + subcategory_index}',
            category=current_category
        )
        subcategory.save()
        subcategories.append(subcategory)

        subcategory_index += 1
        category_index += 1

    return subcategories


def create_books(subcategories, book_max_id, books_count, available_mocked_names):
    books = []
    book_index = 0
    subcategory_index = 0
    subcategories_count = len(subcategories)

    while book_index < books_count:
        mocked_name = choice(available_mocked_names)

        if subcategory_index >= subcategories_count:
            subcategory_index = 0

        current_subcategory = subcategories[subcategory_index]

        book = Book(
            title=f'{mocked_name} {book_max_id + 1 + book_index}',
            author=f'{choice(available_mocked_names)}',
            year=choice(range(1950, 2020)),
            subcategory=current_subcategory
        )
        book.save()
        books.append(book)

        book_index += 1
        subcategory_index += 1

    return books


# create_foreign_key_objects
def create_foreign_key_objects(model, foreign_objects, max_id, count, available_mocked_names):
    objects = []
    object_index = 0
    foreign_object_index = 0
    foreign_objects_count = len(foreign_objects)

    while object_index < count:
        mocked_name = choice(available_mocked_names)

        if foreign_object_index >= foreign_objects_count:
            foreign_object_index = 0

        current_category = foreign_objects[foreign_object_index]

        subcategory = model(
            name=f'{mocked_name} {max_id + 1 + object_index}',
            category=current_category
        )
        subcategory.save()
        objects.append(subcategory)

        object_index += 1
        foreign_object_index += 1

    return objects
