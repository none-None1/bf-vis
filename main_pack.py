import sys,os
from gui import GUI
os.chdir(sys._MEIPASS)
g=GUI()
g.initgui()
while 1:
    g.flip()
