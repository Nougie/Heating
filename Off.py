# import GPIO and time
import RPi.GPIO as GPIO
import time

# set GPIO numbering mode and define output pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(20,GPIO.OUT)
GPIO.setup(26,GPIO.OUT)
GPIO.setup(21,GPIO.OUT)

# try:
#     while True:

# GPIO.output(26,True)
GPIO.cleanup()
        # false is blijkbaar (normally open) schakelaar die sluit
#         GPIO.output(20,True)
#         GPIO.output(21,True)

# finally:
# # cleanup the GPIO before finishing :)
#     GPIO.cleanup()
#     



