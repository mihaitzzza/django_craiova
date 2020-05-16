import os
from django.conf import settings
from uuid import uuid4


def handle_upload_file(file):
    random_filename = uuid4()
    _, os_file_extension = os.path.splitext(file.name)

    path = '{BASE_DIR}/{MEDIA_ROOT}/uploads/{FILENAME}'.format(
        BASE_DIR=settings.BASE_DIR,
        MEDIA_ROOT=settings.MEDIA_ROOT,
        FILENAME='{}{}'.format(random_filename, os_file_extension),
    )

    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
