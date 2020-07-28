from typing import Iterator
from xml.etree import cElementTree
from xml.etree.ElementTree import Element

from Model.Channel import Channel
from Model.Episode import Episode


class FeedParsingService(object):

    def __init__(self):
        pass

    def parse(self, url: str, feedContent: str) -> Iterator[Episode]:
        tree = cElementTree.fromstring(feedContent)

        channel = Channel(self.getChannelTitle(tree), url)

        for episode in tree.iter('item'):
            yield self.parseEpisode(episode, channel)

    def getChannelTitle(self, xmlTree: Element) -> str:
        return xmlTree.find('channel').find('title').text

    def parseEpisode(self, xmlTree: Element, channel: Channel) -> Episode:
        title = xmlTree.find('title').text
        audioFile = xmlTree.find('enclosure').attrib.get('url')
        return Episode(title, audioFile, channel)
