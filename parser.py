from bs4 import BeautifulSoup
import os
import subprocess
import pyautogui
import time
from datetime import datetime
import shutil
path_to_notepad = 'C:\\Program Files (x86)\\Brother\\Ptedit52\Ptedit52.exe'

while True:
    while not os.path.exists("a_files/$pa_dashboard.html"):
        time.sleep(10)
    f = open("a_files/$pa_dashboard.html", "r")
    soup = BeautifulSoup(f, 'html.parser')
    a = soup.find_all(id=lambda x: x and x.startswith('sys_display.ni.VE'))
    #for i in range(len(a)):
        #print(i, a[i].get("value"))

    b = soup.find_all(id=lambda x: x and x.startswith('sys_original.ni.VE'))
    for i in range(len(b)):
        print(i, b[i].get("value"))

    def printlb(allsheets = True):
        pyautogui.keyDown('ctrl')
        pyautogui.press('p')
        pyautogui.keyUp('ctrl')
        if allsheets: 
            pyautogui.press('Tab', 7) 
            pyautogui.press('down')
        #pyautogui.press('enter')

    date = datetime.now()
    ritm = soup.find(id="sys_readonly.sc_req_item.number").get("value")
    requestor = a[0].get("value")
    requestor_dept = a[1].get("value")
    user = a[2].get("value")
    user_dept = a[3].get("value")
    requestor_phone = b[3].get("value")
    backup = b[25].get("value")
    group_login = b[9].get("value").lstrip(" ")
    group = b[10].get("value").lstrip(" ")
        
    # software
    soft_additional = b[16].get("value")
    soft_cc = b[18].get("value")
    soft_fmp19 = b[19].get("value")
    soft_fmp194 = b[20].get("value")
    soft_ff = b[21].get("value")
    soft_mproj = b[22].get("value")
    soft_mvis = b[23].get("value")
    soft_printer = b[30].get("value")
    soft_custom = b[24].get("value")
    #comp
    comp_type = b[14].get("value")
    comp_local = b[32].get("value")
    comp_domain = b[33].get("value")
    comp_st = b[58].get("value")
    cruzid = user[user.find('(')+1:user.find(')')]
    user = user[:user.find('(')-1]
    requestor = requestor[:requestor.find('(')-1]

    if group is not "":
        cruzid = group_login
        user = group_login
    if " " in comp_st or "(" in comp_st or ")" in comp_st or "," in comp_st: comp_st = ""
    pcname = "___-%s-___" % cruzid

    software = soft_custom + " "
    if "false" not in soft_cc: software += "CC "
    if "false" not in soft_fmp19: software += "FMP19 "
    if "false" not in soft_fmp194: software += "FMP19.4 "
    if "false" not in soft_ff: software += "FF "
    if "false" not in soft_mproj: software += "Project "
    if "false" not in soft_mvis: software += "Visio "

    print(ritm)
    print("Requestor: ", requestor)
    print("Requestor Department: ",requestor_dept)
    print("User: ", user)
    print("User Department: ", user_dept)
    print("Requestor Phone: ", requestor_phone)
    print("Backup? ", backup)
    print("Addtl Soft? ", soft_additional)
    print("soft_cc: ", soft_cc)
    print("soft_fmp19: ",soft_fmp19)
    print("soft_fmp194: ",soft_fmp194)
    print("soft_ff:", soft_ff)
    print("soft_mproj: ",soft_mproj)
    print("soft_mvis: ",soft_mvis)
    print("soft_printer: ",soft_printer)
    print(comp_type)
    print("Local Admin: ", comp_local)
    print("Domain: ",comp_domain)
    print("ST: ", comp_st)

    if comp_type == "windows":
        if "Don't Know" in comp_domain: comp_domain = "_____"
        winritm = open("out.txt", "w")
        winritm.write("RITM, ST, PCNAME, FULLUSERNAME, DOMAIN, SW, REQUESTORNAME, BACKUP\n")
        winritm.write("%s, %s, %s, %s, %s, %s, %s, %s\n" % (ritm.lstrip("RITM00"), comp_st, pcname, user, comp_domain.upper(), software, requestor, backup.upper()))
        winritm.close()
        P = subprocess.Popen([path_to_notepad, 'winritm.lbx'])
        time.sleep(5)
        printlb()
        time.sleep(1)
        P.terminate()
        if "No" not in comp_local and "Don't Know" not in comp_domain:
            user = open("out_username.txt", "w")
            user.write("USERNAME\n")
            username = ""
            if "None" not in comp_domain: username += '.\\'
            username += "admin.%s" % cruzid
            user.write(username)
            user.close()
            P = subprocess.Popen([path_to_notepad, 'username.lbx'])
            time.sleep(5)
            printlb(False)
            time.sleep(2)
            P.terminate()
            if "None" in comp_domain:
                user = open("out_username.txt", "w")
                user.write("USERNAME\n")
                username = "%s" % cruzid
                user.write(username)
                user.close()
                P = subprocess.Popen([path_to_notepad, 'username.lbx'])
                time.sleep(5)
                printlb(False)
                time.sleep(2)
                P.terminate()

    elif comp_type == "mac":
        macritm = open("out_mac.txt", "w")
        macritm.write("RITM, PCNAME, FULLUSERNAME, SW, REQUESTORNAME, BACKUP\n")
        macritm.write("%s, %s, %s, %s, %s, %s\n" % (ritm.lstrip("RITM00"), pcname, user, software, requestor, backup.upper()))
        macritm.close()
        P = subprocess.Popen([path_to_notepad, 'macritm.lbx'])
        time.sleep(5)
        printlb()
        time.sleep(2)
        P.terminate()

    f.close()
    shutil.rmtree("a_files", ignore_errors=True)
    os.remove("a.html")