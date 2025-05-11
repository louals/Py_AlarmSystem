from tkinter import *
from SevenSeg import SevenSeg
from gpiozero import LED as LEDZ
from gpiozero import Button as ButtonZ
from time import sleep
from signal import pause
import requests

class AlarmSys:

    def __init__(self, root):
        self.tk = root
        self.tk.title("Securite GUI")

        self.afficheur = SevenSeg(12,9,10,11,16,13,17,False)
        self.alaramLed = LEDZ(4)
        self.btn = ButtonZ(27)
        self.btn_reset = ButtonZ(24)

        self.zone1 = ButtonZ(22) 
        self.zone2 = ButtonZ(5)
        self.zone3 = ButtonZ(6)
        self.zone4 = ButtonZ(19)

        self.systemStatus = 0
        self.alarm_status = 2

        self.btn.when_pressed = self.update_system_status
        self.zone1.when_pressed = self.check_zone1
        self.zone2.when_pressed = self.check_zone2
        self.zone3.when_pressed = self.check_zone3
        self.zone4.when_pressed = self.check_zone4
        self.btn_reset.when_pressed = self.reset_alarm

        left_panel = Frame(self.tk, padx=10, pady=10, borderwidth=2)
        left_panel.grid(row=0, column=0, padx=5, pady=5)

        self.z1 = Label(left_panel, text="Z1", width=6, bg="darkblue", fg="white")
        self.z1.grid(row=0, column=0, padx=5, pady=5)
        self.z2 = Label(left_panel, text="Z2", width=6, bg="darkblue", fg="white")
        self.z2.grid(row=0, column=1, padx=5, pady=5)
        self.z3 = Label(left_panel, text="Z3", width=6, bg="darkblue", fg="white")
        self.z3.grid(row=1, column=0, padx=5, pady=5)
        self.z4 = Label(left_panel, text="Z4", width=6, bg="darkblue", fg="white")
        self.z4.grid(row=1, column=1, padx=5, pady=5)

        self.on_off = Label(left_panel, text="ON/OFF", width=14, bg="darkblue", fg="white")
        self.on_off.grid(row=2, column=0, columnspan=2, pady=5)

        right_panel = Frame(self.tk, padx=10, pady=10, borderwidth=2)
        right_panel.grid(row=0, column=1, padx=5, pady=5)

        self.activate_btn = Button(right_panel, text="Activate", width=10, bg="salmon", command=self.activate_alarm)
        self.activate_btn.grid(row=0, column=0, pady=5)

        self.deactivate_btn = Button(right_panel, text="Deactivate", width=10, bg="salmon", command=self.deactivate_alarm)
        self.deactivate_btn.grid(row=1, column=0, pady=5)

        self.reset_btn = Button(right_panel, text="Reset", width=10, bg="salmon", command=self.reset_alarm)
        self.reset_btn.grid(row=2, column=0, pady=5)

        self.update_flask_status()

        self.tk.mainloop()

    def update_flask_status(self):
        self.get_status_from_flask()
        self.tk.after(1000, self.update_flask_status)

    def get_status_from_flask(self):
        
        flask_url = 'http://192.168.2.18:5000/status'
        response = requests.get(flask_url)
        
        if response.status_code == 200:
           
            status_data = response.text
            
           
            stat = status_data.split(',')
            
            if len(stat) == 6:
                
                self.zone1_status = int(stat[0])
                self.zone2_status = int(stat[1])
                self.zone3_status = int(stat[2])
                self.zone4_status = int(stat[3])
                self.systemStatus = int(stat[4])
                self.alarm_status = int(stat[5])
                
                
                self.update_zone_color(self.zone1_status, self.z1)
                self.update_zone_color(self.zone2_status, self.z2)
                self.update_zone_color(self.zone3_status, self.z3)
                self.update_zone_color(self.zone4_status, self.z4)

    def update_zone_color(self, zone_status, zone_label):
        if zone_status == 1:
            zone_label.config(bg="red")
        else:
            zone_label.config(bg="darkblue")
    
    
    def update_system_status(self):
        if self.systemStatus == 1:
            self.deactivate_alarm()
        else:
            self.activate_alarm()

    def check_zone1(self):
        if self.systemStatus == 1:
            self.afficheur.show1()
            self.zone1_status = 1
            self.z1.config(bg="red")
            self.alaramLed.blink()
            self.alarm_status = 1
            self.send_data_to_flask()

    def check_zone2(self):
        if self.systemStatus == 1:
            self.afficheur.show2()
            self.zone2_status = 1
            self.z2.config(bg="red")
            self.alaramLed.blink()
            self.alarm_status = 1
            self.send_data_to_flask()

    def check_zone3(self):
        if self.systemStatus == 1:
            self.afficheur.show3()
            self.zone3_status = 1
            self.z3.config(bg="red")
            self.alaramLed.blink()
            self.alarm_status = 1
            self.send_data_to_flask()

    def check_zone4(self):
        if self.systemStatus == 1:
            self.afficheur.show4()
            self.zone4_status = 1
            self.z4.config(bg="red")
            self.alaramLed.blink()
            self.alarm_status = 1
            self.send_data_to_flask()

    def activate_alarm(self):
        if self.systemStatus == 0:
            self.afficheur.cout_up()
            self.systemStatus = 1
            self.alaramLed.on()
            self.alarm_status = 0
            self.on_off.config(text="ON", bg="green", fg="white")
            self.send_data_to_flask()

    def deactivate_alarm(self):
        if self.systemStatus == 1:
            self.afficheur.cout_down()
            self.systemStatus = 0
            self.alaramLed.off()
            self.alarm_status = 2
            self.reset_zone_colors()
            self.on_off.config(text="OFF", bg="red", fg="white")
            self.send_data_to_flask()

    def reset_alarm(self):
        if self.systemStatus == 1:
            self.alaramLed.on()
            self.alarm_status = 0
            self.send_data_to_flask()

    def reset_zone_colors(self):
        self.z1.config(bg="darkblue")
        self.z2.config(bg="darkblue")
        self.z3.config(bg="darkblue")
        self.z4.config(bg="darkblue")

    def send_data_to_flask(self):
        
            userdata = {
                'zone1': self.zone1_status,
                'zone2': self.zone2_status,
                'zone3': self.zone3_status,
                'zone4': self.zone4_status,
                'system_status': self.systemStatus,
                'alarm_status': self.alarm_status
            }

            flask_url = "http://192.168.2.18:5000/update"
            try:
                response = requests.post(flask_url, params=userdata)
                print("Data sent:", userdata)
                print("Response status:", response.status_code)
            except requests.exceptions.RequestException as e:
                print(f"Error sending data to Flask: {e}")

app = AlarmSys(Tk())

