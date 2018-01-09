from tkinter import Tk, Toplevel, Frame, Button, Label, Entry, Menu, Canvas
from tkinter.messagebox import showinfo
from decimal import *
import scipy
import numpy
import os

Resistor = Tk()
Resistor.minsize(width = 1000, height = 400)
Resistor.maxsize(width = 1000, height = 400)
Resistor.title('Black Box')

ResistorCanvas = Canvas(Resistor)
ResistorCanvas.place(x = 400, y = 0, width = 400, height = 400)

BlackBox = Canvas(Resistor)
BlackBox.place(x = 0, y = 0, width = 400, height = 400)

minRN = 1#max ResistorNum
maxRN = 0#min ResistorNum
are = False#all resistors are equal

BlackBox_loaded = False
BlackBox_resistance = 0
Battery_power = 0

BatteryWindow = 0
bat_info = 0
bat_input = 0

A = 0

ResistorButtons = Frame(Resistor)
ResistorButtons.place(x = 800, y = 0, width = 400, height = 400)

getanswer = Button(ResistorButtons, text = 'Get answer', fg = 'grey')
getanswer.place(x = 0, y = 360, width = 200, height = 40)

resistance_label = Label(ResistorButtons, text = 'There are no resistors')
resistance_label.place(x = 0, y = 80, width = 200, height = 280)

clamp_num = 0

coord_points_inBB = [[60, 240], [100, 240]]
coord_points = [[10, 200], [390, 200]]
resistors_resistances = []
calculation_info = []

ans_list = []

psave_info = []
rsave_info = ['#']

ResistorNum = 1
PointNum = 0

def closest_item(x, y, coord_points):
    min_distance = -1
    returned = -1
    for i in range (len(coord_points)):
        distance = ((coord_points[i][0] - x) ** 2 + (coord_points[i][1] - y) ** 2) ** (1 / 2)
        if distance < min_distance or returned == -1:
            returned = i
            min_distance = distance
    return returned

def label_rewrite(resistors_resistances):
    global resistance_label
                
    in_text = ''
                
    for i in range (len(resistors_resistances)):
        in_text += 'R' + str(i + 1) + ' = ' + str(resistors_resistances[i]) + ' Ohm.\n'
                
    resistance_label.configure(text = in_text, justify = 'left', anchor = 'nw')

class ammeter():
    xstart = 60
    ystart = 355
    xend = 340
    yend = 355
    
    startpoint = -1
    endpoint = -1  
    
    data = {'x': 0, 'y': 0}
    
    def draw(self):
        ammeter = BlackBox.create_oval(125, 380, 175, 330, width = 3, fill = 'white', tags = 'ammeter')
        ammeter_text = BlackBox.create_text(150, 355, text = 'A', justify = 'center', font = 'Arial 30', tags = 'ammeter')
        BlackBox.tag_bind('ammeter', '<Button-1>', get_from_ammeter)
        
        battery = BlackBox.create_rectangle(245, 330, 255, 380, width = 0, tags = 'battery')
        battery_line1 = BlackBox.create_line(255, 330, 255, 380, width = 3, tags = 'battery')
        battery_line1 = BlackBox.create_line(245, 340, 245, 370, width = 3, tags = 'battery')
        BlackBox.tag_bind('battery', '<Button-1>', input_battery)
        
        horisontal_line1 = BlackBox.create_line(60, 355, 125, 355, width = 3)
        horisontal_line2 = BlackBox.create_line(175, 355, 245, 355, width = 3)
        horisontal_line3 = BlackBox.create_line(255, 355, 340, 355, width = 3)
        
        self.line1 = BlackBox.create_line(self.xstart, self.ystart, 60, 355, width = 3)
        self.line2 = BlackBox.create_line(340, 355, self.xend, self.yend, width = 3)
        self.white_round1 = BlackBox.create_oval(60 + 3, 355 + 3, 60 - 3, 355 - 3, width = 3, fill = 'white')
        self.white_round2 = BlackBox.create_oval(340 + 3, 355 + 3, 340 - 3, 355 - 3, width = 3, fill = 'white')
        self.get1 = BlackBox.create_oval(self.xstart + 3, self.ystart + 3, self.xstart - 3, self.ystart - 3, width = 0, tags = 'get1', fill = 'black')
        self.get2 = BlackBox.create_oval(self.xend + 3, self.yend + 3, self.xend - 3, self.yend - 3, width = 0, tags = 'get2', fill = 'black')      
        
        BlackBox.tag_bind('get1', '<ButtonPress-1>', self.get1_press)
        BlackBox.tag_bind('get1', '<ButtonRelease-1>', self.get1_release)
        BlackBox.tag_bind('get1', '<B1-Motion>', self.get1_motion)
    
        BlackBox.tag_bind('get2', '<ButtonPress-1>', self.get2_press)
        BlackBox.tag_bind('get2', '<ButtonRelease-1>', self.get2_release)
        BlackBox.tag_bind('get2', '<B1-Motion>', self.get2_motion)  
    
    def get1_press(self, event):
        self.data['x'] = event.x
        self.data['y'] = event.y
    
    def get1_release(self, event):
        global coord_points_inBB
        
        closest_point_num = closest_item(self.data['x'], self.data['y'], coord_points_inBB)
        
        self.startpoint = closest_point_num
        
        delta_x = coord_points_inBB[closest_point_num][0] - self.data['x']
        delta_y = coord_points_inBB[closest_point_num][1] - self.data['y']        
        
        self.xstart += delta_x
        self.ystart += delta_y        
        
        BlackBox.delete(self.line1)
        self.line1 = BlackBox.create_line(self.xstart, self.ystart, 60, 355, width = 3)       
        
        self.data['x'] = 0
        self.data['y'] = 0
        
        BlackBox.delete(self.get1)
        self.get1 = BlackBox.create_oval(self.xstart + 3, self.ystart + 3, self.xstart - 3, self.ystart - 3, width = 0, tags = 'get1', fill = 'black')
        
        BlackBox.delete(self.white_round1)
        self.white_round1 = BlackBox.create_oval(60 + 3, 355 + 3, 60 - 3, 355 - 3, width = 3, fill = 'white')
        
    def get1_motion(self, event):
        if event.x > 0 and event.x < 400 and event.y > 0 and event.y < 400:
            delta_x = event.x - self.data['x']
            delta_y = event.y - self.data['y']
        
            self.xstart += delta_x
            self.ystart += delta_y          
            
            BlackBox.move(self.get1, delta_x, delta_y)
        
            BlackBox.delete(self.line1)
            self.line1 = BlackBox.create_line(self.xstart, self.ystart, 60, 355, width = 3)       
      
            BlackBox.delete(self.white_round1)
            self.white_round1 = BlackBox.create_oval(60 + 3, 355 + 3, 60 - 3, 355 - 3, width = 3, fill = 'white')            
        
            self.data['x'] = event.x
            self.data['y'] = event.y  
    
    def get2_press(self, event):
        self.data['x'] = event.x
        self.data['y'] = event.y
    
    def get2_release(self, event):
        global coord_points_inBB
    
        closest_point_num = closest_item(self.data['x'], self.data['y'], coord_points_inBB)
        
        self.endpoint = closest_point_num
        
        delta_x = coord_points_inBB[closest_point_num][0] - self.data['x']
        delta_y = coord_points_inBB[closest_point_num][1] - self.data['y']        
        
        self.xend += delta_x
        self.yend += delta_y       
        
        BlackBox.move(self.get2, delta_x, delta_y)
    
        BlackBox.delete(self.line2)
        self.line2 = BlackBox.create_line(340, 355, self.xend, self.yend, width = 3)        
        
        self.data['x'] = 0
        self.data['y'] = 0
        
        BlackBox.delete(self.get2)
        self.get2 = BlackBox.create_oval(self.xend + 3, self.yend + 3, self.xend - 3, self.yend - 3, width = 0, tags = 'get2', fill = 'black')
        
        BlackBox.delete(self.white_round2)
        self.white_round2 = BlackBox.create_oval(340 + 3, 355 + 3, 340 - 3, 355 - 3, width = 3, fill = 'white')
    
    def get2_motion(self, event):
        if event.x > 0 and event.x < 400 and event.y > 0 and event.y < 400:
            delta_x = event.x - self.data['x']
            delta_y = event.y - self.data['y']
            
            self.xend += delta_x
            self.yend += delta_y          
            
            BlackBox.move(self.get2, delta_x, delta_y)
            
            BlackBox.delete(self.line2)
            self.line2 = BlackBox.create_line(340, 355, self.xend, self.yend, width = 3)       
        
            self.data['x'] = event.x
            self.data['y'] = event.y 
            
            BlackBox.delete(self.white_round2)
            self.white_round2 = BlackBox.create_oval(340 + 3, 355 + 3, 340 - 3, 355 - 3, width = 3, fill = 'white')            

