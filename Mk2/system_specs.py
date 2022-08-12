import os

import psutil
import pyttsx3
import screen_brightness_control as sbc

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def respond(audio):
    engine.say(audio)
    engine.runAndWait()


class Battery:
    def __init__(self):
        pass

    def Status(self):
        battery = psutil.sensors_battery()
        respond("Your system is at " + str(battery.percent) + " percent")


class CPU:
    def __init__(self):
        pass

    def Status(self):
        respond("CPU is at " + str(psutil.cpu_percent()))


class Memory:
    def __init__(self):
        pass

    def Usage(self):
        process_id = os.getpid()
        py = psutil.Process(process_id)
        memory_use = round(py.memory_info()[0] / 2. ** 30, 2)
        respond(" I am currently using {} Gb of memory".format(memory_use))


class Brightness:
    def __init__(self):
        pass

    def Status(self):
        current_brightness_level = sbc.get_brightness()
        return current_brightness_level

    def SetBrightness(self, data):
        try:
            sbc.set_brightness(data)
            respond("Brightness set successfully!")
        except:
            respond("Sorry sir, I am unable to do that")

    def Increase(self):
        try:
            current_brightness = Brightness().Status()
            if current_brightness >= 100:
                respond("Sorry sir, I can't further increase brightness as it is already in maximum state")
            else:
                sbc.set_brightness('+10')
                respond("Brightness Increased")
        except:
            respond("Sorry sir, I can't further increase brightness as it is already in maximum state")

    def Decrease(self):
        try:
            current_brightness = Brightness().Status()
            if current_brightness - 10 >= 0:
                sbc.set_brightness('-10')
            else:
                sbc.set_brightness(0)
            respond("Brightness Decreased")
        except:
            respond("Sorry sir, I can't further decrease brightness as it is already in minimum state")


def System_specs(data):
    if "battery" in data:
        battery = Battery()
        if "status" in data:
            battery.Status()

    elif "cpu" in data:
        cpu = CPU()
        if "status" in data:
            cpu.Status()

    elif "memory" in data:
        memory = Memory()
        if "usage" in data or "consumption" in data:
            memory.Usage()

    elif "brightness" in data:
        brightness = Brightness()
        if "status" in data or "current" in data:
            current_brightness_level = brightness.Status()
            respond("System brightness currently at {} percent".format(current_brightness_level))

        elif "set" in data:
            data = data.split(" ")
            brightness_toset = data[-2]
            brightness.SetBrightness(brightness_toset)

        elif "increase" in data:
            brightness.Increase()

        elif "decrease" or "lower" in data:
            brightness.Decrease()
    return
