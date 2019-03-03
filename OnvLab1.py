from onvif import ONVIFCamera
from time import sleep

class Test:
	def __init__(self,ip,port,user,passw):
		self.ip = ip
		self.port = port
		self.user = user
		self.passw = passw
		self.cam = ONVIFCamera(self.ip, self.port, self.user, self.passw)
	def AbsoluteMoveSupport(self):
		media = self.cam.create_media_service() #Creating media service
		profiles = media.GetProfiles()		    #Getting the list with profiles' info
		token = profiles[0]._token  		    #Getting token from the first protile, we'll need it soon
		ptz = self.cam.create_ptz_service()		#Creating ptz service
		ptz_token = profiles[0].PTZConfiguration._token #Saving ptz config token
		ptz.create_type("AbsoluteMove")			#creating new type of ptz
		
		try:
			pos = ptz.GetStatus({"ProfileToken": token}).Position # getting current position
			x_z = pos.Zoom._x
			x = pos.PanTilt._x
			y = pos.PanTilt._y
			if ((x + 0.1) < 1):   #checking if x max or min, so we decrease or increase the number
				x1 = x + 0.1
			else:
				x1 = x - 0.1
			if ((y + 0.1) < 1):   #checking if y max or min, so we decrease or increase the number
				y1 = y + 0.1
			else:
				y1 = y - 0.1
			if ((x_z + 0.1) < 1): #checking if x_z max or min, so we decrease or increase the number
				x_z1 = x_z + 0.1
			else:
				x_z1 = x_z - 0.1
			ptz.AbsoluteMove({"ProfileToken": token, "Position":{"PanTilt":{"_x": x1,"_y": y1}, "Zoom":{"_x": x_z1}}})#AbsoluteMove to new parameter x1
			sleep(3) 											   #Wait for camera to move
			pos = ptz.GetStatus({"ProfileToken": token}).Position  #Getting new position
			x_z = pos.Zoom._x					 #
			x = pos.PanTilt._x					 #Updating current coordinates
			y = pos.PanTilt._y					 #
			dif1 = (round((x1-x),6))
			dif2 = (round((y1-y),6))
			dif3 = (round((x_z1-x_z),6))
			# print dif1, ' ', dif2, ' ',dif2
			if ((dif1 == 0) & (dif2 == 0) & (dif3 == 0)):								              #Checking, if camera moved
				return 'AbsoluteMove is supported, current coordinates: ' +  str(x) + ' ' + str(y) + ' ' + str(x_z)
			else:
				return 'AbsoluteMove is not supported, it does not follow instructions'
		except AttributeError:
			return 'AbsoluteMove is not supported, AttributeError'

	def Focus(self):
		media = self.cam.create_media_service() 	#Creating media service
		profiles = media.GetProfiles() 				#Getting the list with profiles' info
		imaging = self.cam.create_imaging_service() #Creating imaging service
		token = profiles[0]._token   	        	#Getting token from the first protile, we'll need it soon
		vstoken = media.GetVideoSources()[0]._token #Getting videosources token

		print 'imaging status(position):'                     #printing Imaging Status
		print imaging.GetStatus({'VideoSourceToken': vstoken}).FocusStatus20.Position
		options = imaging.GetMoveOptions({'VideoSourceToken': vstoken})
		imaging.create_type('Move')					#Creating new type of imaging
		#Stopping imaging before start to disturb (if it was) previous moving and setting focus to manual
		imaging.Stop({'VideoSourceToken': vstoken})
		focus = imaging.SetImagingSettings({'VideoSourceToken': vstoken, 'ImagingSettings': {'Focus': {'AutoFocusMode': 'MANUAL'}}})
		try:
			options.Absolute #Checking if absolutemove options are supported and trying absolutemove
			abs_mov = imaging.Move({'VideoSourceToken': vstoken, 'Focus': {'Absolute': {'Position': 0.5, 'Speed': 0.5}}})
			sleep(5) #waiting
			imaging.Stop({'VideoSourceToken': vstoken}) #stopping imaging
			print 'imaging status(position):'           #Getiing current position of imaging
			print imaging.GetStatus({'VideoSourceToken': vstoken}).FocusStatus20.Position
			print 'Absolute imaging is supported, check if it is working. Now trying Continuous imaging'
		except AttributeError: 			#Catching error
			print 'Absolute Imaging is not supported, trying Continuous imaging...'
		print 'sleep 4s'
		sleep(4)
		try:
			options.Continuous
			cont_mov = imaging.Move({'VideoSourceToken': vstoken, #trying continious move if it's supported
									 'Focus':{
										       'Continuous': {'Speed': +0.5}}})
			sleep(2)
			imaging.Stop({'VideoSourceToken': vstoken})
			print 'imaging status(position):'  #Getting current position
			print imaging.GetStatus({'VideoSourceToken': vstoken}).FocusStatus20.Position
			print 'Continuous imaging works'
		except AttributeError:                 #Catching error
			print 'Continious Imaging is not supported'	 #setting autofocus mode back
		imaging.SetImagingSettings({'VideoSourceToken': vstoken, 'ImagingSettings': {'Focus': {'AutoFocusMode': 'AUTO'}}})
		return 'Test done'
		



Inst = Test('192.168.11.12', 80, 'admin', 'Supervisor')
print Inst.AbsoluteMoveSupport()
print Inst.Focus()