import sys, termios, tty, os, time, pygame, io, numpy, cv2
import RPi.GPIO as GPIO
from pygame import K_w, K_s, K_q, K_a, K_d
from pygame.locals import *
from picamera.array import PiRGBArray
from picamera import PiCamera
from multiprocessing import Process

foo = sys.argv

def motorController():

	GPIO.setwarnings(False)

	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(07, GPIO.OUT)
	GPIO.setup(11, GPIO.OUT)

	pwm = GPIO.PWM(07, 50)
	pwm.start(0)
	duty = 8.0

	pwm2 = GPIO.PWM(11, 50)
	pwm2.start(0)
	duty2 = 9.5

	pygame.init()

	size = width, height = 600, 400
	screen = pygame.display.set_mode(size)

	while True:
	
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()


		if pygame.key.get_pressed()[pygame.K_w] and duty <= 13.5:
			duty = duty + 0.5
			pwm.ChangeDutyCycle(duty)
		elif pygame.key.get_pressed()[K_s] and duty >= 4:
			duty = duty - 0.5
			pwm.ChangeDutyCycle(duty)
		if pygame.key.get_pressed()[K_q]:
			break
		if pygame.key.get_pressed()[K_a] and duty2 <= 13.5:
			duty2 = duty2  + 0.5
			pwm2.ChangeDutyCycle(duty2)
		elif pygame.key.get_pressed()[K_d] and duty2 >= 4:
			duty2 = duty2 - 0.5	
			pwm2.ChangeDutyCycle(duty2)		 
		time.sleep(0.05) 
		pygame.event.get()
def facialDetection():
	start_time = time.time()
	camera = PiCamera()
	camera.resolution = (400,300)
	camera.framerate = 32
	rawCapture = PiRGBArray(camera, size=(400,300))
	time.sleep(0.1)
	face_cascade = cv2.CascadeClassifier('lbp.xml')
	for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
		start_time = time.time()
		image = frame.array
		gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
		faces = face_cascade.detectMultiScale(gray, 1.1, 5)

		print ("Founod " + str(len(faces)) + "facee(s)")
		
		for (x, y, w, h) in faces:
			cv2.rectangle(image, (x,y),(x+w, y+h), (255,255,0),2)
		
		cv2.imshow("Frame", image)
		key = cv2.waitKey(1) & 0xFF
		rawCapture.truncate(0)
		print ("--- %s seconds ---" % (time.time()-start_time))
		if key == ord("q"):
			break
def runMotors():
	p = Process(target = motorController)
	p.start()
def runDetection():
	p = Process(target = facialDetection)
	p.start()

settings = {
	'motors':runMotors,
	'facialDetection':runDetection
}
for i in range(len(foo)):
	if i == 0:
		continue
	else:
		print str(foo[i])
		settings[str(foo[i])]()
