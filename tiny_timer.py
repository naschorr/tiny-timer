from time import time, sleep
from win32gui import FlashWindow, GetForegroundWindow, MessageBeep
from Tkinter import *


class App:
    def __init__(self, master):
        # Frames
        self.masterFrame = Frame(master)
        self.masterFrame.pack()

        self.topFrame = Frame(self.masterFrame)
        self.topFrame.grid(row=0)

        # StringVars
        self.svHour = StringVar()
        self.svHour.set("H")

        self.svMin = StringVar()
        self.svMin.set("M")

        self.svSec = StringVar()
        self.svSec.set("S")

        self.svStartBtn = StringVar()
        self.svStartBtn.set("Start")

        # Entry Boxes
        self.ebHour = Entry(self.topFrame, width=5, justify=CENTER, textvariable=self.svHour)
        self.ebHour.grid(row=0, column=0)

        self.ebMin = Entry(self.topFrame, width=5, justify=CENTER, textvariable=self.svMin)
        self.ebMin.grid(row=0, column=1)

        self.ebSec = Entry(self.topFrame, width=5, justify=CENTER, textvariable=self.svSec)
        self.ebSec.grid(row=0, column=2)

        # Buttons
        self.btnWait = Button(self.topFrame, textvariable=self.svStartBtn, command=self.handle_timer)
        self.btnWait.grid(row=0, column=3)

        # Phases
        self.iBtnPhase = 0

        self.iStart = 0
        self.iEnd = 0
        self.iCurr = 0

        self.iAlarmCtr = 0

        self.iHWND = self.masterFrame.winfo_id()

    def check_ebox_validity(self, sIn, sDefault):
        if(sIn == sDefault or sIn.isspace() or sIn == ""):
            return 0
        elif(sIn.isdigit()):
            return int(sIn)

    def get_ebox_values(self):
        sHour = self.check_ebox_validity(self.ebHour.get(), "H")
        sMin = self.check_ebox_validity(self.ebMin.get(), "M")
        sSec = self.check_ebox_validity(self.ebSec.get(), "S")

        return (sHour * 3600) + (sMin * 60) + sSec

    def conv_epoch_to_normal(self, iEpoch):
        iHour = iEpoch/3600
        iMin = iEpoch/60 - (iEpoch/3600)*60
        iSec = iEpoch % 60

        return iHour, iMin, iSec

    def handle_timer(self):
        if(self.iBtnPhase == 0):
            self.iHWND = GetForegroundWindow()
            self.iStart = time()
            self.iEnd = int(self.iStart + self.get_ebox_values())
            self.iCurr = 0
            self.iBtnPhase = 1
            self.svStartBtn.set("Pause")
            self.timer()

        elif(self.iBtnPhase == 1):
            self.svStartBtn.set("Start")
            self.iBtnPhase = 2
            print self.iCurr

        elif(self.iBtnPhase == 2):
            self.svStartBtn.set("Pause")
            self.iBtnPhase = 1
            print self.iCurr
            self.timer()

        elif(self.iBtnPhase == 3):
            self.svStartBtn.set("Done")
            self.btnWait['state'] = 'disabled'

    def timer(self):
        if(self.iBtnPhase == 1):
            while(time() < (self.iStart + self.iCurr + 1)):
                sleep(0.05)
                self.masterFrame.update()
                
            self.iCurr += 1
            iHour, iMin, iSec = self.conv_epoch_to_normal(int(self.iEnd - (self.iStart + self.iCurr)))
            self.svHour.set(iHour)
            self.svMin.set(iMin)
            self.svSec.set(iSec)
            print self.iCurr
            print time(),
            print (self.iStart + self.iCurr + 1)
            print time() < (self.iStart + self.iCurr + 1)

            if((self.iEnd > (self.iStart + self.iCurr))):
                self.timer()
            else:
                self.iBtnPhase = 3
                self.handle_timer()
                self.alarm()

    def alarm(self):
        self.masterFrame.update()
        FlashWindow(self.iHWND, 0)
        MessageBeep(20)

        if(GetForegroundWindow() != self.iHWND and self.iAlarmCtr <= 999):
            sleep(1)
            self.iAlarmCtr += 1
            self.alarm()


def main():
    root = Tk()
    root.wm_title("Tiny Timer")
    app = App(root)
    root.mainloop()
    root.destroy()

main()
