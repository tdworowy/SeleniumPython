from datetime import date

import requests
from bs4 import BeautifulSoup

from Utils.utils import log

# filePath = os.path.dirname(os.path.abspath(__file__))+'\\file.txt'
filePath = "D:\Google_drive\Songs\songsList.txt"
lastUpdated = "D:\Google_drive\Songs\LastUpdated.txt"
PAGES = 706


# PAGES = 2
# LAST_7_DAYS
# LAST_30_DAYS
# LAST_90_DAYS
# LAST_180_DAYS
# LAST_365_DAYS
# ALL

def get_file_path():
    return filePath


def get_titles(url):
    log("Get songs from %s" % url)
    response = requests.get(url).text
    soup = BeautifulSoup(response, "html.parser")
    titles = soup.find_all("a", class_="link-block-target")
    titles = str(titles)
    titles = titles.split(">")
    return clear_titles(titles)


def clear_titles(titles):
    cleanTitels = []
    for text in titles:
        try:
            # print(text)
            if "—" in text:
                i = text.index("title=\"") + 7
                temp = text[i:-1].replace("—", "-")
                cleanTitels.append(temp + "\n")

        except Exception as ex:
            log('EXEPTION in cleanTitels')
            log(ex)
            continue
    return cleanTitels


def get_songs():
    log("Generate songs list")
    log("Clear existing or create new file")
    open(filePath, 'w').close()
    for i in range(1, PAGES):
        titles = get_titles('https://www.last.fm/pl/user/TotaledThomas/library/tracks?page= %s' % str(i))
        to_file(titles)


def to_file(titels):
    with open(filePath, 'a') as f:
        for text in titels:
            try:

                f.write(text)
                f.flush()
            except Exception as ex:
                log("EXEPTION while generating songs list")
                log(str(ex))
                continue


def update_songs():
    dateToday = date.today()
    log("Update songs list")
    f1 = open(filePath)
    f2 = open(filePath, 'a')
    with (open(lastUpdated, 'r')) as f3:
        if f3.readline() == str(dateToday):
            log("List already updated")
            return 0
    log("Files opened Correctly")
    oldTitels = [line for line in f1.readlines()]
    # newTitles = clearTitels(getTitels(10,"http://www.last.fm/pl/user/TotaledThomas/library?date_preset=LAST_7_DAYS&page="))
    for i in range(1, 60):
        newTitles = get_titles(
            "https://www.last.fm/pl/user/TotaledThomas/library?date_preset=LAST_30_DAYSS&page=%s" % str(i))
        log("New titles: %s page %s" % (str(newTitles), str(i)))
        for title in newTitles:
            try:
                if title not in oldTitels:
                    f2.write(title)
                    f2.flush()
            except Exception as ex:
                log("Error while updating songs list")
                log(str(ex))
                continue
    f2.flush()
    f2.close()
    log("Song List updated correctly")
    open(lastUpdated, 'w').write(str(dateToday))


if __name__ == '__main__':
    get_songs()
