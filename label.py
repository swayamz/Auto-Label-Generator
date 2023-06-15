import json
import difflib
import csv
import re

departments = {}
with open('departments.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        departments[row['d']] =  row['a']

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
        self.group = False
        self.printer = "NO"
        self.printer_notes = ""
        self.printer_ip = ""
        self.notes = ""

    def __str__(self):
        strs =  "RITM[" + str(self.RITM) + ']\n'
        strs += "pcname[" + str(self.pcname) + ']\n'
        strs += "software[" + str(self.software) + ']\n'
        strs += "backup[" + str(self.backup) + ']\n'
        strs += "type[" + str(self.type) + ']\n'
        strs += "client_cruzid[" + str(self.client_cruzid) + ']\n'
        strs += "client_name[" + str(self.client_name) + ']\n'
        strs += "requestor_name[" + str(self.requestor_name) + ']\n'
        strs += "localA[" + str(self.localA) + ']\n'
        strs += "domain[" + str(self.domain) + ']\n'
        strs += "serial[" + str(', '.join(self.serial)) + ']\n'
        strs += "printer[" + str(self.printer) + ']\n'
        strs += "printer_notes[" + str(self.printer_notes) + ']\n'
        strs += "printer_ip[" + str(self.printer_ip) + ']\n'
        strs += "notes[" + str(self.notes) + ']\n'
        return strs

    def setSoftware(self, soft):
        self.software = self.software + " " + soft.replace(',', ' ')

    def setClient(self, user):
        self.client_cruzid = user[user.find('(')+1:user.find(')')]
        self.client_name = user[:user.find('(')-1]
        if(self.client_cruzid != ""):
            self.pcname = "-%s-___" % self.client_cruzid
        else:
            self.pcname = ""
    
    def setGroupLogin(self, group):
        self.group = True
        self.client_name = group.replace(',', ' ')
    
    def setGroupName(self, group):
        self.client_cruzid = group.replace(" ", "")
        self.client_name = group
        if(self.client_name is not None):
            self.pcname = self.pcname + "-%s-___" % self.client_cruzid
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
        if self.group is False: self.localA += "admin.%s" % self.client_cruzid
        else: self.localA += "admin.%s" % self.client_name

    def getUsername(self):
        username = ""
        if self.domain is not None: username += '.\\'
        if self.group is False: username += "admin.%s" % self.client_cruzid
        else: username += "admin.%s" % self.client_name
        return username

    def setDepartment(self, dept):
        match = difflib.get_close_matches(dept, departments.keys(), 1, 0.7)
        if match != []:
            if self.pcname is not None:
                self.pcname = departments[match[0]] + self.pcname
            else:
                self.pcname = departments[match[0]]
        else:
            if self.pcname is not None:
                self.pcname = "___" + self.pcname
            else:
                self.pcname = "___"
        
    def setPrinter(self, notes):
        self.printer_notes = notes.replace(',', ';').split(' ')
        for i in self.printer_notes:
            validip = re.match(r"(.).*\1.*\1", i)
            if validip:
                self.printer_ip = self.printer_ip + " " + i
                self.printer_notes.remove(i)
        self.printer_notes = ' '.join([str(elem) for elem in self.printer_notes])
        print(self.printer_ip)
        if self.printer_ip != "":
            self.printer = "DRIVERS & ADD"
        else:
            self.printer = "DRIVERS"

    def setNotes(self, notes):
        self.notes = notes.replace(',', ';')
        self.notes = self.notes.replace('&nbsp;', ' ')
