#tooltip.py
#C:\Program Files\Python\Python38\Lib\site-packages\tooltip.py
#code from Python GUI Python GUI Programming Cookbook 2nd - 2017
import tkinter as tk
 
class ToolTip(object):
    def __init__(self,widget):
        self.widget = widget
        self.tip_window = None
 
    def show_tip(self,tip_text):
        "Display text in a tooltip window"
        if self.tip_window or not tip_text:
            return
        x, y, _cx, cy = self.widget.bbox("insert")      
        # get size of widget
        x = x + self.widget.winfo_rootx() + 25          
        # calculate to display tooptip
        y = y + cy + self.widget.winfo_rooty() + 25     
        # below and to the right
        self.tip_window = tw = tk.Toplevel(self.widget) 
        # create new tooltip window
        tw.wm_overrideredirect(True)                    
        # remove all Window Manager (wm)
        tw.wm_geometry("+%d+%d" %(x, y))                
        # create window size
 
        label = tk.Label(tw, text=tip_text, justify=tk.LEFT,
                         background="#ffffe0", relief=tk.SOLID,
                         borderwidth=1,font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)
 
    def hide_tip(self):
        tw = self.tip_window
        self.tip_window = None
        if tw:
            tw.destroy()
 
def create_ToolTip(widget, text):
    tooltip = ToolTip(widget)
    def enter(event):
        tooltip.show_tip(text)
    def leave(event):
        tooltip.hide_tip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)