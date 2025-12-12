#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
from enigma import eConsoleAppContainer
from Screens.Screen import Screen
from Components.ActionMap import ActionMap
from Components.ScrollLabel import ScrollLabel
from Components.Sources.StaticText import StaticText
from Screens.MessageBox import MessageBox
from enigma import getDesktop
from sys import version_info

# Python version detection
PY3 = version_info[0] == 3

def getDesktopSize():
    s = getDesktop(0).size()
    return (s.width(), s.height())

def isHD():
    desktopSize = getDesktopSize()
    return desktopSize[0] == 1280

class Console2(Screen):
    if isHD():
        skin = '''
            <screen name="Console2" position="center,center" size="800,533" title="Console" flags="wfBorder">
  <widget name="text" position="7,7" size="786,480" font="Regular;18" scrollbarMode="showOnDemand" />
  <widget name="key_red" position="7,493" size="107,33" font="Regular;15" foregroundColor="#000000" backgroundColor="#ff0069" halign="center" valign="center" transparent="0" />
  <widget name="key_green" position="120,493" size="107,33" font="Regular;15" foregroundColor="#000000" backgroundColor="#00ffa9" halign="center" valign="center" transparent="0" />
</screen>
'''
    else:
        skin = '''
            <screen name="Console2" position="center,center" size="1200,800" title="Console" flags="wfBorder">
  <widget name="text" position="10,10" size="1180,720" font="Regular;28" scrollbarMode="showOnDemand" />
  <widget name="key_red" position="10,740" size="160,50" font="Regular;22" foregroundColor="#000000" backgroundColor="#ff0069" halign="center" valign="center" transparent="0" />
  <widget name="key_green" position="180,740" size="160,50" font="Regular;22" foregroundColor="#000000" backgroundColor="#00ffa9" halign="center" valign="center" transparent="0" />
</screen>'''

    def __init__(self, session, title='Console', cmdlist=None, finishedCallback=None, closeOnSuccess=False, showStartStopText=True, skin=None):
        Screen.__init__(self, session)
        self.finishedCallback = finishedCallback
        self.closeOnSuccess = closeOnSuccess
        self.showStartStopText = showStartStopText
        if skin:
            self.skinName = [skin, 'Console2']
        self.errorOcurred = False
        self['text'] = ScrollLabel('')
        self['key_red'] = StaticText(_('Cancel'))
        self['key_green'] = StaticText(_('Hide'))
        self["actions"] = ActionMap(["WizardActions", "DirectionActions", 'ColorActions'],
        {
            "ok": self.cancel,
            "up": self["text"].pageUp,
            "down": self["text"].pageDown,
            "red": self.cancel,
            "green": self.toggleHideShow,
            "blue": self.restartenigma,
            "exit": self.cancel,
        }, -1)
        self.cmdlist = isinstance(cmdlist, list) and cmdlist or [cmdlist]
        self.newtitle = title == 'Console' and _('Console') or title
        self.cancel_msg = None
        self.onShown.append(self.updateTitle)
        self.container = eConsoleAppContainer()
        self.run = 0
        self.finished = False
        try:  ## DreamOS By RAED
            self.container.appClosed.append(self.runFinished)
            self.container.dataAvail.append(self.dataAvail)
        except:
            self.container.appClosed_conn = self.container.appClosed.connect(self.runFinished)
            self.container.dataAvail_conn = self.container.dataAvail.connect(self.dataAvail)
        self.onLayoutFinish.append(self.startRun)

    def updateTitle(self):
        self.setTitle(self.newtitle)

    def startRun(self):
        if self.showStartStopText:
            self['text'].setText(_('Execution progress:') + '\n\n')
        print('[Console] executing in run', self.run, ' the command:', self.cmdlist[self.run])
        if self.container.execute(self.cmdlist[self.run]):
            self.runFinished(-1)

    def runFinished(self, retval):
        if retval:
            self.errorOcurred = True
        self.show()
        self.run += 1
        if self.run != len(self.cmdlist):
            if self.container.execute(self.cmdlist[self.run]):
                self.runFinished(-1)
        else:
            self.show()
            self.finished = True
            try:
                lastpage = self['text'].isAtLastPage()
            except:
                lastpage = self['text']
            if self.cancel_msg:
                self.cancel_msg.close()
            if self.showStartStopText:
                self['text'].appendText(_('Execution finished!!'))
            if self.finishedCallback is not None:
                self.finishedCallback()
            if not self.errorOcurred and self.closeOnSuccess:
                self.closeConsole()
            else:
                self['text'].appendText(_('\nPress OK or Exit to abort!'))
                self['key_red'].setText(_('Exit'))
                self['key_green'].setText('')

    def toggleHideShow(self):
        if self.finished:
            return
        if self.shown:
            self.hide()
        else:
            self.show()

    def cancel(self):
        if self.finished:
            self.closeConsole()
        else:
            self.cancel_msg = self.session.openWithCallback(self.cancelCallback, MessageBox, _('Cancel execution?'), type=MessageBox.TYPE_YESNO, default=False)

    def cancelCallback(self, ret=None):
        self.cancel_msg = None
        if ret:
            try:  ## DreamOS By RAED
                self.container.appClosed.remove(self.runFinished)
                self.container.dataAvail.remove(self.dataAvail)
            except:
                self.container.appClosed_conn = None
                self.container.dataAvail_conn = None
            self.container.kill()
            self.close()

    def closeConsole(self):
        if self.finished:
            try:  ## DreamOS By RAED
                self.container.appClosed.remove(self.runFinished)
                self.container.dataAvail.remove(self.dataAvail)
            except:
                self.container.appClosed_conn = None
                self.container.dataAvail_conn = None
            self.close()
        else:
            self.show()

    def dataAvail(self, str):
        """Handle console output - fixed for Python 2/3 compatibility"""
        # FIX: Convert bytes to string if needed (Python 3)
        if PY3 and isinstance(str, bytes):
            try:
                str = str.decode('utf-8')
            except UnicodeDecodeError:
                # Fallback to latin-1 if utf-8 fails
                str = str.decode('latin-1', errors='ignore')
        
        # Now safely append the string
        self['text'].appendText(str)

    def restartenigma(self):
        from Screens.Standby import TryQuitMainloop
        self.session.open(TryQuitMainloop, 3)
