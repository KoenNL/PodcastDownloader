import os

from requests.exceptions import MissingSchema

from Model.DownloadStatus import DownloadStatus
from Service.DowloadService import DownloadService
from Service.FeedParsingService import FeedParsingService


class DownloadController(object):

    def __init__(self):
        pass

    def askConfirmation(self) -> bool:
        answer = input('Are you sure you want to download all episodes? This might take a while: [y/n] ')

        if answer.lower() != 'y' and answer.lower() != 'n':
            print('Please respond with either "y" or "n"')
            return self.askConfirmation()
        elif answer.lower() == 'y':
            return True
        else:
            return False

    def download(self):
        print('=== Podcast Downloader version 0.1 ===')
        url = input('Podcast RSS feed URL: ')
        downloadDirectory = input('Download directory: '
                                  '[press enter for default: "' + self.getDefaultDownloadDirectory() + '"] ')

        if len(downloadDirectory) == 0:
            downloadDirectory = self.getDefaultDownloadDirectory()

        try:
            downloadService = DownloadService(FeedParsingService(), downloadDirectory)

            print('Preparing download...')

            downloadStatus = downloadService.downloadFeed(url)
            print('Found ' + str(downloadStatus.getNumberOfEpisodes()) + ' episodes to download')

            if self.askConfirmation():
                print('Starting download... (press "q" to stop)')
                print(self.formatProgress(downloadStatus), end='\r')
                for downloadStatus in downloadService.downloadEpisodes():
                    print(self.formatProgress(downloadStatus), end='\r')
            else:
                print('\nProcess stopped by user.')
        except ConnectionError as exception:
            print('ERROR: ' + str(exception))
        except MissingSchema:
            print('Could not find feed at the given URL. If you\'re having trouble finding the right URL, '
                  'try finding your podcast on https://podcastaddict.com/podcasts')
        except IOError as exception:
            print('ERROR: ' + str(exception))
            print(type(exception))

        print('\nDone!')

    def formatProgress(self, downloadStatus: DownloadStatus) -> str:
        return ' Downloading... ' + str(downloadStatus.getNumberOfDownloadedEpisodes()) + ' out of ' \
               + str(downloadStatus.getNumberOfEpisodes()) + ' episodes downloaded. ' \
               + str(downloadStatus.getPercentageDone().__round__(2)) + '% complete.'

    def getDefaultDownloadDirectory(self) -> str:
        return 'C:\\Users\\' + os.getlogin() + '\\Downloads'
