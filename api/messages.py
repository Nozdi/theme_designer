"""
.. module:: messages
    :synopsis: ProtoRPC messages
"""

from protorpc import messages


class InputMelody(messages.Message):
    """Input melody input"""
    name = messages.StringField(1, required=True)
    music_string = messages.StringField(2, required=True)


class EditMelody(messages.Message):
    """Edit melody input"""
    m_id = messages.IntegerField(1, variant=messages.Variant.INT32, required=True)
    name = messages.StringField(2, required=True)
    music_string = messages.StringField(3, required=True)


class DeleteMelody(messages.Message):
    """Delete melody input"""
    m_id = messages.IntegerField(1, variant=messages.Variant.INT32, required=True)


class OutputMelody(messages.Message):
    """Output melody output"""
    m_id = messages.IntegerField(1, variant=messages.Variant.INT32)
    name = messages.StringField(2)
    music_string = messages.StringField(3)
    path = messages.StringField(4)


class OutputMelodyCollection(messages.Message):
    """Collection of OutpurMelodies."""
    items = messages.MessageField(OutputMelody, 1, repeated=True)