class point:
    num = 0
    xpoint = 10
    ypoint = 10
    
    color = 'black'
    
    data = {'x': 0, 'y': 0}
    
    def load_point(self, ResistorCanvas, Resistor):
        global psave_info
        
        self.point = ResistorCanvas.create_oval(self.xpoint + 4, self.ypoint + 4, self.xpoint - 4, self.ypoint - 4, width = 0, tags = 'point' + str(self.num), fill = self.color)
        self.num_in_Canvas = ResistorCanvas.create_text(self.xpoint + 8, self.ypoint, text = str(self.num + 1), justify = 'left', anchor = 'w')
        
        ResistorCanvas.addtag_withtag('point', 'point' + str(self.num))
        
        ResistorCanvas.tag_bind('point' + str(self.num), '<ButtonPress-1>', self.point_press)
        ResistorCanvas.tag_bind('point' + str(self.num), '<ButtonRelease-1>', self.point_release)
        ResistorCanvas.tag_bind('point' + str(self.num), '<B1-Motion>', self.point_motion)
        
        psave_info.append([self.xpoint, self.ypoint, self.color])
    
    def point_press(self, event):
        self.data['x'] = event.x
        self.data['y'] = event.y
    
    def point_release(self, event):
        global coord_points
        
        coord_points[self.num][0] = self.xpoint
        coord_points[self.num][1] = self.ypoint
        
        self.data['x'] = 0
        self.data['y'] = 0
    
    def point_motion(self, event):
        if event.x > 0 and event.x < 400 and event.y > 0 and event.y < 400:
            delta_x = event.x - self.data['x']
            delta_y = event.y - self.data['y']
            
            self.xpoint += delta_x
            self.ypoint += delta_y
            
            psave_info[self.num][0] = self.xpoint
            psave_info[self.num][1] = self.ypoint
            
            ResistorCanvas.move(self.point, delta_x, delta_y)
            ResistorCanvas.move(self.num_in_Canvas, delta_x, delta_y)
            
            self.data['x'] = event.x
            self.data['y'] = event.y    
    
