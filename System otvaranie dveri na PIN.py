
import I2C_LCD_driver
import RPi.GPIO as GPIO
from time import sleep

C1 = 5
C2 = 6
C3 = 13
C4 = 19

R1 = 12
R2 = 16
R3 = 20
R4 = 21

buzzer = 17

Relay = 27
relayState = True

lcd = I2C_LCD_driver.LCD()

lcd.lcd_display_string("System sa zapina",1)
for a in range (0,16):
    lcd.lcd_display_string_pos(".",2,a)
    sleep(0.1)
lcd.lcd_clear()

keypadPressed = -1

secretCode = "1111"
input = ""

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer,GPIO.OUT)
GPIO.setup(Relay,GPIO.OUT)
GPIO.output(Relay,GPIO.HIGH)

GPIO.setup(C1, GPIO.OUT)
GPIO.setup(C2, GPIO.OUT)
GPIO.setup(C3, GPIO.OUT)
GPIO.setup(C4, GPIO.OUT)

GPIO.setup(R1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(R2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(R3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(R4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def keypadCallback(channel):
    global keypadPressed
    if keypadPressed == -1:
        keypadPressed = channel

GPIO.add_event_detect(R1, GPIO.RISING, callback=keypadCallback)
GPIO.add_event_detect(R2, GPIO.RISING, callback=keypadCallback)
GPIO.add_event_detect(R3, GPIO.RISING, callback=keypadCallback)
GPIO.add_event_detect(R4, GPIO.RISING, callback=keypadCallback)

def setAllColumns(state):
    GPIO.output(C1, state)
    GPIO.output(C2, state)
    GPIO.output(C3, state)
    GPIO.output(C4, state)

def commands():
    global relayState
    global input
    pressed = False
    GPIO.output(C1, GPIO.HIGH)
    
    
    if (GPIO.input(R1) == 1):
        print("Premenná input sa resetuje!");
        lcd.lcd_clear()
        lcd.lcd_display_string("Vymazane        ",1)
        sleep(1)
        pressed = True
    GPIO.output(C1, GPIO.HIGH)
    
    if (not pressed and GPIO.input(R2) == 1):
        if input == secretCode:
            print("Správny PIN!")
            lcd.lcd_clear()
            lcd.lcd_display_string("Spravny PIN!    ",1)
            
            if relayState:
                GPIO.output(Relay,GPIO.LOW)
                GPIO.output(buzzer,GPIO.HIGH)
                sleep(0.3)
                GPIO.output(buzzer,GPIO.LOW)
                sleep(1)
                relayState = False
                
            else:
                GPIO.output(Relay,GPIO.HIGH)
                GPIO.output(buzzer,GPIO.HIGH)
                sleep(0.3)
                GPIO.output(buzzer,GPIO.LOW)
                sleep(1)
                relayState = True
                  
            
        else:
            print("Nesprávny PIN!")
            lcd.lcd_clear()
            lcd.lcd_display_string("Nespravny PIN!  ",1)
            GPIO.output(buzzer,GPIO.HIGH)
            sleep(0.3)
            GPIO.output(buzzer,GPIO.LOW)
            sleep(0.3)
            GPIO.output(buzzer,GPIO.HIGH)
            sleep(0.3)
            GPIO.output(buzzer,GPIO.LOW)
            sleep(0.3)
            GPIO.output(buzzer,GPIO.HIGH)
            sleep(0.3)
            GPIO.output(buzzer,GPIO.LOW) 
        pressed = True
    GPIO.output(C1, GPIO.LOW)
    if pressed:
        input = ""
    return pressed

def read(column, characters):
    global input
    GPIO.output(column, GPIO.HIGH)
    if(GPIO.input(R1) == 1):
        input = input + characters[0]
        print(input)
        lcd.lcd_display_string(str(input),2)
    if(GPIO.input(R2) == 1):
        input = input + characters[1]
        print(input)
        lcd.lcd_display_string(str(input),2)
    if(GPIO.input(R3) == 1):
        input = input + characters[2]
        print(input)
        lcd.lcd_display_string(str(input),2)
    if(GPIO.input(R4) == 1):
        input = input + characters[3]
        print(input)
        lcd.lcd_display_string(str(input),2)
    GPIO.output(column, GPIO.LOW)
try:
    while True:       
        lcd.lcd_display_string("Zadajte PIN:    ",1)
        
 
        if keypadPressed != -1:
            setAllColumns(GPIO.HIGH)
            if GPIO.input(keypadPressed) == 0:
                keypadPressed = -1
            else:
                sleep(0.1)
       
        else:
            if not commands():
                read(C1, ["D","C","B","A"])
                read(C2, ["#","9","6","3"])
                read(C3, ["0","8","5","2"])
                read(C4, ["*","7","4","1"])
                sleep(0.1)
            else:
                sleep(0.1)
except KeyboardInterrupt:
    print("Zastavené!")