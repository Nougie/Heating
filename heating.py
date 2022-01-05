import time
import RPi.GPIO as GPIO
import sys

#target temperatures
temp_low=15.5
temp_high=17
manual=0

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

    temp=float(results.split(",")[3]) # temperature of Keukenplafond - sensor 28-01203333797e
    HM=int(time.strftime('%H''%M'))
#     print(time)

#    if (HM < 730 or HM > 1500) and temp < temp_high: # time between 6h30-7h30 or 15h00-22h30
    if HM > 1400 and temp < temp_high: # time between 14:00-
        GPIO.output(26,False)
        print("HM={} > 14h00 and temp = {} < temp_high".format(HM,temp))
    elif temp < temp_low:
        GPIO.output(26,False)
        print("{} : temp = {} < temp_low".format(HM,temp))
    else:
        GPIO.output(26,True)

    results = results + "\n"  
    
    with open("/home/pi/data_log.csv", "a") as file:            
        file.write(results)

    
#    if HM > 2300:
    if HM > 2000 + manual*200: # als manueel ingesteld verwarmen tot 22:00, anders tot 20:00
        GPIO.output(26,True)
#         GPIO.cleanup()
        print("{} PM. Go to sleep until around 6 AM".format(HM))
        time.sleep (36000 - 3600*2*manual) # 10h = 60*60*10 sec. 10 hours after 20h = 6h
    else:
        time.sleep (1200)    # change number of seconds to change time between sensor reads