class resistor:
    num = 1
    xbody = 180
    ybody = 10
    xstart = 0
    ystart = 0
    xend = 0
    yend = 0
    
    startpoint = 0
    endpoint = 1
    
    resistance = 1
    
    data = {'x': 0, 'y': 0}
    
    def load(self, ResistorCanvas, Resistor):
        global coord_points, resistance_label, resistors_resistances, calculation_info, rsave_info
        
        resistors_resistances.append(self.resistance)
        label_rewrite(resistors_resistances)
        
        calculation_info.append([self.startpoint, self.endpoint, self.resistance])
        
        if self.startpoint == 0:
            self.xstart = coord_points[0][0]
            self.ystart = coord_points[0][1]
        if self.endpoint == 1:
            self.xend = coord_points[1][0]
            self.yend = coord_points[1][1]  
        if self.startpoint == 1:
            self.xstart = coord_points[1][0]
            self.ystart = coord_points[1][1]
        if self.endpoint == 0:
            self.xend = coord_points[0][0]
            self.yend = coord_points[0][1]
        
        self.line1 = ResistorCanvas.create_line(self.xstart, self.ystart, self.xbody, self.ybody + 10, width = 3)
        self.line2 = ResistorCanvas.create_line(self.xbody + 40, self.ybody + 10, self.xend, self.yend, width = 3)
        self.get1 = ResistorCanvas.create_oval(self.xstart + 3, self.ystart + 3, self.xstart - 3, self.ystart - 3, width = 0, tags = 'get1' + str(self.num), fill = 'black')
        self.get2 = ResistorCanvas.create_oval(self.xend + 3, self.yend + 3, self.xend - 3, self.yend - 3, width = 0, tags = 'get2' + str(self.num), fill = 'black')
        self.body = ResistorCanvas.create_rectangle(self.xbody, self.ybody, self.xbody + 40, self.ybody + 20, width = 3, fill = 'white', tags = 'resistor' + str(self.num))
        
        self.resistance_text = ResistorCanvas.create_text(self.xbody + 20, self.ybody + 10, text = 'R' + str(self.num), justify = 'center', tags = 'resistor' + str(self.num))
        
        ResistorCanvas.tag_bind('resistor' + str(self.num), '<ButtonPress-1>', self.body_press)
        ResistorCanvas.tag_bind('resistor' + str(self.num), '<ButtonRelease-1>', self.body_release)
        ResistorCanvas.tag_bind('resistor' + str(self.num), '<B1-Motion>', self.body_motion)
        
        ResistorCanvas.tag_bind('resistor' + str(self.num), '<Button-3>', self.new_resistance)
        
        ResistorCanvas.tag_bind('get1' + str(self.num), '<ButtonPress-1>', self.get1_press)
        ResistorCanvas.tag_bind('get1' + str(self.num), '<ButtonRelease-1>', self.get1_release)
        ResistorCanvas.tag_bind('get1' + str(self.num), '<B1-Motion>', self.get1_motion)
        
        ResistorCanvas.tag_bind('get2' + str(self.num), '<ButtonPress-1>', self.get2_press)
        ResistorCanvas.tag_bind('get2' + str(self.num), '<ButtonRelease-1>', self.get2_release)
        ResistorCanvas.tag_bind('get2' + str(self.num), '<B1-Motion>', self.get2_motion)         
   
        rsave_info.append([self.xbody, self.ybody, self.xstart, self.ystart, self.xend, self.yend, self.startpoint, self.endpoint, self.resistance])
    
    def body_press(self, event):
        self.data['x'] = event.x
        self.data['y'] = event.y
    
    def body_release(self, event):
        self.data['x'] = 0
        self.data['y'] = 0
        
        ResistorCanvas.delete(self.get1)
        self.get1 = ResistorCanvas.create_oval(self.xstart + 3, self.ystart + 3, self.xstart - 3, self.ystart - 3, width = 0, tags = 'get1' + str(self.num), fill = 'black')        
        
        ResistorCanvas.delete(self.get2)
        self.get2 = ResistorCanvas.create_oval(self.xend + 3, self.yend + 3, self.xend - 3, self.yend - 3, width = 0, tags = 'get2' + str(self.num), fill = 'black')        
        
        ResistorCanvas.delete(self.body)
        self.body = ResistorCanvas.create_rectangle(self.xbody, self.ybody, self.xbody + 40, self.ybody + 20, width = 3, fill = 'white', tags = 'resistor' + str(self.num))
        
        ResistorCanvas.delete(self.resistance_text)
        self.resistance_text = ResistorCanvas.create_text(self.xbody + 20, self.ybody + 10, text = 'R' + str(self.num), justify = 'center', tags = 'resistor' + str(self.num))

    def body_motion(self, event):
        global rsave_info
        
        if event.x > 0 and event.x < 400 and event.y > 0 and event.y < 400:
            ResistorCanvas.itemconfig(self.body, outline = 'gray', fill = 'gray')
            
            delta_x = event.x - self.data['x']
            delta_y = event.y - self.data['y']
            
            self.xbody += delta_x
            self.ybody += delta_y
            
            rsave_info[self.num][0] = self.xbody
            rsave_info[self.num][1] = self.ybody
            
            ResistorCanvas.move(self.body, delta_x, delta_y)
            ResistorCanvas.move(self.resistance_text, delta_x, delta_y)
            
            ResistorCanvas.delete(self.line1)
            ResistorCanvas.delete(self.line2)
            
            self.line1 = ResistorCanvas.create_line(self.xstart, self.ystart, self.xbody, self.ybody + 10, width = 3)
            self.line2 = ResistorCanvas.create_line(self.xbody + 40, self.ybody + 10, self.xend, self.yend, width = 3)
        
            '''
            Can be this:
            ResistorCanvas.move(self.line1, delta_x, delta_y)
            ResistorCanvas.move(self.line2, delta_x, delta_y)
            '''
        
            self.data['x'] = event.x
            self.data['y'] = event.y
    
    def new_resistance(self, event):
        self.ResistanceWindow = Toplevel(Resistor)
        self.ResistanceWindow.grab_set()
        self.ResistanceWindow.focus_force()
        self.ResistanceWindow.minsize(width = 200, height = 100)
        self.ResistanceWindow.maxsize(width = 200, height = 100)
        self.ResistanceWindow.title('Change resistance')        
        
        self.info = Label(self.ResistanceWindow, text = 'Enter the resistance (in Ohms)\nof the resistor No ' + str(self.num) + ':')
        self.info.place(x = 0, y = 0, width = 200, height = 40)
        
        self.input = Entry(self.ResistanceWindow)
        self.input.place(x = 0, y = 40, width = 200, height = 20)
        
        self.OK_but = Button(self.ResistanceWindow, text = 'OK')
        self.OK_but.place(x = 0, y = 60, width = 100, height = 40)
        self.OK_but.bind('<Button-1>', self.OK_action)
        
        self.Cancel_but = Button(self.ResistanceWindow, text = 'Cancel')
        self.Cancel_but.place(x = 100, y = 60, width = 100, height = 40)
        self.Cancel_but.bind('<Button-1>', self.Cancel_action)
        
        self.ResistanceWindow.mainloop()
    
    def OK_action(self, event):
        global resistance_label, resistors_resistances
        
        resistance = self.input.get()
        
        try:
            resistance_in = float(self.input.get())
        
            if resistance_in <= 0:
                raise ValueError
        
            self.resistance = resistance_in
            
            resistors_resistances[self.num - 1] = self.resistance
            label_rewrite(resistors_resistances)
            
            calculation_info[self.num - 1][2] = self.resistance
            
            rsave_info[self.num][8] = self.resistance
            self.ResistanceWindow.destroy()
        except ValueError:
            self.ResistanceWindow.destroy()
    
    def Cancel_action(self, event):
        self.ResistanceWindow.destroy()
    
    def get1_press(self, event):
        self.data['x'] = event.x
        self.data['y'] = event.y
    
    def get1_release(self, event):
        global coord_points
        
        closest_point_num = closest_item(self.data['x'], self.data['y'], coord_points)
        
        self.startpoint = closest_point_num
        
        rsave_info[self.num][6] = self.startpoint       
        
        calculation_info[self.num - 1][0] = self.startpoint
        
        delta_x = coord_points[closest_point_num][0] - self.data['x']
        delta_y = coord_points[closest_point_num][1] - self.data['y']        
        
        self.xstart += delta_x
        self.ystart += delta_y        
        
        rsave_info[self.num][2] = self.xstart
        rsave_info[self.num][3] = self.ystart
        
        ResistorCanvas.delete(self.line1)
        self.line1 = ResistorCanvas.create_line(self.xstart, self.ystart, self.xbody, self.ybody + 10, width = 3)        
        
        self.data['x'] = 0
        self.data['y'] = 0
        
        ResistorCanvas.delete(self.get1)
        self.get1 = ResistorCanvas.create_oval(self.xstart + 3, self.ystart + 3, self.xstart - 3, self.ystart - 3, width = 0, tags = 'get1' + str(self.num), fill = 'black')
        
        ResistorCanvas.delete(self.body)
        self.body = ResistorCanvas.create_rectangle(self.xbody, self.ybody, self.xbody + 40, self.ybody + 20, width = 3, fill = 'white', tags = 'resistor' + str(self.num))        
        
        ResistorCanvas.delete(self.resistance_text)
        self.resistance_text = ResistorCanvas.create_text(self.xbody + 20, self.ybody + 10, text = 'R' + str(self.num), justify = 'center', tags = 'resistor' + str(self.num))        
        
    def get1_motion(self, event):
        if event.x > 0 and event.x < 400 and event.y > 0 and event.y < 400:
            delta_x = event.x - self.data['x']
            delta_y = event.y - self.data['y']
        
            self.xstart += delta_x
            self.ystart += delta_y
            
            rsave_info[self.num][2] = self.xstart
            rsave_info[self.num][3] = self.ystart           
            
            ResistorCanvas.move(self.get1, delta_x, delta_y)
        
            ResistorCanvas.delete(self.line1)
            self.line1 = ResistorCanvas.create_line(self.xstart, self.ystart, self.xbody, self.ybody + 10, width = 3)       
        
            ResistorCanvas.delete(self.body)
            self.body = ResistorCanvas.create_rectangle(self.xbody, self.ybody, self.xbody + 40, self.ybody + 20, width = 3, fill = 'white', tags = 'resistor' + str(self.num))
            
            ResistorCanvas.delete(self.resistance_text)
            self.resistance_text = ResistorCanvas.create_text(self.xbody + 20, self.ybody + 10, text = 'R' + str(self.num), justify = 'center', tags = 'resistor' + str(self.num))            
        
            self.data['x'] = event.x
            self.data['y'] = event.y  
    
    def get2_press(self, event):
        self.data['x'] = event.x
        self.data['y'] = event.y
    
    def get2_release(self, event):
        global coord_points
    
        closest_point_num = closest_item(self.data['x'], self.data['y'], coord_points)
        
        self.endpoint = closest_point_num
        
        rsave_info[self.num][7] = self.endpoint
        
        calculation_info[self.num - 1][1] = self.endpoint
        
        delta_x = coord_points[closest_point_num][0] - self.data['x']
        delta_y = coord_points[closest_point_num][1] - self.data['y']        
        
        self.xend += delta_x
        self.yend += delta_y
        
        rsave_info[self.num][4] = self.xend
        rsave_info[self.num][5] = self.yend       
        
        ResistorCanvas.move(self.get2, delta_x, delta_y)
    
        ResistorCanvas.delete(self.line2)
        self.line2 = ResistorCanvas.create_line(self.xbody + 40, self.ybody + 10, self.xend, self.yend, width = 3)        
        
        self.data['x'] = 0
        self.data['y'] = 0
        
        ResistorCanvas.delete(self.get2)
        self.get2 = ResistorCanvas.create_oval(self.xend + 3, self.yend + 3, self.xend - 3, self.yend - 3, width = 0, tags = 'get2' + str(self.num), fill = 'black')
        
        ResistorCanvas.delete(self.body)
        self.body = ResistorCanvas.create_rectangle(self.xbody, self.ybody, self.xbody + 40, self.ybody + 20, width = 3, fill = 'white', tags = 'resistor' + str(self.num))        
    
        ResistorCanvas.delete(self.resistance_text)
        self.resistance_text = ResistorCanvas.create_text(self.xbody + 20, self.ybody + 10, text = 'R' + str(self.num), justify = 'center', tags = 'resistor' + str(self.num))    
    
    def get2_motion(self, event):
        if event.x > 0 and event.x < 400 and event.y > 0 and event.y < 400:
            delta_x = event.x - self.data['x']
            delta_y = event.y - self.data['y']
            
            self.xend += delta_x
            self.yend += delta_y
            
            rsave_info[self.num][4] = self.xend
            rsave_info[self.num][5] = self.yend            
            
            ResistorCanvas.move(self.get2, delta_x, delta_y)
            
            ResistorCanvas.delete(self.line2)
            self.line2 = ResistorCanvas.create_line(self.xbody + 40, self.ybody + 10, self.xend, self.yend, width = 3)       
        
            ResistorCanvas.delete(self.body)
            self.body = ResistorCanvas.create_rectangle(self.xbody, self.ybody, self.xbody + 40, self.ybody + 20, width = 3, fill = 'white', tags = 'resistor' + str(self.num))               
        
            ResistorCanvas.delete(self.resistance_text)
            self.resistance_text = ResistorCanvas.create_text(self.xbody + 20, self.ybody + 10, text = 'R' + str(self.num), justify = 'center', tags = 'resistor' + str(self.num))        
        
            self.data['x'] = event.x
            self.data['y'] = event.y    

