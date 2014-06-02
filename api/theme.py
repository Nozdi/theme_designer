"""
.. module:: theme_api
    :synopsis: Theme designer API implemented using Google Cloud Endpoints.
"""

import time
import endpoints
from protorpc import (
    message_types,
    remote,
)

from api.messages import (
    InputMelody,
    EditMelody,
    DeleteMelody,
    OutputMelody,
    OutputMelodyCollection,
)
from api.gsc import (
    create_file,
    delete_file,
)
from api.models import (
    Track,
    user_key,
)
from sound import (
    get_sound_in_bytes,
    OCTAVE,
)

WEB_CLIENT_ID = '405390963802-1gkqm09rnc9fhjl6atra67gmnvo6crdi.apps.googleusercontent.com'

package = 'Theme'


@endpoints.api(name='theme', version='v1',
               allowed_client_ids=[WEB_CLIENT_ID, endpoints.API_EXPLORER_CLIENT_ID],
               scopes=[endpoints.EMAIL_SCOPE])
class ThemeDesignerApi(remote.Service):
    """Theme Designer API v1."""

    def create_wave(self, music_string, nick):
        try:
            wave = get_sound_in_bytes(music_string)
        except ValueError:
            raise endpoints.BadRequestException(
                "Use " + " ".join(OCTAVE.keys()) + " or digits"
            )
        filename = "{}/{}.wav".format(nick, str(time.time()).replace('.', '_'))
        url = create_file(filename, wave.read())
        return url

    def validate_existance(self, obj, msg):
        if not obj:
            raise endpoints.NotFoundException(msg)

    @endpoints.method(InputMelody, OutputMelody,
                      path='theme/create', http_method='POST',
                      name='createMusic')
    def create_music(self, request):
        current_user = endpoints.get_current_user()
        nick = (current_user.nickname() if current_user is not None
                else 'anonymous')

        self.validate_existance(request.name, "Insert a name")

        url = self.create_wave(request.music_string, nick)
        m_id = 0

        if current_user:
            new_track = Track(parent=user_key(current_user.nickname()))
            new_track.author = current_user
            new_track.name = request.name
            new_track.music_string = request.music_string.upper()
            new_track.music_filename = url
            key = new_track.put()
            m_id = key.id()

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

    @endpoints.method(EditMelody, OutputMelody,
                      path='theme/edit', http_method='POST',
                      name='editMusic')
    def edit_by_key(self, request):
        current_user = endpoints.get_current_user()
        nick = (current_user.nickname() if current_user is not None
                else 'anonymous')

        url = self.create_wave(request.music_string, nick)

        if current_user:
            t = Track.get_by_id(
                request.m_id,
                parent=user_key(current_user.nickname())
            )

            self.validate_existance(request.name, "Insert a name")
            self.validate_existance(t, "Not found id: {}".format(request.m_id))

            delete_file(t.music_filename)

            t.name = request.name
            t.music_string = request.music_string
            t.music_filename = url
            t.put()

        return OutputMelody(
            m_id=request.m_id,
            name=request.name,
            music_string=request.music_string,
            path=url,
        )

    @endpoints.method(DeleteMelody, message_types.VoidMessage,
                      path='theme/delete', http_method='POST',
                      name='deleteMusic')
    def remove_by_key(self, request):
        current_user = endpoints.get_current_user()
        if current_user:
            t = Track.get_by_id(
                request.m_id,
                parent=user_key(current_user.nickname())
            )

            self.validate_existance(t, "Not found id: {}".format(request.m_id))

            delete_file(t.music_filename)
            t.delete()
        return message_types.VoidMessage()


APPLICATION = endpoints.api_server([ThemeDesignerApi])
