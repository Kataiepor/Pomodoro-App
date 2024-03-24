import tkinter as tk
from tkinter import messagebox
from ttkbootstrap import ttk, Style

WORK_TIME = 25*60
SHORT_BREAK_TIME = 5*60
LONG_BREAK_TIME = 15*60

class PomodoroTimer: 
    def __init__(self) -> None:  
        self.root = tk.Tk()
        self.root.geometry("500x350")
        self.root.title("Pomodoro Timer")
        self.style = Style()
        self.current_theme = "light"
        
        self.timer_label = tk.Label(self.root, text="", font=("TKDefaultFont", 40))
        self.timer_label.pack(pady=20)
        
        self.start_button = ttk.Button(self.root, text="Start", command=self.start_timer, style="start.TButton")
        self.start_button.pack(pady=5)
        
        self.stop_button = ttk.Button(self.root, text="Stop", command=self.stop_timer, state=tk.DISABLED, style="stop.TButton")
        self.stop_button.pack(pady=5)
        
        self.work_time, self.break_time = WORK_TIME, SHORT_BREAK_TIME
        self.is_work_time, self.pomodoros_completed, self.is_running = True, 0, False
        
        self.moon_img = tk.PhotoImage(file="moon.png").subsample(8) 
        self.sun_img = tk.PhotoImage(file="sun.png").subsample(8)  
        self.theme_button = tk.Button(self.root, image=self.moon_img, bd=0, command=self.toggle_theme)
        self.theme_button.pack(side="top", pady=10) 
        
        self.update_theme()  
        
        self.root.mainloop()
        
    def start_timer(self):
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.is_running = True
        self.update_timer()
    
    def stop_timer(self):
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.is_running = False
        
    def update_timer(self):
        if self.is_running: 
            if self.is_work_time:
                self.work_time -= 1
                if self.work_time == 0:
                    self.is_work_time = False
                    self.pomodoros_completed += 1
                    self.break_time = LONG_BREAK_TIME if self.pomodoros_completed % 4 == 0 else SHORT_BREAK_TIME
                    message = "Great Job! Take a long break and rest your mind." if self.pomodoros_completed % 4 == 0 else "Good Job! Take a short break and stretch your legs!"
                    messagebox.showinfo("Pomodoro Completed", message)
            else:
                self.break_time -= 1
                if self.break_time == 0:
                    self.is_work_time = True
                    self.work_time = WORK_TIME
                    messagebox.showinfo("Work Time", "Get back to work!")
            minutes, seconds = divmod(self.work_time if self.is_work_time else self.break_time, 60)
            self.timer_label.config(text="{:02d}:{:02d}".format(minutes, seconds))
            self.root.after(1000, self.update_timer)
    
    def toggle_theme(self):
        if self.current_theme == "light":
            self.current_theme = "dark"
            self.theme_button.config(image=self.sun_img)  
            self.start_button.config(style="dark.TButton")  
            self.stop_button.config(style="dark.TButton") 
        else:
            self.current_theme = "light"
            self.theme_button.config(image=self.moon_img) 
            self.start_button.config(style="green.TButton") 
            self.stop_button.config(style="green.TButton")   
        self.update_theme()
        
    def update_theme(self):
        if self.current_theme == "light":
            self.style.theme_use("flatly")  
        else:
            self.style.theme_use("darkly")  

PomodoroTimer()

input("Press enter to close program")