'''
Need to write:
Example = resistor()
Example.num = examplenum
Example.load(ResistorCanvas)
'''

def CreateResistor(event):
    global ResistorCanvas, ResistorNum, Resistor
    new_one = resistor()
    new_one.num = ResistorNum
    ResistorNum += 1
    new_one.load(ResistorCanvas, Resistor)

def CreatePoint(event):
    global ResistorCanvas, PointNum, Resistor, coord_points
    new_one = point()
    new_one.num = PointNum
    PointNum += 1
    coord_points.append([10, 10])
    new_one.load_point(ResistorCanvas, Resistor)

def CreatePoint_1():
    global ResistorCanvas, PointNum, Resistor, coord_points
    new_one = point()
    new_one.num = PointNum
    new_one.color = 'red'
    new_one.xpoint = 10
    new_one.ypoint = 200
    PointNum += 1
    new_one.load_point(ResistorCanvas, Resistor)

def CreatePoint_2():
    global ResistorCanvas, PointNum, Resistor, coord_points
    new_one = point()
    new_one.num = PointNum
    new_one.color = 'red'
    new_one.xpoint = 380
    new_one.ypoint = 200
    PointNum += 1
    new_one.load_point(ResistorCanvas, Resistor)

def CreatePoint_3():
    global ResistorCanvas, PointNum, Resistor, coord_points
    new_one = point()
    new_one.num = PointNum
    new_one.color = 'red'
    new_one.xpoint = 195
    new_one.ypoint = 10
    PointNum += 1
    new_one.load_point(ResistorCanvas, Resistor)

