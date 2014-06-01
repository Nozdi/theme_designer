"""
.. module:: theme_api
    :synopsis: Theme designer API implemented using Google Cloud Endpoints.
"""

import time
import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote

from api.messages import (
    InputMelody,
    OutputMelody,
    OutputMelodyCollection,
)
from api.gsc import create_file
from api.models import (
    Track,
    user_key,
)
from sound import get_sound_in_bytes

WEB_CLIENT_ID = '405390963802-1gkqm09rnc9fhjl6atra67gmnvo6crdi.apps.googleusercontent.com'

package = 'Theme'


@endpoints.api(name='theme', version='v1',
               allowed_client_ids=[WEB_CLIENT_ID, endpoints.API_EXPLORER_CLIENT_ID],
               scopes=[endpoints.EMAIL_SCOPE])
class ThemeDesignerApi(remote.Service):
    """Theme Designer API v1."""

    @endpoints.method(InputMelody, OutputMelody,
                      path='theme/create', http_method='POST',
                      name='createMusic')
    def create_music(self, request):
        current_user = endpoints.get_current_user()
        nick = (current_user.nickname() if current_user is not None
                 else 'anonymous')

        wave = get_sound_in_bytes(request.music_string)

        filename = "{}/{}.wave".format(nick, str(time.time()).replace('.', '_'))
        url = create_file(filename, wave.read())
        m_id = 0

        if current_user:
            new_track = Track(parent=user_key(current_user.nickname()))
            new_track.author = current_user
            new_track.name = request.name
            new_track.music_string = request.music_string.upper()
            new_track.music_filename = url
            new_track.put()
            m_id = new_track.key().id()

        return OutputMelody(
            m_id=m_id,
            name=request.name,
            music_string=request.music_string,
            path=url,
        )

    @endpoints.method(message_types.VoidMessage, OutputMelodyCollection,
                      path='theme/all', http_method='GET',
                      name='listMelodies')
    def get_all_music(self, request):
        current_user = endpoints.get_current_user()
        nick = (current_user.nickname() if current_user is not None
                 else 'anonymous')

        tracks = Track.all().filter("author =", current_user)

        items = []
        for t in tracks:
            items.append(OutputMelody(
                m_id=t.key().id(),
                name=t.name,
                music_string=t.music_string,
                path=t.music_filename
            ))

        return OutputMelodyCollection(items=items)

    #     return Greeting(message='hello %s' % (email,))

    # MULTIPLY_METHOD_RESOURCE = endpoints.ResourceContainer(
    #         Greeting,
    #         times=messages.IntegerField(2, variant=messages.Variant.INT32,
    #                                     required=True))

    # @endpoints.method(MULTIPLY_METHOD_RESOURCE, Greeting,
    #                   path='hellogreeting/{times}', http_method='POST',
    #                   name='greetings.multiply')
    # def greetings_multiply(self, request):
    #     return Greeting(message=request.message * request.times)

    # @endpoints.method(message_types.VoidMessage, GreetingCollection,
    #                   path='hellogreeting', http_method='GET',
    #                   name='greetings.listGreeting')
    # def greetings_list(self, unused_request):
    #     return STORED_GREETINGS


    # ID_RESOURCE = endpoints.ResourceContainer(
    #         message_types.VoidMessage,
    #         id=messages.IntegerField(1, variant=messages.Variant.INT32))
    # @endpoints.method(ID_RESOURCE, Greeting,
    #                   path='hellogreeting/{id}', http_method='GET',
    #                   name='greetings.getGreeting')
    # def greeting_get(self, request):
    #     try:
    #         return STORED_GREETINGS.items[request.id]
    #     except (IndexError, TypeError):
    #         raise endpoints.NotFoundException('Greeting %s not found.' %
    #                                           (request.id,))




APPLICATION = endpoints.api_server([ThemeDesignerApi])
