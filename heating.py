import time
import RPi.GPIO as GPIO
import sys

#target temperatures
temp_low=15.5
temp_high=17

manual=0
collectSun=0
shortsleep=0

# overrule target temperatures if manual command such as: python heater.py 19
if len(sys.argv) > 1:
    temp_low=float(sys.argv[1])
    temp_high=float(sys.argv[1])
    manual=1
    print("Heating manually overruled, new target temperature = {}".format(sys.argv[1]))

# set GPIO numbering mode and define output pins
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
# GPIO.setup(20,GPIO.OUT)
GPIO.setup(26,GPIO.OUT) #this seems like the only pin needed for our thermostat
# GPIO.setup(21,GPIO.OUT)

#######Read and write SENSOR data ###########
#cat /sys/bus/w1/devices/28-01203335f00a/w1_slave & cat /sys/bus/w1/devices/28-01203320a597/w1_slave
sensorids = ["28-01203335f00a", "28-01203320a597", "28-01203333797e"] # place the ID's of your ds18b20's in here

def read_temp_raw():
    f = open(device_file, "r")
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != "YES":
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find("t=")
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        
        return temp_c
        
while True:
    
    results = time.strftime("%Y-%m-%d %H:%M")
    for sensor in range(len(sensorids)):
        device_file = "/sys/bus/w1/devices/"+ sensorids[sensor] +"/w1_slave"
        temperature = (read_temp())
        dtemp = "%.1f" % temperature
        results = results + "," + str(dtemp)
    results = results + "\n"  
    
    with open("/home/pi/data_log.csv", "a") as file:            
        file.write(results)
        
    tempKitchen=float(results.split(",")[3]) # temperature of Kitchen ceiling - sensor 28-01203333797e
    tempSolar=float(results.split(",")[1]) # temperature of output of Solar Collector - sensor 28-01203335f00a
#    tempTank=float(results.split(",")[4]) # temperature at bottom of Water Storage Tank - sensor 28-XXXXXXX
    HM=int(time.strftime('%H''%M'))
#     print(time)

#############Thermostat###########
#    if (HM < 730 or HM > 1500) and temp < temp_high: # time between 6h30-7h30 or 15h00-22h30
    if HM > 1400 and tempKitchen < temp_high: # time between 14h and 20/22h
        GPIO.output(26,False)
        print("HM=HH:mm={} > 14h00 and temp = {} < temp_high".format(HM,tempKitchen))
    elif tempKitchen < temp_low:
        GPIO.output(26,False)
        print("HM=HH:mm={} : temp = {} < temp_low".format(HM,tempKitchen))
    else:
        GPIO.output(26,True)

###########Solar Collector##########
    
    if tempSolar > 60: # or (shortsleep and tempSolar > tempTank):
        # GPIO.output(21,False)
        collectSun = 1
        print("HM=HH:mm={}, tempSolar = {} thus relay of pump solar on".format(HM,tempSolar))

        else: 
            # GPIO.output(21,True)
            collectSun = 0

######Sleep#######            
#    if HM > 2300:
    if HM > 2000 + manual*200: # als manueel ingesteld verwarmen tot 22:00, anders tot 20:00
        GPIO.output(26,True)
#         GPIO.cleanup()
        print("{} PM. Go to sleep until around 6 AM".format(HM))
        time.sleep (36000 - 3600*2*manual) # 10h = 60*60*10 sec. 10 hours after 20h = 6h
        shortSleep=0
    elif collectSun=1:
        time.sleep (30)
        shortSleep=1
    else:
        time.sleep (1200)    # change number of seconds to change time between sensor reads
        shortSleep=0