def CreatePoint_4():
    global ResistorCanvas, PointNum, Resistor, coord_points
    new_one = point()
    new_one.num = PointNum
    new_one.color = 'red'
    new_one.xpoint = 195
    new_one.ypoint = 390
    PointNum += 1
    new_one.load_point(ResistorCanvas, Resistor)

def CreatePoint_5():
    global ResistorCanvas, PointNum, Resistor, coord_points
    new_one = point()
    new_one.num = PointNum
    new_one.color = 'red'
    new_one.xpoint = 10
    new_one.ypoint = 10
    PointNum += 1
    new_one.load_point(ResistorCanvas, Resistor)

def CreatePoint_6():
    global ResistorCanvas, PointNum, Resistor, coord_points
    new_one = point()
    new_one.num = PointNum
    new_one.color = 'red'
    new_one.xpoint = 10
    new_one.ypoint = 390
    PointNum += 1
    new_one.load_point(ResistorCanvas, Resistor)

def CreatePoint_7():
    global ResistorCanvas, PointNum, Resistor, coord_points
    new_one = point()
    new_one.num = PointNum
    new_one.color = 'red'
    new_one.xpoint = 380
    new_one.ypoint = 10
    PointNum += 1
    new_one.load_point(ResistorCanvas, Resistor)

def CreatePoint_8():
    global ResistorCanvas, PointNum, Resistor, coord_points
    new_one = point()
    new_one.num = PointNum
    new_one.color = 'red'
    new_one.xpoint = 380
    new_one.ypoint = 390
    PointNum += 1
    new_one.load_point(ResistorCanvas, Resistor)

def calculation(calculation_info, ResistorNum, PointNum, s, f):
    N = PointNum
    M = ResistorNum - 1
    matrix = [[0 for i in range (N + M - 2)] for j in range (N + M - 2)]
    vector = [[0] for i in range (N + M - 2)]
    currents = []
    EMF = 1
    for i in range (M):
        S = calculation_info[i][0]
        T = calculation_info[i][1]
        R = calculation_info[i][2]
        if S == s:
            S = 0
        elif S < s:
            S += 1
        if T == s:
            T = 0
        elif T < s:
            T += 1
        if S == f:
            S = N - 1
        elif S > f:
            S -= 1
        if T == f:
            T = N - 1
        elif T > f:
            T -= 1        
        if S == 0:
            vector[i][0] += EMF
            currents.append(i) 
        elif S != N - 1:
            matrix[i][M + S - 1] -= 1
            matrix[M + S - 1][i] -= 1
        if T == 0:
            vector[i][0] -= EMF
            currents.append(i)
        elif T != N - 1:
            matrix[i][M + T - 1] += 1
            matrix[M + T - 1][i] += 1
        matrix[i][i] += R
    matrix = scipy.array(matrix)
    vector = scipy.array(vector)
    ans = numpy.linalg.solve(matrix, vector).tolist()
    currentsum = 0
    for current in currents:
        currentsum += abs(ans[current][0])
    ansR = EMF / currentsum
    return ansR

