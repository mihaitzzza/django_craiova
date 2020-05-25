from requests import request, HTTPError
from django.core.files.base import ContentFile
from uuid import uuid4


def profile_picture(backend, user, response, is_new, *args, **kwargs):
    if is_new:
        url = None
        params = {}

        if backend.name == 'google-oauth2':
            url = response['picture']

        if backend.name == 'facebook':
            url = 'http://graph.facebook.com/{USER_ID}/picture'.format(
                USER_ID=response['id'],
            )
            params['type'] = 'large'

        if url:
            try:
                image_response = request('GET', url, params=params)
                image_response.raise_for_status()
            except HTTPError:
                pass
            else:
                profile = user.profile
                profile.avatar.save(f'{uuid4()}.jpg', ContentFile(image_response.content))
                profile.save()
