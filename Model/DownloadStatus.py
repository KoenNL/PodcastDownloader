class DownloadStatus(object):

    __numberOfEpisodes = 0
    __numberOfDownloadedEpisodes = 0
    __percentageDone = 0.0

    def __init__(self, numberOfEpisodes: int):
        self.__numberOfEpisodes = numberOfEpisodes

    def incrementDownloaded(self):
        self.__numberOfDownloadedEpisodes += 1
        self.calculatePercentageDone()

    def calculatePercentageDone(self):
        self.__percentageDone = (self.__numberOfDownloadedEpisodes / self.__numberOfEpisodes) * 100

    def getNumberOfDownloadedEpisodes(self) -> int:
        return self.__numberOfDownloadedEpisodes

    def getNumberOfEpisodes(self) -> int:
        return self.__numberOfEpisodes

    def getPercentageDone(self) -> float:
        return self.__percentageDone