def GetAnswer(event):
    global calculation_info, ResistorNum, PointNum, BlackBox_resistance, minRN, maxRN, are, resistors_resistances, ans_list;
    
    AnswerWindow = Toplevel(Resistor)
    AnswerWindow.grab_set()
    AnswerWindow.focus_force()
    AnswerWindow.minsize(width = 200, height = 40)
    AnswerWindow.maxsize(width = 200, height = 40)
    AnswerWindow.title('Answer')        
    
    if are:
        f = True
        if resistors_resistances != [resistors_resistances[0] for i in range (ResistorNum - 1)]:
            f = False
    else:
        f = True
    
    try_list = []
    for i in range (0, clamp_num):
        try_list.append([])
        for j in range (i + 1, clamp_num):
            try_list[i].append(calculation(calculation_info, ResistorNum, PointNum, i, j))    
    if try_list == ans_list and f and ResistorNum - 1 >= minRN and (ResistorNum - 1 <= maxRN or maxRN == 0):
        answer = Label(AnswerWindow, text = 'Correct')
    else:
        answer = Label(AnswerWindow, text = 'Incorrect')
    answer.place(x = 0, y = 0, width = 200, height = 40) 

def Help():
    showinfo('Help', 'Press button "Create resistor" to create resistors.\nPress button "Create point" to create connecting points.\nPress left mouse button to move resistors and connecting points.\nPress right mouse button to change resistance of resistor.\nPress button "Get answer" to get total resistans of the circuit.\n\nIn "File" menu:\nPress "Save" to save your circuit.\nPress "Load" to load your old circuit.\nPress "Clear" to delete all elements in your circuit.')

def About():
    showinfo('About', 'Product: Black Box\n\nVersion: 0.6.1\n\nRelease date: 03.01.2018\n\nDevelopers:\nIgor Korkin\nkorkin170202@gmail.com\nArseniy Nestyuk\narseniy.nestyuk@gmail.com')

def Load():
    global rsave_info, psave_info, ResistorNum, PointNum, ResistorCanvas, Resistor, BlackBox_loaded, BlackBox_resistance, getanswer, minRN, maxRN, are, clamp_num, ans_list
    try:
        Clear()
        
        file_to_load = open('Save.txt', 'r')
        clamp_num = int(file_to_load.readline())
        PointNum = int(file_to_load.readline())
        for i in range(PointNum):
            line = list(map(str, file_to_load.readline().split()))
            for j in range(2):
                line[j] = int(line[j])
            new_one = point()
            new_one.num = i
            new_one.xpoint = line[0]
            new_one.ypoint = line[1]
            new_one.color = line[2]
            
            coord_points.append([new_one.xpoint, new_one.ypoint])
        
            new_one.load_point(ResistorCanvas, Resistor)
        ResistorNum = int(file_to_load.readline()) + 1
        for i in range (1, ResistorNum):
            line = list(map(float, file_to_load.readline().split()))
        
            for j in range(8):
                line[j] = int(line[j])
        
            new_one = resistor()
            new_one.num = i
            new_one.xbody = line[0]
            new_one.ybody = line[1]
            new_one.xstart = line[2]
            new_one.ystart = line[3]
            new_one.xend = line[4]
            new_one.yend = line[5]
            new_one.startpoint = line[6]
            new_one.endpoint = line[7]
            new_one.resistance = line[8]
        
            new_one.load(ResistorCanvas, Resistor)
        
        condition_number = int(file_to_load.readline())
        for i in range (condition_number):
            line = file_to_load.readline().split()
            if line[0] == 'are':
                are = True
            elif line[0] == 'minRN':
                minRN = int(line[1])
            elif line[0] == 'maxRN':
                maxRN = int(line[1])
        
        BlackBox_loaded = True
        for i in range (0, clamp_num):
            ans_list.append([])
            for j in range (i + 1, clamp_num):
                ans_list[i].append(calculation(calculation_info, ResistorNum, PointNum, i, j))
        
        getanswer.configure(fg = 'black')
        getanswer.bind('<Button-1>', GetAnswer)
        
        New_canvas()
    except:
        New_canvas()

def Clear():
    global rsave_info, psave_info, ResistorNum, PointNum, ResistorCanvas, coord_points, resistors_resistances, calculation_info
    ResistorCanvas.delete('all')
    
    coord_points = []
    resistors_resistances = []
    calculation_info = []
    
    psave_info = []
    rsave_info = ['#']
    
    ResistorNum = 1
    PointNum = 0    
    
    resistance_label.configure(text = 'There are no resistors', justify = 'center', anchor = 'center')

def New_canvas():
    global coord_points, classmethod
    
    Clear()
    
    coord_points = [[10, 200], [390, 200]]
    
    if clamp_num == 2:
        two_clamps()
    if clamp_num == 3:
        three_clamps()
    if clamp_num == 4:
        four_clamps()
    if clamp_num == 5:
        five_clamps()
    if clamp_num == 6:
        six_clamps()
    if clamp_num == 7:
        seven_clamps()
    if clamp_num == 8:
        eight_clamps()    

def get_from_ammeter(event):
    global Resistor, BlackBox_loaded, BlackBox_resistance, A, ans_list
    
    AmmeterWindow = Toplevel(Resistor)
    AmmeterWindow.grab_set()
    AmmeterWindow.focus_force()
    AmmeterWindow.minsize(width = 200, height = 40)
    AmmeterWindow.maxsize(width = 200, height = 40)
    AmmeterWindow.title('Current strength')
    
    Ammeterlabel = Label(AmmeterWindow)
    Ammeterlabel.place(x = 0, y = 0, width = 200, height = 40)
    
    if not BlackBox_loaded:
        Ammeterlabel.configure(text = 'There are no circuit')
    elif Battery_power == 0:
        Ammeterlabel.configure(text = 'There are no battery')
    elif A.startpoint == -1 or A.endpoint == -1:
        Ammeterlabel.configure(text = 'The circuit is not connected')
    elif A.startpoint == A.endpoint:
        Ammeterlabel.configure(text = 'The ammeter does not work.\nThis is strange.')
    else:
        Ammeterlabel.configure(text = 'Current strenth is\n' + str(Battery_power / ans_list[min(A.startpoint, A.endpoint)][max(A.startpoint, A.endpoint) - min(A.startpoint, A.endpoint) - 1]) + ' amps.')
    
