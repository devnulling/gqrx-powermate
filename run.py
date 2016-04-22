from powermate import PowerMateBase, LedEvent, MAX_BRIGHTNESS
import glob
import telnetlib
import subprocess
from time import sleep
import os

debugMode = 0
currentMode = "OFF"
stepLeft = 1000
stepRight = 10000

freqSteps = [1, 10, 100, 1000, 10000, 100000, 1000000, 10000000, 100000000]
deModes = ['OFF', 'RAW', 'AM', 'FM', 'WFM', 'WFM_ST', 'LSB', 'USB', 'CW', 'CWL', 'CWU']

class Gqrx():

    def _request(self, request):
        global debugMode
        if debugMode == 1:
            print request
        else:
            con = telnetlib.Telnet('127.0.0.1', 7356)
            con.write(('%s\n' % request).encode('ascii'))
            response = con.read_some().decode('ascii').strip()
            con.write('c\n'.encode('ascii'))
            return response

    def set_frequency(self, frequency):
        return self._request('F %s' % frequency)

    def get_frequency(self):
        return self._request('f')

    def set_mode(self, mode):
        return self._request('M %s' % mode)

    def get_mode(self):
        return self._request('m')

    def get_level(self):
        return self._request('l')
    
    
def getlevel():
    gqrx = Gqrx()
    level = gqrx.get_level()
    print level
    
def switchmode():
    global currentMode
    global deModes
    
    curModePos = deModes.index(currentMode)
    newModePos = int(curModePos) + 1
    
    if newModePos >= len(deModes):
        newModePos = 0
    
    currentMode = deModes[newModePos]
    gqrx = Gqrx()
    result = gqrx.set_mode(currentMode)
    print result
    print currentMode
    
    
    
def incstep(side):
    global stepLeft
    global stepRight
    global freqSteps
    
    if side == "left":
        currentStep = stepLeft
        stepPos = freqSteps.index(currentStep)
        newPos = int(stepPos) + 1
        if newPos >= len(freqSteps):
            newPos = 0
        stepLeft = freqSteps[newPos]
    elif side == "right":
        currentStep = stepRight
        stepPos = freqSteps.index(currentStep)
        newPos = int(stepPos) + 1
        if newPos >= len(freqSteps):
            newPos = 0
        stepRight = freqSteps[newPos]
    

def decstep(side):
    global stepLeft
    global stepRight
    global freqSteps
    
    if side == "left":
        currentStep = stepLeft
        stepPos = freqSteps.index(currentStep)
        newPos = int(stepPos) - 1
        if newPos == -1:
            newPos = len(freqSteps)-1
        stepLeft = freqSteps[newPos]
    elif side == "right":
        currentStep = stepRight
        stepPos = freqSteps.index(currentStep)
        newPos = int(stepPos) - 1
        if newPos == -1:
            newPos = len(freqSteps)-1
        stepRight = freqSteps[newPos]
  
    
def incfreq(side):
    global stepLeft
    global stepRight
    currentStep = 0
    left = "left"
    right = "right"
    
    if side == left:
        currentStep = stepLeft
    elif side == right:
        currentStep = stepRight
    else:
        currentStep = 0
        
    print 'running inc freq'
    if debugMode == 1:
        freq = 1
    else:
        gqrx = Gqrx()
        freq = gqrx.get_frequency()
        print freq
        setfreq = int(freq) + currentStep
        set = gqrx.set_frequency(setfreq)
        nf = gqrx.get_frequency()
        print nf

def decfreq(side):
    global stepLeft
    global stepRight
    currentStep = 0
    left = "left"
    right = "right"
    
    if side == left:
        currentStep = stepLeft
    elif side == right:
        currentStep = stepRight
    else:
        currentStep = 0
        
    print 'running dec freq'
    if debugMode == 1:
        freq = 1
    else:
        gqrx = Gqrx()
        freq = gqrx.get_frequency()
        print freq
        setfreq = int(freq)-currentStep
        set = gqrx.set_frequency(setfreq)
        nf = gqrx.get_frequency()
        print nf

class ExamplePowerMate(PowerMateBase):
  def __init__(self, path):
    super(ExamplePowerMate, self).__init__(path)
    self._pulsing = False
    self._brightness = MAX_BRIGHTNESS

  def short_press(self):
    print('Short press!')
    self._pulsing = not self._pulsing
    print(self._pulsing)
    if self._pulsing:
      return LedEvent.pulse()
    else:
      return LedEvent(brightness=self._brightness)

  def long_press(self):
    print('Long press!')

  def rotate(self, rotation):
    if rotation == 1:
      incfreq("right")
    elif rotation == -1:
      decfreq("right")

    print('Rotate {}!'.format(rotation))
    self._brightness = max(0, min(MAX_BRIGHTNESS, self._brightness + rotation))
    self._pulsing = False
    return LedEvent(brightness=self._brightness)

  def push_rotate(self, rotation):
    if rotation == 1:
      incfreq("left")
    elif rotation == -1:
      decfreq("left")
    print('Push rotate {}!'.format(rotation))

if __name__ == '__main__':
  pm = ExamplePowerMate(glob.glob('/dev/input/by-id/*PowerMate*')[0])
  pm.run()
