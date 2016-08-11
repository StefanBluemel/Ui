import gi
import requests
#import time
#import threading
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,Gdk
from gi.repository import GdkPixbuf
import urllib3

class FixedExample():#threading.Thread):


    def __init__(self):
        self.x = 0
        self.y = 0
        self.firsttimeclicked = 0

        self.fixes = []             #Liste für die fixes von den users.buttons
        self.fixes2 = []            #Liste für die fixes von den drinks.buttons

        self.window = Gtk.Window()
        self.window.connect("destroy", lambda w: Gtk.main_quit())
        self.window.set_border_width(0)


        self.fixed = Gtk.Fixed()
        self.window.add(self.fixed)
        self.fixed.show()


        self.window.fullscreen()
        self.window.show()

    def daten_ausgabe(self, button, value, v2,box):


        if self.firsttimeclicked == 0:

            self.firsttimeclicked = 1
            print(value['name'], v2)
            for j in range(0, len(self.fixes)):
                self.fixes[j].hide()

            f = self.fixes[box]

            f = self.fixes[box]
            self.fixed.move(self.fixes[box],330+280,70+100)
            f.show()

            res2 = requests.get("https://mete.piratenfraktion-nrw.de/drinks.json")   #resources drinks
            data2= res2.json()

            #Creating drinks.buttons            
            i=0
            for x in range(0,6,1):
                for y in range(0,4,1):
                    if i>int(len(data2) - 1):
                        break

                    fix= Gtk.Fixed()
                    fix.show()
                    self.fixes2.append(fix)
                    self.fixed.add(fix)


                    vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
                    vbox.show()
                    fix.add(vbox)
                    self.boxes.append(i)

                    button = Gtk.Button()
                    button.set_size_request(150,150)
                    self.id.append('Button'+str(i+1))

                    button.show()
                    vbox.pack_start(button, True, True, 0)
                    button.connect("clicked", self.daten_ausgabe2)

                    self.fixed.move(fix,330+200*y,370+200*x)

                    i+=1
    def daten_ausgabe2(self,button):
        pass



    def run(self):
        i=0
        res =requests.get("https://mete.piratenfraktion-nrw.de/users.json")   #resources : users
        data = res.json()
        self.id = []
        self.boxes = []

        for x in range(0,5,1):
            for y in range(0,6,1):
                if i>int(len(data) - 1):
                    break


                fix= Gtk.Fixed()
                fix.show()
                self.fixes.append(fix)
                self.fixed.add(fix)


                vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
                vbox.show()
                fix.add(vbox)
                self.boxes.append(i)

                button = Gtk.Button()
                button.set_size_request(150,150)
                self.id.append('Button'+str(i+1))



                button.show()
                vbox.pack_start(button, True, True, 0)
                button.connect("clicked", self.daten_ausgabe, data[i], self.id[i],self.boxes[i])



                pixbuf = GdkPixbuf.Pixbuf().new_from_file('eye.png')
                image = Gtk.Image().new_from_pixbuf(pixbuf)
                button.add(image)

                pixbuf = pixbuf.scale_simple(150, 150,GdkPixbuf.InterpType.BILINEAR)
                image.set_from_pixbuf(pixbuf)


                image.show_all()

                l  = str(data[i]['name'])



                label = Gtk.Label(label=(l))
                label.show()
                vbox.pack_start(label, True, True, 0)

                self.fixed.move(fix,330+200*y,70+200*x)

                if i < 2:
                    if i == 0:
                        button2 = Gtk.Button(label="Users")
                        button2.show()
                        self.fixed.add(button2)
                        self.fixed.move(button2,100,240)
                    else:
                        button2 = Gtk.Button(label="Drinks")
                        button2.show()
                        self.fixed.add(button2)
                        self.fixed.move(button2,100,440)

                i += 1




def main():
    t1 = FixedExample()
    t1.run()
    #t1.start()
    Gtk.main()

if __name__ == "__main__":
    main()



