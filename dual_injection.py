'''
 This script demostrate how to use the I2C trigger machine. 
'''
import serial
from Spider import *
from Chronology import *
import time

if __name__ == '__main__':

    ## Setting Up Serial Ports
    Spider_com_port = serial.Serial()
    Spider_com_port.port = "COM7"

    Pinata_com_port = serial.Serial(
        port='COM6',
        baudrate=115200,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
    )

    Spider_com_port.close()
    Pinata_com_port.close()   

    Spider_com_port.open()
    Pinata_com_port.open()


    spiderCore1 = Spider(Spider.CORE1, Spider_com_port); # Instantiate a Spider object using CORE2
    spiderCore2 = Spider(Spider.CORE2, Spider_com_port)

    spiderCore1.resetSettings(); # Reset all the existing settings of CORE2
    spiderCore2.resetSettings(); # Reset all the existing settings of CORE2
    glitcher = Chronology(spiderCore1)

    glitcher.forgetEvents() # Forget any previous added events
    glitcher.setVccNow(Spider.GLITCH_OUT1, 3.3) # Set Vcc immediatly to 0 volts

    '''
    START TO ADD EVENTS
    '''
    #glitcher.setVcc(Spider.GLITCH_OUT1, 3.3) # After receiving the trigger, set GLITCH_OUT1 to 3.3 volts
    glitcher.waitTrigger(0, Spider.RISING_EDGE, 1) # Wait for a rising edge to appear on CORE1.Pin0 
    
    #glitcher.waitTime(100e-6) # Then wait for 100 us
    glitcher.glitch(Spider.GLITCH_OUT1, 1.5, 100e-6, 150e-9) # Then generate a glitch of -4.0 volts, with offset of 0, and duration of 100 ns
    glitcher.glitch(Spider.GLITCH_OUT1, 1.5, 70e-6, 150e-9) # Another glitch of -1.0 volts, with offset of 100 us, and duration of 500 ns
    glitcher.glitch(Spider.GLITCH_OUT1, 1.5, 5e-9, 150e-9)
    #glitcher.waitTime(0.5) # Wait 500 ms
    #glitcher.setVcc(Spider.GLITCH_OUT1, 0) # Set GLITCH_OUT1 to 0 volts

    #glitcher.reportEvents() # Generate a report of state utilization of above events

    glitcher.start() # Start to progress through the events

    time.sleep(0.2)
    ## Encryption 
    for i in range(1):
        cmd = [0xAE, 0x7B, 0xE9, 0x59, 0x01, 0xBD, 0x9F, 0x48, 0x31, 0x7B, 0xE9, 0x59, 0x01, 0xBD, 0x9F, 0x48, 0x31]
        Pinata_com_port.write(bytes((bytearray(cmd))))
        time.sleep(0.2)
        
        tmp =  list(Pinata_com_port.read(16))   
        print(tmp) 

    #print "Event sequence timed out: ", glitcher.waitUntilFinish(3000) # wait the events to finish, with a time out of 3000 ms

    Spider_com_port.close()
    Pinata_com_port.close()