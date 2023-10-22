import time
import RPi.GPIO as GPIO
import sys

#target temperatures
temp_low=17.2
temp_high=17.7

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
GPIO.setup(20,GPIO.OUT) #eerste relay voor solar
GPIO.setup(26,GPIO.OUT) #this seems like the only pin needed for our thermostat
# GPIO.setup(21,GPIO.OUT)

#######Read and write SENSOR data ###########
#cat /sys/bus/w1/devices/28-01203335f00a/w1_slave & cat /sys/bus/w1/devices/28-01203320a597/w1_slave
sensorids = ["28-01203335f00a", "28-01203320a597", "28-01203333797e", "28-01203303fd63"] # place the ID's of your ds18b20's in here
#see lines around 73 for the identification of these sensors 

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

    
#####if Night: sleep#######
    HM=int(time.strftime('%H''%M'))
    if HM > 2000 + manual*200: # als manueel ingesteld verwarmen tot 22:00, anders tot 20:00
        GPIO.output(26,True)
        GPIO.output(20,True)
#        GPIO.cleanup() # ATTENTION, this will give something like GPIO not set-up error..
        print("{} PM. Go to sleep until around 6 AM".format(HM))
        time.sleep (36000 - 3600*2*manual) # 10h = 60*60*10 sec. 10 hours after 20h = 6h

###########Solar Collector##########
               
    else:
        for x in range(10): # this for-loop assures a sleep of in total 10 times 120 seconds  
            timestamp = time.strftime("%Y-%m-%d %H:%M")
            results = timestamp #rest of the array results will be added in following lines
            for sensor in range(len(sensorids)):
                device_file = "/sys/bus/w1/devices/"+ sensorids[sensor] +"/w1_slave"
                temperature = (read_temp())
                dtemp = "%.1f" % temperature
                results = results + "," + str(dtemp)
            results = results + "\n"
            
            tempSolar=float(results.split(",")[1]) # temperature of output of Solar Collector - sensor 28-01203335f00a
            tempKitchen=float(results.split(",")[3]) # temperature of Kitchen ceiling - sensor 28-01203333797e
            tempTank=float(results.split(",")[4]) # temperature at bottom of Water Storage Tank - sensor 28-01203303fd63
            
            if tempSolar > tempTank+1: # +1 because tempTank sensor underestimates real storage tank temperature 
                GPIO.output(20,False)
                print("{} : tempSolar = {} > (tempTank = {})+1".format(timestamp,tempSolar,tempTank))
            else:
                GPIO.output(20,True)
            time.sleep (120)    # change number of seconds to change time between sensor reads: 120 seconds = 2 minutes
    
        ### write results every 10 x 120 seconds = every 20 minutes
        with open("data_log.csv", "a") as file:            
            file.write(results)    

    #############Thermostat###########
    #    if (HM < 730 or HM > 1500) and temp < temp_high: # time between 6h30-7h30 or 15h00-22h30
        if int(time.strftime('%H''%M')) > 1400 and tempKitchen < temp_high: # time between 14h and 20/22h
            GPIO.output(26,False)
            print("{} > 14h00 and temp = {} < temp_high".format(timestamp,tempKitchen))
        elif tempKitchen < temp_low:
            GPIO.output(26,False)
            print("{} : temp = {} < temp_low".format(timestamp,tempKitchen))
        else:
            GPIO.output(26,True)

