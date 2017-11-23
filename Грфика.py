from tkinter import Tk, Toplevel, Frame, Button, Label, Entry, StringVar, Canvas
Resistor = Tk()
Resistor.minsize(width = 600, height = 400)
Resistor.maxsize(width = 600, height = 400)
Resistor.title('Resistor')

ResistorCanvas = Canvas(Resistor)
ResistorCanvas.place(x = 0, y = 0, width = 400, height = 400)

class resistor:
    num = 1
    xbody = 23
    ybody = 3
    xstart = xbody - 20
    ystart = ybody + 10
    xend = xbody + 60
    yend = ybody + 10
    
    resistance = 1
    
    data = {'x': 0, 'y': 0}
    
    def load(self, ResistorCanvas):
        self.line1 = ResistorCanvas.create_line(self.xstart, self.ystart, self.xbody, self.ybody + 10, width = 3)
        self.line2 = ResistorCanvas.create_line(self.xbody + 40, self.ybody + 10, self.xend, self.yend, width = 3)
        self.get1 = ResistorCanvas.create_oval(self.xstart + 3, self.ystart + 3, self.xstart - 3, self.ystart - 3, width = 0, tags = 'get1' + str(self.num), fill = 'black')
        self.get2 = ResistorCanvas.create_oval(self.xend + 3, self.yend + 3, self.xend - 3, self.yend - 3, width = 0, tags = 'get2' + str(self.num), fill = 'black')
        self.body = ResistorCanvas.create_rectangle(self.xbody, self.ybody, self.xbody + 40, self.ybody + 20, width = 3, fill = 'white', tags = 'resistor' + str(self.num))
        
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

    def body_motion(self, event):
        ResistorCanvas.itemconfig(self.body, outline = 'gray', fill = 'gray')
        
        delta_x = event.x - self.data['x']
        delta_y = event.y - self.data['y']
        
        self.xbody += delta_x
        self.ybody += delta_y
        
        ResistorCanvas.move(self.body, delta_x, delta_y)
        
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
        global Resistor
        
        self.ResistanceWindow = Toplevel(Resistor)
        self.ResistanceWindow.grab_set()
        self.ResistanceWindow.focus_force()
        self.ResistanceWindow.minsize(width = 200, height = 100)
        self.ResistanceWindow.maxsize(width = 200, height = 100)
        self.ResistanceWindow.title('Change resistance')        
        
        self.info = Label(self.ResistanceWindow, text = 'Enter the resistance (in ohms)\nof the resistor No ' + str(self.num) + ':')
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
        self.resistance = int(self.input.get())
        self.ResistanceWindow.destroy()
    
    def Cancel_action(self, event):
        self.ResistanceWindow.destroy()
    
    def get1_press(self, event):
        self.data['x'] = event.x
        self.data['y'] = event.y
    
    def get1_release(self, event):
        self.data['x'] = 0
        self.data['y'] = 0
        
        ResistorCanvas.delete(self.get1)
        self.get1 = ResistorCanvas.create_oval(self.xstart + 3, self.ystart + 3, self.xstart - 3, self.ystart - 3, width = 0, tags = 'get1' + str(self.num), fill = 'black')
        
        ResistorCanvas.delete(self.body)
        self.body = ResistorCanvas.create_rectangle(self.xbody, self.ybody, self.xbody + 40, self.ybody + 20, width = 3, fill = 'white', tags = 'resistor' + str(self.num))        
        
    def get1_motion(self, event):
        delta_x = event.x - self.data['x']
        delta_y = event.y - self.data['y']
        
        self.xstart += delta_x
        self.ystart += delta_y
        
        ResistorCanvas.move(self.get1, delta_x, delta_y)
        
        ResistorCanvas.delete(self.line1)
        self.line1 = ResistorCanvas.create_line(self.xstart, self.ystart, self.xbody, self.ybody + 10, width = 3)       
        
        ResistorCanvas.delete(self.body)
        self.body = ResistorCanvas.create_rectangle(self.xbody, self.ybody, self.xbody + 40, self.ybody + 20, width = 3, fill = 'white', tags = 'resistor' + str(self.num))
        
        self.data['x'] = event.x
        self.data['y'] = event.y  
    
    def get2_press(self, event):
        self.data['x'] = event.x
        self.data['y'] = event.y
    
    def get2_release(self, event):
        self.data['x'] = 0
        self.data['y'] = 0
        
        ResistorCanvas.delete(self.get2)
        self.get2 = ResistorCanvas.create_oval(self.xend + 3, self.yend + 3, self.xend - 3, self.yend - 3, width = 0, tags = 'get2' + str(self.num), fill = 'black')
        
        ResistorCanvas.delete(self.body)
        self.body = ResistorCanvas.create_rectangle(self.xbody, self.ybody, self.xbody + 40, self.ybody + 20, width = 3, fill = 'white', tags = 'resistor' + str(self.num))        
    
    def get2_motion(self, event):
        delta_x = event.x - self.data['x']
        delta_y = event.y - self.data['y']
        
        self.xend += delta_x
        self.yend += delta_y
        
        ResistorCanvas.move(self.get2, delta_x, delta_y)
        
        ResistorCanvas.delete(self.line2)
        self.line2 = ResistorCanvas.create_line(self.xbody + 40, self.ybody + 10, self.xend, self.yend, width = 3)       
        
        ResistorCanvas.delete(self.body)
        self.body = ResistorCanvas.create_rectangle(self.xbody, self.ybody, self.xbody + 40, self.ybody + 20, width = 3, fill = 'white', tags = 'resistor' + str(self.num))               
        
        self.data['x'] = event.x
        self.data['y'] = event.y    

'''
Need to write:
Example = resistor()
Example.num = examplenum
Example.load(ResistorCanvas)
'''

def CreateResistor(event):
    global ResistorCanvas, ResistorNum
    new_one = resistor()
    new_one.num = ResistorNum
    ResistorNum += 1
    new_one.load(ResistorCanvas)

ResistorButtons = Frame(Resistor)
ResistorButtons.place(x = 400, y = 0, width = 400, height = 400)

ResistorNum = 1

createresistor = Button(ResistorButtons, text = 'Create resistor')
createresistor.bind('<Button-1>', CreateResistor)
createresistor.place(x = 0, y = 0, width = 200, height = 40)

Resistor.mainloop()