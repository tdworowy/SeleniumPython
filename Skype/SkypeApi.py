import re
import sys

from skpy import Skype

from Utils.utils import writeToFileNoDuplicates


class skypeApi:
    def __init__(self,login,passw):
        self.skype = Skype(login, passw)


    def getChats(self):
        return self.skype.chats.recent()

    def getChatIDByTopic(self,name):
        for chat in  self.skype.chats.recent().values():
            if hasattr(chat, 'topic') and chat.topic == name: return chat



    def getAllMessages(self,name):
        messages = []
        chat = self.getChatIDByTopic(name)
        self.__getAllMessages(chat,messages)
        return messages


    def __getAllMessages(self,chat,list_):
        lastLen =0
        while 1:
                list_.extend(chat.getMsgs())
                if lastLen == len(list_) : break
                else: lastLen =len(list_)




    def getLinks(self,name):
        links = []
        for msg in self.getAllMessages(name):
            match = re.search(r'href=[\'"]?([^\'" >]+)', msg.content)
            if match:
               links.append(match.group(1))
        return links


if __name__ == '__main__':
    user = sys.argv[1]
    passw = sys.argv[2]
    sa = skypeApi(user,passw)
    links = sa.getLinks("Learning is an awesome journey")
    writeToFileNoDuplicates("D:\Google_drive\links_from_skype\links.txt",links)
