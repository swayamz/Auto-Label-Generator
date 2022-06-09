class Label():
    def __init__(self, RITM):
        self.RITM = RITM
        self.software = ""
        self.backup = False
        self.type = None
        self.client_cruzid = None
        self.client_name = None
        self.requestor_name = None
        self.localA = None
        self.domain = None
        self.serial = ""
        self.returnLoc = None
        self.pcname = None

    def __str__(self):
        strs =  "RITM[" + str(self.RITM) + ']\n'
        strs += "software[" + str(self.software) + ']\n'
        strs += "backup[" + str(self.backup) + ']\n'
        strs += "type[" + str(self.type) + ']\n'
        strs += "client_cruzid[" + str(self.client_cruzid) + ']\n'
        strs += "client_name[" + str(self.client_name) + ']\n'
        strs += "requestor_name[" + str(self.requestor_name) + ']\n'
        strs += "localA[" + str(self.localA) + ']\n'
        strs += "domain[" + str(self.domain) + ']\n'
        strs += "serial[" + str(self.serial) + ']\n'
        strs += "returnLoc[" + str(self.returnLoc) + ']\n'
        return strs

    def setSoftware(self, soft):
        self.software = self.software + " " + soft.replace(',', ' ')
    
    def setClient(self, user):
        self.client_cruzid = user[user.find('(')+1:user.find(')')]
        self.client_name = user[:user.find('(')-1]
        if(self.client_cruzid != ""):
            self.pcname = "___-%s-___" % self.client_cruzid
        else:
            self.pcname = ""

    def setRequestor(self, user):
        self.requestor_name = user[:user.find('(')-1]

    def setType(self, type):
        self.type = type
    
    def getType(self):
        if "Mac" in self.type:
            return "Mac"
        elif "PC\Windows" in self.type:
            return "Windows"
        else:
            return None

    def setLocal(self):
        self.localA = ""
        if self.domain is not None and self.domain != "Unknown": self.localA += '.\\'
        self.localA += "admin.%s" % self.client_cruzid

    def getUsername(self):
        username = ""
        if self.domain is not None: username += '.\\'
        username += "admin.%s" % self.client_cruzid
        return username

