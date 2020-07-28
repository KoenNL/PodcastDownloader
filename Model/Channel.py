class Channel(object):

    __title = ''
    __url = ''

    def __init__(self, title: str, url: str):
        self.__title = title
        self.__url = url

    def getTitle(self) -> str:
        return self.__title

    def getUrl(self) -> str:
        return self.__url
