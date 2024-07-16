import time, os, sys
import pynput

loginPasswordPath = ""
scriptPath = ""
loginPasswordLines = []
intline = 0
recordrun = True
stepend = False
steps = []
mouse = pynput.mouse.Controller()
keyboard = pynput.keyboard.Controller()

class step:
    def __init__(self, stepid:int = 0, point = (0,0), time:float = 0,
                 toClickLeft:bool = False, toClickRight:bool = False, toWrite1:bool = False, toWrite2:bool = False,
                 toCopy:bool = False, toPaste:bool = False, toF11:bool = False, toAltF4:bool = False):
        self.point = point
        self.stepid = stepid
        self.time = time
        self.toClickLeft = toClickLeft
        self.toClickRight = toClickRight
        self.toWrite1 = toWrite1
        self.toWrite2 = toWrite2
        self.toCopy = toCopy
        self.toPaste = toPaste
        self.toF11 = toF11
        self.toAltF4 = toAltF4
    
    def run(self):
        global intline
        mouse.position = (self.point[0], self.point[1])
        if (self.toClickLeft):
            mouse.click(pynput.mouse.Button.left, 2)
        if (self.toClickRight):
            mouse.click(pynput.mouse.Button.right, 2)
        if (self.toWrite1):
            keyboard.type(loginPasswordLines[intline][0])
        if (self.toWrite2):
            keyboard.type(loginPasswordLines[intline][1])
            intline += 1
        if (self.toCopy):
            keyboard.press(pynput.keyboard.Key.ctrl)
            keyboard.press('c')
            keyboard.release(pynput.keyboard.Key.ctrl)
            keyboard.release('c')
        if (self.toPaste):
            keyboard.press(pynput.keyboard.Key.ctrl)
            keyboard.press('v')
            keyboard.release(pynput.keyboard.Key.ctrl)
            keyboard.release('v')
        if (self.toF11):
            keyboard.press(pynput.keyboard.Key.f11)
            keyboard.release(pynput.keyboard.Key.f11)
        if (self.toAltF4):
            keyboard.press(pynput.keyboard.Key.alt)
            keyboard.press(pynput.keyboard.Key.f4)
            keyboard.release(pynput.keyboard.Key.alt)
            keyboard.release(pynput.keyboard.Key.f4)
        
        if (self.stepid == 0): time.sleep(1)
        else: time.sleep(self.time)

    def __str__(self) -> str:
        return f"{str(self.stepid).rjust(2, " ")}|{str(self.point[0]).rjust(5, " ")},{str(self.point[1]).rjust(5, " ")}|{str(round(self.time, 3)).rjust(5, " ")}|{'1' if self.toClickLeft else '0'},{'1' if self.toClickRight else '0'},{'1' if self.toWrite1 else '0'},{'1' if self.toWrite2 else '0'},{'1' if self.toCopy else '0'},{'1' if self.toPaste else '0'},{'1' if self.toF11 else '0'},{'1' if self.toAltF4 else '0'}"

thisstep = step()

def readLoginPasswordFile():
    global loginPasswordPath, loginPasswordLines
    with open(loginPasswordPath, 'r', encoding='utf-8') as file:
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
        if (key == pynput.keyboard.Key.esc):
            thisstep.point = mouse.position
            steps.append(thisstep)
            stepend = True
            recordrun = False
        if (key == pynput.keyboard.Key.space):
            thisstep.point = mouse.position
            steps.append(thisstep)
            stepend = True
        if (key == pynput.keyboard.KeyCode.from_char('1')):
            thisstep.toClickLeft = True
        if (key == pynput.keyboard.KeyCode.from_char('2')):
            thisstep.toClickRight = True
        if (key == pynput.keyboard.KeyCode.from_char('3')):
            thisstep.toWrite1 = True
        if (key == pynput.keyboard.KeyCode.from_char('4')): 
            thisstep.toWrite2 = True
        if (key == pynput.keyboard.KeyCode.from_char('5')):
            thisstep.toCopy = True
        if (key == pynput.keyboard.KeyCode.from_char('6')):
            thisstep.toPaste = True
        if (key == pynput.keyboard.KeyCode.from_char('7')):
            thisstep.toF11 = True
        if (key == pynput.keyboard.KeyCode.from_char('8')):
            thisstep.toAltF4 = True
        return False

    recordrun = True
    stepend = False
    stepid = 0
    time.sleep(5)
    print("[Record] start")
    while (recordrun):
        print("[Step] start")
        stepStartTime = time.time()
        thisstep = step(stepid=stepid)
        while (not stepend):
            with pynput.keyboard.Listener(on_press=on_press) as listener:
                listener.join()
        stepEndTime = time.time()
        thisstep.time = stepEndTime - stepStartTime
        print("[Step] end")
        stepid += 1
        stepend = False
    print("[Record] end")

def play():
    def on_press(key):
        if (key == pynput.keyboard.Key.esc):
            print("[Play] stop")
            os._exit(0)
    listener = pynput.keyboard.Listener(on_press=on_press)
    listener.start()
    
    print("[Play] start")
    for i in range(0, len(steps)):
        print(steps[i])
        if (i-1 > 0): steps[i].run()
        else: steps[i].run()
    print("[Play] end")

def scriptWrite():
    print("[Write] start")
    with open(scriptPath, 'w', encoding='utf-8') as file:
        for i in range(0, len(steps)):
            file.write(f"{steps[i]}\n")
    print("[Write] end")

def scriptRead():
    print("[Read] start")
    with open(scriptPath, 'r', encoding='utf-8') as file:
        line = "fill"
        while (line != ""):
            line = file.readline()
            if (line != ""):
                line = line.replace("\n", "").split('|')
                steppoint = line[1].split(",")
                stepparams = line[3].split(",")
                steps.append(step(
                    int(line[0]),
                    (int(steppoint[0]), int(steppoint[1])),
                    float(line[2]),
                    bool(int(stepparams[0])),
                    bool(int(stepparams[1])),
                    bool(int(stepparams[2])),
                    bool(int(stepparams[3])),
                    bool(int(stepparams[4])),
                    bool(int(stepparams[5])),
                    bool(int(stepparams[6])),
                    bool(int(stepparams[7]))
                ))
    print("[Read] end")

def main():
    global loginPasswordPath, scriptPath
    if (len(sys.argv) < 4):
        print(f'To run: python "{sys.argv[0]}" "pathToLoginPasswordFile" "pathToScriptFile" mode\n')
        print(f'pathToLoginPasswordFile - a path to your login:password file')
        print(f'pathToScriptFile - a path to your script file')
        print(f'mode - a mod from listed below')
        print(f'rp - record and play')
        print(f'rW - record and write')
        print(f'Rp - read and play')
        print(f'RpL - read and play with endless loop')
    else:
        loginPasswordPath = sys.argv[1].replace('"', '')
        scriptPath = sys.argv[2].replace('"', '')
        readLoginPasswordFile()
        match sys.argv[3]:
            case 'rp':
                record()
                play()
            case 'rW':
                record()
                scriptWrite()
            case 'Rp':
                scriptRead()
                play()
            case 'RpL':
                playCount = 0
                scriptRead()
                while (True):
                    play()
                    playCount += 1
                    print(f"Play count: {playCount}")

if __name__ == "__main__":
    main()