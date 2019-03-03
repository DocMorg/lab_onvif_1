# Key Bindings
# 8 - 56
# 6 - 54
# 4 - 52
# 2 - 50
# + - 43
# - - 45
# * - 42
# / - 47

from onvif import ONVIFCamera
from getch.getch import getch

class Continious_Ptz():
    def __init__(self,ip,port,user,passw):            #Init'ing class
        self.ip = ip
        self.port = port
        self.user = user
        self.passw = passw
        self.cam = ONVIFCamera(self.ip, self.port, self.user, self.passw)
        global ptz
        print 'Connected to ONVIF Camera ' + ip
        token = self.cam.create_media_service().GetProfiles()[0]._token #Getting profile's token
        ptz = self.cam.create_ptz_service()                             #Creating ptz service
        self.Define_Requests(token)

    def Define_Requests(self, token):      #Defining global requests
        global req_move, req_stop, req_goto_home

        req_move = ptz.create_type('ContinuousMove')
        req_move.ProfileToken = token

        req_stop = ptz.create_type('Stop')
        req_stop.ProfileToken = token

        req_goto_home = ptz.create_type('GotoHomePosition')
        req_goto_home.ProfileToken = token

    def stop(self):
        ptz.Stop(req_stop)

    def move_left(self, speed=0.5):                     #Setting functions to
        req_move.Velocity.Zoom._x = 0.0                 #handle all entries from keyboard
        req_move.Velocity.PanTilt._x = -speed
        req_move.Velocity.PanTilt._y = 0.0
        ptz.ContinuousMove(req_move)
        self.stop()

    def move_right(self, speed=0.5):
        req_move.Velocity.Zoom._x = 0.0
        req_move.Velocity.PanTilt._x = speed
        req_move.Velocity.PanTilt._y = 0.0
        ptz.ContinuousMove(req_move)
        self.stop()

    def move_down(self, speed=0.5):
        req_move.Velocity.Zoom._x = 0.0
        req_move.Velocity.PanTilt._x = 0.0
        req_move.Velocity.PanTilt._y = -speed
        ptz.ContinuousMove(req_move)
        self.stop()

    def move_up(self, speed=0.5):
        req_move.Velocity.Zoom._x = 0.0
        req_move.Velocity.PanTilt._x = 0.0
        req_move.Velocity.PanTilt._y = speed
        ptz.ContinuousMove(req_move)
        self.stop()

    def move_right_up(self, speed=0.5):
        req_move.Velocity.Zoom._x = 0.0
        req_move.Velocity.PanTilt._x = speed
        req_move.Velocity.PanTilt._y = speed
        ptz.ContinuousMove(req_move)
        self.stop()

    def move_left_up(self, speed=0.5):
        req_move.Velocity.Zoom._x = 0.0
        req_move.Velocity.PanTilt._x = -speed
        req_move.Velocity.PanTilt._y = speed
        ptz.ContinuousMove(req_move)
        self.stop()

    def move_right_down(self, speed=0.5):
        req_move.Velocity.Zoom._x = 0.0
        req_move.Velocity.PanTilt._x = speed
        req_move.Velocity.PanTilt._y = -speed
        ptz.ContinuousMove(req_move)
        self.stop()

    def move_left_down(self, speed=0.5):
        req_move.Velocity.Zoom._x = 0.0
        req_move.Velocity.PanTilt._x = -speed
        req_move.Velocity.PanTilt._y = -speed
        ptz.ContinuousMove(req_move)
        self.stop()

    def move_home(self):
        ptz.GotoHomePosition(req_goto_home)
   
    def zoom_in(self, speed=0.5):
        self.stop()
        req_move.Velocity.PanTilt._x = 0.0
        req_move.Velocity.PanTilt._y = 0.0
        req_move.Velocity.Zoom._x = speed
        ptz.ContinuousMove(req_move)

    def zoom_out(self, speed=0.5):
        self.stop()
        req_move.Velocity.PanTilt._x = 0.0
        req_move.Velocity.PanTilt._y = 0.0
        req_move.Velocity.Zoom._x = -speed
        ptz.ContinuousMove(req_move)

cam = Continious_Ptz('192.168.11.12', 80, 'admin', 'Supervisor')
print 'Press ESC to exit'
speed = 0.5
while True:
    key = ord(getch())
    if key == 27: #ESC
        break
    elif key == 56: #Up
        cam.move_up(speed)
    elif key == 50: #Down
        cam.move_down(speed)
    elif key == 54: #Right
        cam.move_right(speed)
    elif key == 52: #Left
        cam.move_left(speed)
    elif key == 53: #Home
        cam.move_home()
    elif key == 57: #Right Up
        cam.move_right_up(speed)
    elif key == 55: #Left Up
        cam.move_left_up(speed)
    elif key == 49: #Left Down
        cam.move_left_down(speed)
    elif key == 51: #Right Down
        cam.move_right_down(speed)
    elif key == 43: #Plus(+)
        cam.zoom_in(speed)
    elif key == 45: #Minus(-)
        cam.zoom_out(speed)
    elif key == 47: #Divide(/)
        if (speed >= 0.2):
            speed = speed - 0.1
            print 'Current speed:', speed
        else:
            print 'Min speed already'
    elif key == 42: #Myltiply(*)
        if (speed <= 0.9):
            speed = speed + 0.1
            print 'Current speed:', speed
        else:
            print 'Max speed already'
