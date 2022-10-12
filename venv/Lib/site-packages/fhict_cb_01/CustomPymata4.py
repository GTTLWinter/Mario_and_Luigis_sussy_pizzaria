from pymata4 import pymata4

class CustomPymata4(pymata4.Pymata4):

    def __init__(self, com_port=None, baud_rate=57600,
                 arduino_instance_id=1, arduino_wait=4,
                 sleep_tune=0.000001,
                 shutdown_on_exception=True):
            super().__init__(com_port, baud_rate, arduino_instance_id, 
                             arduino_wait, sleep_tune, shutdown_on_exception)

           
    def displayOff(self) :
        self._send_sysex(self._DISPLAY_OFF)
    
    def displayOn(self) :
        self._send_sysex(self._DISPLAY_ON)
    
    def displayClear(self) :
        self._send_sysex(self._DISPLAY_CLEAR)
        
    def displaySetBrightness(self, brightness) :
        self._send_sysex(self._DISPLAY_SET_BRIGHTNESS, [brightness])
        
    def displayCharAt(self, pos, char, showDot=False):
        """
        Configure dht sensor prior to operation.
        @param pos n number on arduino
        @param char
        """
        data = [pos, char, showDot]
        self._send_sysex(self._DISPLAY_SHOW_CHAR, data)

    def displayShow(self, value) :
        string = str(value)
        self.displayClear()
        pos = 0
        prev = '.'
        for letter in string:
            if letter == '.' and prev != '.':
                self.displayCharAt(pos - 1, ord(prev), showDot = True)
            else :
                self.displayCharAt(pos, ord(letter), showDot = False)
                pos += 1
            prev = letter
    """
    Private Sysex commands
    """
    _DISPLAY_OFF            = 0x0F
    _DISPLAY_ON             = 0x0E
    _DISPLAY_CLEAR          = 0x0D
    _DISPLAY_SET_BRIGHTNESS = 0x0C
    _DISPLAY_SHOW_CHAR      = 0x0B