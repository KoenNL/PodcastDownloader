from pathlib import Path
from typing import Iterator

import requests

from Model.Channel import Channel
from Model.DownloadStatus import DownloadStatus
from Model.Episode import Episode
from Service.FeedParsingService import FeedParsingService


class DownloadService(object):
    __downloadDirectory = ''
    __downloadStatus = None
    __episodes = []
    __feedParsingService = None

    def __init__(self, feedParsingService: FeedParsingService, downloadDirectory: str):
        self.__downloadDirectory = Path(downloadDirectory)

        if not self.__downloadDirectory.exists():
            raise IOError('The given download directory "' + str(self.__downloadDirectory) + '" does not exist.')

        self.__feedParsingService = feedParsingService

    def createDownloadDirectory(self, channel: Channel) -> Path:
        channelDirectory = Path(self.__downloadDirectory / channel.getTitle())
        if channelDirectory.exists():
            raise IOError('Channel "' + channel.getTitle() + '" already has a directory. '
                                                             'Move or remove directory and try again.')

        channelDirectory.mkdir()
        return channelDirectory

    def downloadFeed(self, url: str) -> DownloadStatus:
        response = self.doRequest(url)
        for episode in self.__feedParsingService.parse(url, response.text):
            self.__episodes.append(episode)

        self.__downloadStatus = DownloadStatus(len(self.__episodes))

        return self.__downloadStatus

    def downloadEpisodes(self) -> Iterator[DownloadStatus]:
        channelDirectory = None
        for episode in self.__episodes:
            if channelDirectory is None:
                channelDirectory = self.createDownloadDirectory(episode.getChannel())

            self.downloadToFile(channelDirectory, episode)
            self.__downloadStatus.incrementDownloaded()
            yield self.__downloadStatus

    def downloadToFile(self, channelDirectory: Path, episode: Episode):
        filePath = Path(channelDirectory / episode.getTitle().replace(':', ' -')).with_suffix('.mp3')
        if filePath.exists():
            raise IOError('Episode "' + episode.getTitle() + '" already exists. It might be a duplicate in the feed.')

        filePath.touch()
        filePath.write_bytes(self.doRequest(episode.getAudioFile()).content)

    def doRequest(self, url: str) -> requests.Response:
        response = requests.get(url)

        if response.status_code != 200:
            raise ConnectionError('Got an unexpected response from the given URL. '
                                  'Check if the URL is correct and try again.')

        return response