def input_battery(event):
    global Resistor, Battery_power, BatteryWindow, bat_info, bat_input
    
    BatteryWindow = Toplevel(Resistor)
    BatteryWindow.grab_set()
    BatteryWindow.focus_force()
    BatteryWindow.minsize(width = 200, height = 100)
    BatteryWindow.maxsize(width = 200, height = 100)
    BatteryWindow.title('Change resistance')        

    bat_info = Label(BatteryWindow, text = 'Enter the EMF\nof the battery (in Volts):')
    bat_info.place(x = 0, y = 0, width = 200, height = 40)

    bat_input = Entry(BatteryWindow)
    bat_input.place(x = 0, y = 40, width = 200, height = 20)

    bat_OK_but = Button(BatteryWindow, text = 'OK')
    bat_OK_but.place(x = 0, y = 60, width = 100, height = 40)
    bat_OK_but.bind('<Button-1>', bat_OK_action)

    bat_Cancel_but = Button(BatteryWindow, text = 'Cancel')
    bat_Cancel_but.place(x = 100, y = 60, width = 100, height = 40)
    bat_Cancel_but.bind('<Button-1>', bat_Cancel_action)

def bat_OK_action(event):
    global Battery_power, BatteryWindow, bat_info, bat_input      

    try:
        resistance_in = float(bat_input.get())
        
        if resistance_in <= 0:
            raise ValueError
        
        Battery_power = resistance_in
        
        BatteryWindow.destroy()
    except ValueError:
        BatteryWindow.destroy()

def bat_Cancel_action(event):
    global BatteryWindow
    BatteryWindow.destroy()
    
def create_BlackBox():
    global BlackBox, clamp_num ,coord_points_inBB, A
    
    box = BlackBox.create_rectangle(20, 20, 380, 200, width = 0, fill = 'black')
    box_text = BlackBox.create_text(200, 110, text = 'Black\nBox', justify = 'center', fill = 'white', font = 'Arial 30')
    
    BBline = BlackBox.create_line(60, 200, 60, 240, width = 3)
    BBpoint = BlackBox.create_oval(60 + 4, 240 + 4, 60 - 4, 240 - 4, width = 0, fill = 'red')
    BBline = BlackBox.create_line(100, 200, 100, 240, width = 3)
    BBpoint = BlackBox.create_oval(100 + 4, 240 + 4, 100 - 4, 240 - 4, width = 0, fill = 'red')    
    if clamp_num > 2:
        BBline = BlackBox.create_line(140, 200, 140, 240, width = 3)
        BBpoint = BlackBox.create_oval(140 + 4, 240 + 4, 140 - 4, 240 - 4, width = 0, fill = 'red')
        coord_points_inBB.append([140, 240]) 
    else:
        BBline = BlackBox.create_line(140, 200, 140, 240, width = 3, fill = 'grey')
        BBpoint = BlackBox.create_oval(140 + 4, 240 + 4, 140 - 4, 240 - 4, width = 0, fill = 'grey')        
    if clamp_num > 3:
        BBline = BlackBox.create_line(180, 200, 180, 240, width = 3)
        BBpoint = BlackBox.create_oval(180 + 4, 240 + 4, 180 - 4, 240 - 4, width = 0, fill = 'red')
        coord_points_inBB.append([180, 240])
    else:
        BBline = BlackBox.create_line(180, 200, 180, 240, width = 3, fill = 'grey')
        BBpoint = BlackBox.create_oval(180 + 4, 240 + 4, 180 - 4, 240 - 4, width = 0, fill = 'grey')         
    if clamp_num > 4:
        BBline = BlackBox.create_line(220, 200, 220, 240, width = 3)
        BBpoint = BlackBox.create_oval(220 + 4, 240 + 4, 220 - 4, 240 - 4, width = 0, fill = 'red')
        coord_points_inBB.append([220, 240])
    else:
        BBline = BlackBox.create_line(220, 200, 220, 240, width = 3, fill = 'grey')
        BBpoint = BlackBox.create_oval(220 + 4, 240 + 4, 220 - 4, 240 - 4, width = 0, fill = 'grey')        
    if clamp_num > 5:
        BBline = BlackBox.create_line(260, 200, 260, 240, width = 3)
        BBpoint = BlackBox.create_oval(260 + 4, 240 + 4, 260 - 4, 240 - 4, width = 0, fill = 'red')
        coord_points_inBB.append([260, 240])
    else:
        BBline = BlackBox.create_line(260, 200, 260, 240, width = 3, fill = 'grey')
        BBpoint = BlackBox.create_oval(260 + 4, 240 + 4, 260 - 4, 240 - 4, width = 0, fill = 'grey')         
    if clamp_num > 6:
        BBline = BlackBox.create_line(300, 200, 300, 240, width = 3)
        BBpoint = BlackBox.create_oval(300 + 4, 240 + 4, 300 - 4, 240 - 4, width = 0, fill = 'red')
        coord_points_inBB.append([300, 240])
    else:
        BBline = BlackBox.create_line(300, 200, 300, 240, width = 3, fill = 'grey')
        BBpoint = BlackBox.create_oval(300 + 4, 240 + 4, 300 - 4, 240 - 4, width = 0, fill = 'grey')        
    if clamp_num > 7:
        BBline = BlackBox.create_line(340, 200, 340, 240, width = 3)
        BBpoint = BlackBox.create_oval(340 + 4, 240 + 4, 340 - 4, 240 - 4, width = 0, fill = 'red')
        coord_points_inBB.append([340, 240])
    else:
        BBline = BlackBox.create_line(340, 200, 340, 240, width = 3, fill = 'grey')
        BBpoint = BlackBox.create_oval(340 + 4, 240 + 4, 340 - 4, 240 - 4, width = 0, fill = 'grey')
        
    '''
    box_line1 = BlackBox.create_line(20, 150, 100, 150, width = 3)
    box_line2 = BlackBox.create_line(380, 150, 300, 150, width = 3)
    
    s_ammeter_point = BlackBox.create_oval(60 + 4, 150 + 4, 60 - 4, 150 - 4, width = 0, fill = 'black')
    s_ammeter_point = BlackBox.create_oval(340 + 4, 150 + 4, 340 - 4, 150 - 4, width = 0, fill = 'black')
    ammeter_vertical_line1 = BlackBox.create_line(60, 150, 60, 325, width = 3)
    ammeter_vertical_line2 = BlackBox.create_line(340, 150, 340, 325, width = 3)
    
    ammeter = BlackBox.create_oval(125, 350, 175, 300, width = 3, fill = 'white', tags = 'ammeter')
    ammeter_text = BlackBox.create_text(150, 325, text = 'A', justify = 'center', font = 'Arial 30', tags = 'ammeter')
    BlackBox.tag_bind('ammeter', '<Button-1>', get_from_ammeter)
    
    battery = BlackBox.create_rectangle(245, 300, 255, 350, width = 0, tags = 'battery')
    battery_line1 = BlackBox.create_line(255, 300, 255, 350, width = 3, tags = 'battery')
    battery_line1 = BlackBox.create_line(245, 310, 245, 340, width = 3, tags = 'battery')
    BlackBox.tag_bind('battery', '<Button-1>', input_battery)
    
    horisontal_line1 = BlackBox.create_line(60 - 1.5, 325, 125, 325, width = 3)
    horisontal_line2 = BlackBox.create_line(175, 325, 245, 325, width = 3)
    horisontal_line3 = BlackBox.create_line(255, 325, 340 + 1.5, 325, width = 3)
    
    s_point = BlackBox.create_oval(20 + 4, 150 + 4, 20 - 4, 150 - 4, width = 0, fill = 'red')
    f_point = BlackBox.create_oval(380 + 4, 150 + 4, 380 - 4, 150 - 4, width = 0, fill = 'blue')
    '''
    
    A = ammeter()
    A.draw()

