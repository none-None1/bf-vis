"""
GUI interface.
"""
from tkinter import *
from PIL import Image,ImageTk
from bf import BrainFuck
import sys
import tkinter.messagebox as tmb
import tkinter.filedialog as tfd
class GUI:
    """
    GUI interface
    """
    def __init__(self):
        self.tk=Tk()
        self.active=True
        self.vm=BrainFuck()
        self.labels=[]
        self.pointer=None
        self.code_editor=None
        self.input_editor=None
        self.output_display=None
        self.visbtn=None
        self.combobox=None
        self.abrbtn=None
        self.copybtn = None
        self.abort_btn=None
        self.openbtn=None
        self.active_label=[StringVar() for i in range(10)]
        self.running=False
        self.itk=ImageTk.PhotoImage(Image.open('pointer.png'))
        self.icon=ImageTk.PhotoImage(Image.open('icon.png'))
    def flip(self):
        if not self.active:
            sys.exit()
        self.tk.update()
    def initgui(self):
        self.tk.geometry('600x600')
        self.tk.title('It\'s a Brainfuck Visualizer! - Not Running')
        self.tk.iconphoto(False,self.icon)
        self.tk.bind('<Control-r>',lambda *_:self.run())
        self.tk.bind('<Control-s>',lambda *_:self.step())
        self.tk.bind('<Control-o>',lambda *_:self.openfile())
        self.tk.bind('<Control-b>',lambda *_:self.abort())
        self.pointer=Label(self.tk,image=self.itk,text='pointer:0',compound=CENTER)
        self.pointer.place(x=30,y=10,height=30,width=90)
        for i in range(10):
            self.active_label[i].set('0')
            self.labels.append(Label(self.tk,textvariable=self.active_label[i],relief=GROOVE))
            self.labels[-1].place(y=50,x=(i+1)*50,width=50,height=50)
        self.code_editor=Text()
        self.code_editor.insert(END,'[Your Code Here]')
        self.code_editor.tag_config('running-cmd', background='green')
        self.code_editor.place(y=100,x=50,width=500,height=150)
        self.input_editor = Text()
        self.input_editor.tag_config('running-cmd', background='green')
        self.input_editor.insert(END, '[Input Here, usually ends with a line feed]')
        self.input_editor.place(y=250, x=50, width=500, height=150)
        self.output_display = Text()
        self.output_display.insert(END, '[Program Output]')
        self.output_display.place(y=400, x=50, width=500, height=150)
        self.output_display.bind('<Key>',lambda *_: 'break')
        self.visbtn=Button(self.tk,text='Run',command=self.run)
        self.visbtn.place(x=50,y=560,width=100,height=30)
        self.abrbtn = Button(self.tk, text='Step',command=self.step)
        self.abrbtn.place(x=150, y=560, width=100, height=30)
        self.abort_btn=Button(self.tk,text='Abort',command=self.abort)
        self.abort_btn.place(x=250,y=560,width=100,height=30)
        self.openbtn=Button(self.tk,text='Open File',command=self.openfile)
        self.openbtn.place(x=350,y=560,width=100,height=30)
        self.copybtn=Button(self.tk,text='Copy Output',command=self.copy)
        self.copybtn.place(x=450,y=560,width=100,height=30)
        self.tk.protocol('WM_DELETE_WINDOW', self.onexit)
    def onexit(self):
        self.active=False
        self.tk.quit()
        self.tk.destroy()
    def initrun(self):
        self.output_display.delete('1.0',END)
        self.input=self.input_editor.get('1.0',END)
        self.code=self.code_editor.get('1.0',END)
        self.code_editor.tag_remove('running-cmd','1.0',END)
        self.code_editor.tag_add('running-cmd', '1.0', '1.1')
        self.input_editor.tag_remove('running-cmd', '1.0', END)
        self.input_editor.tag_add('running-cmd', '1.0', '1.1')
        self.running=True
    def run(self):
        self.tk.title('It\'s a Brainfuck Visualizer! - Running')
        self.initrun()
        self.vm.load(self.code.strip(),self.input)
    def step(self):
        if not self.running:
            tmb.showerror('It\'s a Brainfuck Visualizer - Error','You cannot step when not running!')
            return
        if not self.vm.running():
            self.tk.title('It\'s a Brainfuck Visualizer! - Not Running')
            self.running=False
            self.code_editor.tag_remove('running-cmd', '1.0', END)
            self.input_editor.tag_remove('running-cmd', '1.0', END)
            return
        if not self.running:
            return
        self.code_editor.tag_add('running-cmd','1.0+'+str(self.vm.pos)+'c','1.0+' + str(self.vm.pos+1)+'c')
        self.input_editor.tag_add('running-cmd', '1.0+'+str(len(self.input)-len(self.vm.input))+'c', '1.0+'+str(len(self.input)-len(self.vm.input)+1)+'c')
        self.vm.step()
        self.upcell()
        self.code_editor.tag_remove('running-cmd','1.0',END)
        self.input_editor.tag_remove('running-cmd', '1.0', END)
        self.code_editor.tag_add('running-cmd', '1.0+' + str(self.vm.pos)+'c','1.0+' + str(self.vm.pos+1)+'c')
        self.input_editor.tag_add('running-cmd', '1.0+' + str(len(self.input) - len(self.vm.input)) + 'c',
                                  '1.0+' + str(len(self.input) - len(self.vm.input) + 1) + 'c')
        self.output_display.delete('1.0',END)
        self.output_display.insert(END,self.vm.output)
    def upcell(self):
        if self.vm.p>9:
            self.pointer.place(x=480)
            self.pointer.config(text='pointer:'+str(self.vm.p))
            for i in range(10):
                self.active_label[i].set(str(self.vm.cell[self.vm.p-9+i]))
        else:
            self.pointer.place(x=50*self.vm.p+30)
            self.pointer.config(text='pointer:' + str(self.vm.p))
            for i in range(10):
                self.active_label[i].set(str(self.vm.cell[i]))
    def abort(self):
        if not self.running:
            tmb.showerror('It\'s a Brainfuck Visualizer - Error','You cannot abort when not running!')
            return
        self.tk.title('It\'s a Brainfuck Visualizer! - Not Running')
        self.running=False
        self.code_editor.tag_remove('running-cmd','1.0',END)
        self.input_editor.tag_remove('running-cmd', '1.0', END)
    def openfile(self):
        if self.running:
            result=tmb.askyesno('It\'s a Brainfuck Visualizer - Confirm','The visualizer is running some code.\nAbort and open the file?')
            if result==NO:
                return
            else:
                self.abort()
        fp=tfd.askopenfilename(title='Open a Brainfuck file',filetypes=[('Brainfuck file .b','.b'),('Brainfuck file .f','.bf'),('All Files','.*')],initialdir='.')
        if not fp.strip():
            return
        try:
            with open(fp,'r',errors='ignore') as f:
                self.code_editor.delete('1.0',END)
                self.code_editor.insert(END,f.read())
        except BaseException as e:
            tmb.showerror('It\'s a Brainfuck Visualizer - Error','Can\'t open file, error is '+str(e))
    def copy(self):
        self.output_display.clipboard_append(self.output_display.get('1.0',END))
