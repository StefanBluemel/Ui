import gi
import requests
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,Gdk
from gi.repository import GdkPixbuf
import shutil


class FixedExample():#threading.Thread):


    def __init__(self):
        self.hostname = "https://mete.piratenfraktion-nrw.de/"
        self.x = 0
        self.y = 0
        self.firsttimeclicked = 0

        self.fixUsers = []             #Liste für die fixUsers von den users.buttons
        self.fixUsers2 = []            #Liste für die fixUsers von den drinks.buttons
        self.bal2 = None               #Zwischenspeicher für die balance des users
        self.id = []
        self.boxes = []


        self.window = Gtk.Window()
        self.window.connect("destroy", lambda w: Gtk.main_quit())
        self.window.set_border_width(0)


        self.fixed = Gtk.Fixed()
        self.window.add(self.fixed)
        self.fixed.show()


        self.window.show()

    def daten_ausgabe(self, button, value, v2,box,ii):
        
        
        if self.firsttimeclicked == 0:
            
            self.buttons= []            

            self.firsttimeclicked = 1
            print(value['name'], v2)         
            for j in range(0, len(self.fixUsers)):
                self.fixUsers[j].hide()

            f = self.fixUsers[box]
            self.fixed.move(self.fixUsers[box],330+280,70+100)
            f.show()       

            drinks = self.get_drinks()

            users = self.get_users()

            o  = str(users[ii]['balance'])
            bal = Gtk.Label('balance: '+o+'€')
            f.add(bal)
            bal.show()
            f.move(bal,43,180)

            #Creating drinks.buttons            
            i=0
            for x in range(0,6,1):
                for y in range(0,4,1):
                    if i>int(len(drinks) - 1):
                        break

                    drink_logo_url = str(drinks[i]['logo_url'])                    
                    drink_price = str(drinks[i]['price'])
                    drink_name = str(drinks[i]['name'])

                    fix= Gtk.Fixed()
                    fix.show()
                    self.fixUsers2.append(fix)
                    self.fixed.add(fix)
                    self.buttons.append(i)
                    
                    vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
                    vbox.show()
                    fix.add(vbox)
                    self.boxes.append(i)
                    
                    button = Gtk.Button()
                    button.set_size_request(150,150)
                    self.id.append('Button'+str(i+1))
                    
                    button.show()
                    vbox.pack_start(button, True, True, 0)
                    button.connect("clicked", self.daten_ausgabe2,i,bal,self.buttons[i],box)
                    
                    self.fixed.move(fix,330+200*y,370+200*x)
                    
                    
                    label_name = Gtk.Label(drink_name)
                    vbox.add(label_name)
                    label_name.show()

                    label_price = Gtk.Label(drink_price + "€")
                    vbox.add(label_price)
                    label_price.show()

                    response = requests.get(self.hostname + drink_logo_url, stream=True)                                                                                                                                 
                    with open('img.png', 'wb') as out_file:                                                                                                                                   
                        shutil.copyfileobj(response.raw, out_file)                                                                                                                            
                    del response                                                                                                                                                              
                                                                                                                                                                                              
                    pixbuf = GdkPixbuf.Pixbuf().new_from_file('img.png')                                                                                                                      
                    image = Gtk.Image().new_from_pixbuf(pixbuf)                                                                                                                               
                    button.add(image)
                    image.show_all()               

                    i += 1

            self.bal2 = bal


    def buy_drink(self, user_id, drink_id):
        res = requests.get("https://mete.piratenfraktion-nrw.de/users/"+str(user_id+1)+"/buy?drink="+str(drink_id+1))               
        #print(res) # TODO: Schoen machen!!!

    def get_user_data(self, user_id):
        res = requests.get("https://mete.piratenfraktion-nrw.de/users/" + str(user_id+1)  + ".json")   #resources : users
        return res.json()
        

    def get_users(self):
        res =requests.get("https://mete.piratenfraktion-nrw.de/users.json")   #resources : users
        return res.json()

    def get_drinks(self):
        res = requests.get(self.hostname + "drinks.json")   #resources drinks
        return res.json()
    
    def daten_ausgabe2(self,button,drink_id,bal,ibutton,user_id):


        
        self.fixUsers[user_id].remove(self.bal2)


        self.buy_drink(user_id, drink_id)
        print("UserId: ",  str(user_id+1), "DrinkId: ", str(drink_id+1))                

        data = self.get_user_data(user_id)
        print(data['balance'])

        o  = str(data['balance'])
        
        bal = Gtk.Label('balance: '+o+'€')
        
        
        self.fixUsers[ibutton].add(bal)
        bal.show()
        self.fixUsers[ibutton].move(bal,43,180)

        #self.bal2.append(bal)
        self.bal2=bal



    def run(self):
        i=0
        res =requests.get("https://mete.piratenfraktion-nrw.de/users.json")   #resources : users
        data = res.json()
        
        buttonUsers = Gtk.Button(label="Users")
        buttonUsers.show()
        self.fixed.add(buttonUsers)
        self.fixed.move(buttonUsers, 100, 240)

        buttonDrink = Gtk.Button(label="Drinks")
        buttonDrink.show()
        self.fixed.add(buttonDrink)
        self.fixed.move(buttonDrink, 100, 440)

        for x in range(0, 5, 1):
            for y in range(0, 6, 1):
                if i>int(len(data) - 1):
                    break
                
                fix= Gtk.Fixed()
                fix.show()
                self.fixUsers.append(fix)
                self.fixed.add(fix)
                vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
                vbox.show()
                fix.add(vbox)
                self.boxes.append(i)

                buttonUser = Gtk.Button()
                buttonUser.set_size_request(150, 150)
                buttonUser.show()

                vbox.pack_start(buttonUser, True, True, 0)
                self.id.append('Button' + str(i+1))
                buttonUser.connect("clicked", self.daten_ausgabe, data[i], self.id[i],self.boxes[i],i)



                


                pixbuf = GdkPixbuf.Pixbuf().new_from_file('eye.png')
                image = Gtk.Image().new_from_pixbuf(pixbuf)
                buttonUser.add(image)                

                pixbuf = pixbuf.scale_simple(150, 150,GdkPixbuf.InterpType.BILINEAR)
                image.set_from_pixbuf(pixbuf)


                image.show_all()
                
                l  = str(data[i]['name'])



                label = Gtk.Label(label=(l))
                label.show()
                vbox.pack_start(label, True, True, 0)

                self.fixed.move(fix,330+200*y,70+200*x)

                i += 1

def main():
    t1 = FixedExample()
    t1.run()
    #t1.start()
    Gtk.main()

if __name__ == "__main__":
    main()