def two_clamps():
    global coord_points, clamp_num
    
    Clear()
    
    clamp_num = 2
    coord_points = [[10, 200], [380, 200]]
    
    CreatePoint_1()
    CreatePoint_2()  

def three_clamps():
    global coord_points, clamp_num
    
    Clear()
    
    clamp_num = 3
    coord_points = [[10, 200], [380, 200], [195, 10]]
    
    CreatePoint_1()
    CreatePoint_2()
    CreatePoint_3()     

def four_clamps():
    global coord_points, clamp_num
    
    Clear()
    
    clamp_num = 4
    coord_points = [[10, 200], [380, 200], [195, 10], [195, 390]]
    
    CreatePoint_1()
    CreatePoint_2()
    CreatePoint_3()
    CreatePoint_4()      
    
def five_clamps():
    global coord_points, clamp_num
    
    Clear()
    
    clamp_num = 5
    coord_points = [[10, 200], [380, 200], [195, 10], [195, 390], [10, 10]]
    
    CreatePoint_1()
    CreatePoint_2()
    CreatePoint_3()
    CreatePoint_4()
    CreatePoint_5()     
    
def six_clamps():
    global coord_points, clamp_num
    
    Clear()
    
    clamp_num = 6
    coord_points = [[10, 200], [380, 200], [195, 10], [195, 390], [10, 10], [10, 390]]
    
    CreatePoint_1()
    CreatePoint_2()
    CreatePoint_3()
    CreatePoint_4()
    CreatePoint_5()
    CreatePoint_6()      
    
def seven_clamps():
    global coord_points, clamp_num
    
    Clear()
    
    clamp_num = 7
    coord_points = [[10, 200], [380, 200], [195, 10], [195, 390], [10, 10], [10, 390], [380, 10]]
    
    CreatePoint_1()
    CreatePoint_2()
    CreatePoint_3()
    CreatePoint_4()
    CreatePoint_5()
    CreatePoint_6()
    CreatePoint_7()      
    
def eight_clamps():
    global coord_points, clamp_num
    
    Clear()
    
    clamp_num = 8
    coord_points = [[10, 200], [380, 200], [195, 10], [195, 390], [10, 10], [10, 390], [380, 10], [380, 390]]
    
    CreatePoint_1()
    CreatePoint_2()
    CreatePoint_3()
    CreatePoint_4()
    CreatePoint_5()
    CreatePoint_6()
    CreatePoint_7()
    CreatePoint_8()

Load() 

createresistor = Button(ResistorButtons, text = 'Create resistor')
createresistor.bind('<Button-1>', CreateResistor)
createresistor.place(x = 0, y = 0, width = 200, height = 40)

createpoint = Button(ResistorButtons, text = 'Create point')
createpoint.bind('<Button-1>', CreatePoint)
createpoint.place(x = 0, y = 40, width = 200, height = 40)

menu = Menu(Resistor)
Resistor.config(menu = menu)

file_menu = Menu(menu)
menu.add_cascade(label = 'File', menu = file_menu)
file_menu.add_command(label = 'Clear', command = New_canvas)

help_menu = Menu(menu)
menu.add_cascade(label = 'Help', menu = help_menu)
help_menu.add_command(label = 'Help', command = Help)
help_menu.add_command(label = 'About', command = About)     

create_BlackBox()

Resistor.mainloop()