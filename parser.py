import imaplib
import email
from queue import Empty
from label import Label
import os
import subprocess
import pyautogui
import time
import re
path_to_notepad = 'C:\\Program Files (x86)\\Brother\\Ptedit52\Ptedit52.exe'
pyautogui.FAILSAFE = False

def printlb(allsheets = True):
    pyautogui.keyDown('ctrl')
    pyautogui.press('p')
    pyautogui.keyUp('ctrl')
    if allsheets: 
        pyautogui.press('Tab', 7) 
        pyautogui.press('down')
    pyautogui.press('enter')

def labelExecute(label):
    if label.getType() == "Windows":
        if label.domain is None: dom = "Local"
        elif "Unknown" in label.domain: dom = "_____"
        else: dom = label.domain
        winritm = open("out.txt", "w")
        winritm.write("RITM, ST, PCNAME, FULLUSERNAME, DOMAIN, SW, REQUESTORNAME, BACKUP, RETURNLOC\n")
        winritm.write("%s, %s, %s, %s, %s, %s, %s, %s, %s\n" % (str(label.RITM), str(label.serial), str(label.pcname), str(label.client_name), dom.upper(), str(label.software), str(label.requestor_name), str(label.backup), str(label.returnLoc)))
        winritm.close()
        P = subprocess.Popen([path_to_notepad, 'winritm.lbx'])
        time.sleep(10)
        printlb()
        time.sleep(1)
        P.terminate()
        if label.localA is not None:
            user = open("out_username.txt", "w")
            user.write("USERNAME\n")
            user.write(label.getUsername())
            user.close()
            P = subprocess.Popen([path_to_notepad, 'username.lbx'])
            time.sleep(5)
            printlb(False)
            time.sleep(2)
            P.terminate()

    elif label.getType() == "Mac":
        macritm = open("out_mac.txt", "w")
        macritm.write("RITM, PCNAME, FULLUSERNAME, SW, REQUESTORNAME, BACKUP\n")
        macritm.write("%s, %s, %s, %s, %s, %s, %s\n" % (label.RITM, label.pcname, label.client_name, label.software, label.requestor_name, label.backup, label.returnLoc))
        macritm.close()
        P = subprocess.Popen([path_to_notepad, 'macritm.lbx'])
        time.sleep(10)
        printlb()
        time.sleep(2)
        P.terminate()

username =
app_password= 

gmail_host= 'imap.gmail.com'
mail = imaplib.IMAP4_SSL(gmail_host)
mail.login(username, app_password)

while True:
    mail.select("Labels", False)
    _, selected_mails = mail.search(None, '(TO "depot+labels@ucsc.edu")', '(UNSEEN)')
    print("Total Labels:" , len(selected_mails[0].split()))
    print("==========================================\n")
    pyautogui.press('F15')

    labels = []
    for num in selected_mails[0].split():
        _, data = mail.fetch(num , '(RFC822)')
        _, bytes_data = data[0]
        mail.store(num,'+FLAGS','\Seen')

        email_message = email.message_from_bytes(bytes_data)    
        for part in email_message.walk():
            if part.get_content_type()=="text/plain" or part.get_content_type()=="text/html":
                message = part.get_payload(decode=True)
                labels.append(message.decode())
                break


    for label in labels:
        #fields = label.split('<br>')
        fields = re.split('<p>|<br>', label)
        fields[-1] = fields[-1].strip("</p></body></html>\r\n")
        fields[0] = (fields[0].lstrip("<html><head></head><body><h3 id=\"main\">RITM00")).strip("&nbsp;</h3>\r\n")
        print(fields)
        #fields.remove('')
        label = Label(fields[0])
        SVC = False

        for field in fields:
            if "Client" in field:
                label.setClient(field.lstrip("Client: "))
            elif "Requestor" in field:
                label.setRequestor(field.lstrip("Requestor: "))
            elif "ComputerType" in field:
                label.setType(field.lstrip("ComputerType: "))
            elif "Scotts Valley: true" in field:
                SVC = True
                break
            elif "Back up" in field:
                if "Yes" in field:
                    label.backup = "Yes"
                elif "No" in field:
                    label.backup = "No"
            elif "Adobe" in field:
                if "true" in field:
                    label.setSoftware("CC") 
            elif "FileMaker 19" in field:
                if "true" in field:
                    label.setSoftware("FM19") 
            elif "FileMaker 19.4" in field:
                if "true" in field:
                    label.setSoftware("FM194") 
            elif "Firefox" in field:
                if "true" in field:
                    label.setSoftware("FF") 
            elif "Project" in field:
                if "true" in field:
                    label.setSoftware("Proj") 
            elif "Visio" in field:
                if "true" in field:
                    label.setSoftware("Vis") 
            elif "Additional Software" in field:
                label.setSoftware(field.lstrip("Additional Software: ")) 
            elif "Local Admin" in field:
                if "Yes" in field:
                    label.setLocal()
            elif "Domain" in field:
                if "know" in field:
                    label.domain = "Unknown"
                elif "None" in field:
                    label.domain = None
                else:
                    label.domain = field.lstrip("Domain: ")
            elif "Serial Number" in field:
                label.serial = field.lstrip("Serial Number or Service Tag: ")
                if label.serial == "":
                    label.serial = ""
            elif "Return" in field:
                label.returnLoc = field.lstrip("Return: ")
                if label.returnLoc == "":
                    label.returnLoc = None

        if SVC:
            continue
        print(label)
        labelExecute(label)
        print("==========================================\n")
        time.sleep(2)
    time.sleep(10)