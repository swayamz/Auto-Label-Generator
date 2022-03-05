import subprocess
import pyautogui
import time
from datetime import datetime
date = datetime.now()
RITM = input("Enter RITM #: RITM00")
CU_name = input("Enter Computer User's Name: ")
CU_cruzid = input("Enter Computer User's CRUZID: ")
C_type = input("Win Or Mac? (def: Win): ")
if (C_type == ""): C_type = "Win"
if(C_type == "Win"):
    C_st = input("Enter ST: ")
    C_bind = input("Bind Local/AD/PPDO/AU (def: AD): ")
    if (C_bind == ""): C_bind = "AD"
C_backup = input("Backup needed? (Y/N): ")
C_software = input("Enter xtra Software: ")
C_dept = input("Enter User's Dept Naming Convention: ")
C_lap = input("Laptop? (Y/N def: Y): ")
if (C_lap == ""): C_lap = "Y"
C_mig = input("Migration? (Y/N def: N): ")
if (C_mig == ""): C_mig = "N"

extern_label = open("extern.txt", "w")
comp_label = open("comp.txt", "w")
users_label = open("users.txt", "w")

#External Label
extern_label.write("RITM00" + RITM + "\n")
extern_label.write("Client Name:\n" + CU_name + "\n")
extern_label.write("Intake Data: " + date.strftime("%m/%d/%Y") + "\n")
if(C_mig == "Y"):
    x = "X"
elif(C_mig == "N"):
    x = " "
extern_label.write("Migration: [" + x + "]\n")
extern_label.write("Return Location\n[   ] Depot [   ] Other:")
extern_label.close()

if(C_type == "Win"):
    comp_label.write("RITM00" + RITM + "\n")
    comp_label.write("Service Tag: " + C_st + "\n")
    if(C_lap == "Y"): x = "-lt"
    elif(C_lap == "N"): x = ""
    comp_label.write("PC: " + C_dept + "-" + CU_cruzid + x + "\n")
    comp_label.write("Full User's Name:\n" + CU_name + "\n")
    comp_label.write("Domain: " + C_bind + "[   ] BIOS[   ]\n")
    comp_label.write("Updates[   ] Users[   ] Image[ ]\n")
    comp_label.write("Drivers[   ] Encrypt[   ] DefSW[   ]\n")
    comp_label.write("SW[   ]: " + C_software + "\n")
    if(C_backup == "Y"): x = "YES[   ]"
    elif(C_backup == "N"): x = "NO"
    else: C_backup = input("Backup needed? (Y/N): ")
    comp_label.write("BACKUP? " + x + "\n")
    if(C_backup == "Y"): x = "MIGRATE[   ]"
    elif(C_backup == "N"): x = ""
    comp_label.write("SHIP[   ] " + x)
    comp_label.close()

path_to_notepad = 'C:\\Program Files (x86)\\Brother\\Ptedit52\Ptedit52.exe'
path_to_file = 'comp.txt'
P = subprocess.Popen([path_to_notepad, path_to_file])
time.sleep(5)
'''pyautogui.keyDown('ctrl')  # hold down the shift key
pyautogui.press('p')     # press the left arrow key
pyautogui.keyUp('ctrl')
pyautogui.press('enter')
time.sleep(1)
P.terminate()'''