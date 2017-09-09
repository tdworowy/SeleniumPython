import re

from skpy import Skype


class SkypeApi:
    def __init__(self,login,passw):
        self.skype = Skype(login, passw)
        self.chats = None


    def getContactID(self,first,last):
        for contact in self.skype.contacts.search(first + ' '+last):
            if contact.name.first == first and contact.name.last == last:
                 print("Name: %s ID: %s" %(contact.name,contact.id))
                 return contact.id


    def getChats(self):
        return self.skype.chats.recent()

    def getChatByTopic(self, names):
        self.chats = set()
        for chat in  self.skype.chats.recent().values():
            print(chat)
            if hasattr(chat, 'topic') and chat.topic in names:
                print("Found: %s" % chat)
                self.chats.add(chat)




    def snedMessage(self,chatsNames,message):
        if self.chats == None:
            self.getChatByTopic(chatsNames)
        else:
            for chat in self.chats:
                chat.sendMsg(message)


    # def getAllMessages(self,name):
    #     messages = []
    #     chat = self.getChatByTopic(name)
    #     self.__getAllMessages(chat,messages)
    #     return messages


    def __getAllMessages(self,chat,list_):
        lastLen =0
        while 1:
                list_.extend(chat.getMsgs())
                if lastLen == len(list_) : break
                else: lastLen =len(list_)


    def addPerson(self,chatName,SkypeID):
        chat = self.getChatByTopic(chatName)
        chat.addMember(SkypeID)



    def getLinks(self,name):
        links = []
        for msg in self.getAllMessages(name):
            match = re.search(r'href=[\'"]?([^\'" >]+)', msg.content)
            if match:
               links.append(match.group(1))
        return links


if __name__ == '__main__':
    pass
    # user = sys.argv[1]
    # passw = sys.argv[2]
    # sa = skypeApi(user,passw)
    # links = sa.getLinks("Learning is an awesome journey")
    # writeToFileNoDuplicates("D:\Google_drive\links_from_skype\links.txt",links)

