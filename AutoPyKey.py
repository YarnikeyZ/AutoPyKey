import time
import sys as sus

import pyautogui
from pynput import keyboard as pkb
import keyboard as kb

loginPasswordPath = ""
scriptPath = ""
loginPasswordLines = []
intline = 0
recordrun = True
stepend = False
steps = []

class step:
    def __init__(self, stepid:int, point:pyautogui.Point = pyautogui.Point(0,0), time:float = 0,
                 toClick:bool = False, toWrite1:bool = False, toWrite2:bool = False, toCopy:bool = False, toPaste:bool = False):
        self.point = point
        self.stepid = stepid
        self.time = time
        self.toClick = toClick
        self.toWrite1 = toWrite1
        self.toWrite2 = toWrite2
        self.toCopy = toCopy
        self.toPaste = toPaste
    
    def run(self, previous):
        global intline
        if (self.toClick):
            pyautogui.click(self.point.x, self.point.y)
        if (self.toWrite1):
            kb.write(loginPasswordLines[intline][0])
        if (self.toWrite2):
            kb.write(loginPasswordLines[intline][1])
            intline += 1
        if (self.toCopy):
            with pyautogui.hold('ctrl'):
                pyautogui.press('c')
        if (self.toPaste):
            with pyautogui.hold('ctrl'):
                pyautogui.press('v')
        
        if (self.stepid == 0): time.sleep(1)
        else: time.sleep(self.time - previous.time)

    def __str__(self) -> str:
        return f"{str(self.stepid).rjust(2, " ")}|{str(self.point.x).rjust(5, " ")},{str(self.point.y).rjust(5, " ")}|{str(self.time).rjust(18, " ")}|{'1' if self.toClick else '0'},{'1' if self.toWrite1 else '0'},{'1' if self.toWrite2 else '0'},{'1' if self.toCopy else '0'},{'1' if self.toPaste else '0'}"

thisstep = step(0)

def readLoginPasswordFile():
    global loginPasswordPath, loginPasswordLines
    with open(loginPasswordPath) as file:
        line = "fill"
        while (line != ""):
            line = file.readline()
            if (line != ""):
                line = line.replace("\n", "").split(":")
                loginPasswordLines.append(line)

def record():
    global recordrun, stepend, thisstep
    def on_press(key):
        global recordrun, stepend, thisstep
        if (key == pkb.Key.esc):
            thisstep.point = pyautogui.position()
            thisstep.time = time.time()
            steps.append(thisstep)
            stepend = True
            recordrun = False
        if (key == pkb.Key.space):
            thisstep.point = pyautogui.position()
            thisstep.time = time.time()
            steps.append(thisstep)
            stepend = True
        if (key == pkb.KeyCode.from_char('1')):
            thisstep.toClick = True
        if (key == pkb.KeyCode.from_char('2')):
            thisstep.toWrite1 = True
        if (key == pkb.KeyCode.from_char('3')): 
            thisstep.toWrite2 = True
        if (key == pkb.KeyCode.from_char('4')):
            thisstep.toCopy = True
        if (key == pkb.KeyCode.from_char('5')):
            thisstep.toPaste = True
        return False

    recordrun = True
    stepend = False
    stepid = 0
    print("[Record] start1 ")
    while (recordrun):
        print("[Step] start")
        thisstep = step(stepid=stepid)
        while (not stepend):
            with pkb.Listener(on_press=on_press) as listener:
                listener.join()
        print("[Step] end")
        stepid += 1
        stepend = False
    print("[Record] end")

def play():
    print("[Play] start")
    for i in range(0, len(steps)):
        print(steps[i])
        if (i-1 > 0): steps[i].run(steps[i-1])
        else: steps[i].run(steps[i])
    print("[Play] end")

def scriptWrite():
    print("[Write] start")
    with open(scriptPath, 'w') as file:
        for i in range(0, len(steps)):
            file.write(f"{steps[i]}\n")
    print("[Write] end")

def scriptRead():
    print("[Read] start")
    with open(scriptPath, 'r') as file:
        line = "fill"
        while (line != ""):
            line = file.readline()
            if (line != ""):
                line = line.replace("\n", "").split('|')
                steppoint = line[1].split(",")
                stepparams = line[3].split(",")
                steps.append(step(
                    int(line[0]),
                    pyautogui.Point(int(steppoint[0]), int(steppoint[1])),
                    float(line[2]),
                    bool(int(stepparams[0])),
                    bool(int(stepparams[1])),
                    bool(int(stepparams[2])),
                    bool(int(stepparams[3])),
                    bool(int(stepparams[4]))
                ))
    print("[Read] end")

def main():
    global loginPasswordPath, scriptPath
    if (len(sus.argv) < 2):
        print(f'To run: python "{sus.argv[0]}" "pathToLoginPasswordFile" "pathToScriptFile" mode\n')
        print(f'pathToLoginPasswordFile - a path to your login:password file')
        print(f'pathToScriptFile - a path to your script file')
        print(f'mode - a mod from listed below')
        print(f'rp - record and play')
        print(f'rW - record and write')
        print(f'Rp - read and play')
    else:
        loginPasswordPath = sus.argv[1].replace('"', '')
        scriptPath = sus.argv[2].replace('"', '')
        readLoginPasswordFile()
        match sus.argv[3]:
            case 'rp':
                record()
                play()
            case 'rW':
                record()
                scriptWrite()
            case 'Rp':
                scriptRead()
                play()

if __name__ == "__main__":
    main()