from Model.Channel import Channel


class Episode(object):
    __audioFile = ''
    __channel = None
    __title = ''

    def __init__(self, title: str, audioFile: str, channel: Channel):
        self.__title = title
        self.__audioFile = audioFile
        self.__channel = channel

    def getAudioFile(self) -> str:
        return self.__audioFile

    def getChannel(self) -> Channel:
        return self.__channel

    def getTitle(self) -> str:
        return self.__title
