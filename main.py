import tkinter as tk
import time

# =========================
# SETTINGS
# =========================
WORK_TIME = 20 * 60 # 20 min time before a break
SHORT_BREAK = 20    # 20 s short break
LONG_BREAK = 5 * 60  # 5 min long break 


# =========================
# BREAK SCREEN
# =========================

def show_break(duration): #if duration is 3, it show the break screen for 3seconds

	# Tell GNOME not to idle or suspend during the break
    inhibitor = subprocess.Popen([
        "gnome-session-inhibit",
        "--inhibit", "idle:suspend",
        "--reason", "20-20-20 break",
        "--inhibit-only"
    ])
    #Popen means start another program/process
    # inhibitor = subprocess.Popen([ "gnome-session-inhibit", means we are telling python to start gnome-session-inhibit
	
    breakScreen = tk.Tk() #create the actual tkinter window 

    breakScreen.attributes("-fullscreen", True) #make the window full screen 
    breakScreen.attributes("-topmost", True) #keep the window above other windows
    breakScreen.configure(bg="black") # set the background black 

	#create the countdown label 
    label = tk.Label(
        breakScreen,
        text="",
        font=("Arial", 100), #100 here is font size 
        fg="white", # fg = foreground color #foreground in almost every situation means text color 
        bg="black"
    )
    # put the label in the window (or) put the label in the breakScreen
    label.pack(expand=True) #pack() tells tkinter to place the label inside the window 
    #expand = ture tell it to use the available space and center the label. why expand meant centre and what do you mean using available space?
    
	# prevent normal window closing 
    breakScreen.protocol("WM_DELETE_WINDOW", lambda: None)
    #breakScreen.protocol() = communicating with the os's window manager. 
    #("WM_DELETE_WINDOW",...) means when someone tries to close this window, do this instead
    #lambda: None means do nothing 
    #thus,  breakScreen.protocol("WM_DELETE_WINDOW", lambda: None) means if the window manager tries to close the window, don't close it. 
    #but this is not a security lock. So u shouldn't leave the screen just like this in front of others. someone who really wants to bypass the break could still do things such as killing the python process, switching workspaces, etc. 
    # in short, never let it open with others even though the screen is just showing a black screen with a countdown. 
    
	# adding the countdown function 
    def countdown(seconds_left):
        minutes = seconds_left // 60
        seconds = seconds_left % 60

        label.config(text=f"{minutes:02d}:{seconds:02d}")
        # label.config() changes the label and by (text=..) we are changing its text

	#check if the countdown is finished 
        if seconds_left > 0:
            breakScreen.after(1000, countdown, seconds_left - 1) # if there is second left, wait 1 second and call the countdown function again 
            #we don't use time.sleep(1) here coz we are doing this countdown mainly for the displaying to the user. so if we use time.sleep() there is a risk that it can mix up with the timer inside that run the app logic 
        else:
            breakScreen.destroy() #closes the tkinter window 

    countdown(duration) # start countdown 
    breakScreen.mainloop() #tkinter event loop #mainloop() basically says keep this window running and process its events until the window is destroyed


# =========================
# THE MAIN TIMER
# =========================

def timer():

    while True:

        # First 20-minute period
        time.sleep(WORK_TIME) #the program waits 20 minutes coz work time is 20min
        show_break(SHORT_BREAK)

        # Second 20-minute period
        time.sleep(WORK_TIME)
        show_break(SHORT_BREAK)

        # Third 20-minute period
        time.sleep(WORK_TIME)
        show_break(LONG_BREAK)



# =========================
# START
# =========================

if __name__ == "__main__":
    print("20-20-20 timer started.")
    print("Press Ctrl+C in this terminal to stop it.")

    timer()
