from tkinter import *
from random import randint,choice,seed
class App(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        seed(0)
        self.cellsize=32
        self.gold=0
        self.hp=10
        self.maxhp=10
        self.agi=0
        self.str=0
        self.blk=0
        self.acc=0
        self.ui=[0,0,0,0,0]
        self.monsterlist=[]
        self.createWidgets()
    def createWidgets(self):
        self.draw=Canvas(self,width=16*self.cellsize+6,height=16*self.cellsize+6)
        self.creategrid()
        self.draw.pack(side="left")
        self.gamemap[self.playerx][self.playery].uncap()
        self.drawgrid(self.cellsize)
        self.drawtiles()
        self.createui()
        self.drawui()
    def creategrid(self):
        wmap=choice([\
            ["0000000000000000",\
            "0000000000000000",\
            "0011111111111100",\
            "0010000110000100",\
            "0000000110000000",\
            "0000000110000000",\
            "0000000110000000",\
            "0000000110000000",\
            "0000000110000000",\
            "0000000110000000",\
            "0000000110000000",\
            "0000000110000000",\
            "0000000110000000",\
            "0000001111000000",\
            "0000000000000000",\
            "0000000000000000"],\
            ["0000000000000000",\
            "0000000000000000",\
            "0000000000000000",\
            "0001111111111000",\
            "0001000000001000",\
            "0001000000001000",\
            "0001001001001000",\
            "0001001001001000",\
            "0001001001001000",\
            "0001001111001000",\
            "0001000000001000",\
            "0001000000001000",\
            "0001110000111000",\
            "0000000000000000",\
            "0000000000000000",\
            "0000000000000000"]])
        self.gamemap=[[Tile(j,i,self.cellsize,self.draw,self) for i in range(0,16)] for j in range(0,16)]
        self.playerx=randint(1,15)
        self.playery=randint(1,15)
        treasure=["gold"]
        monsters=["rat","cultist"]
        for i in range(10):
            x=randint(0,15)
            y=randint(0,15)
            if self.tile(x,y).tile=="blank":
                z=choice(monsters)
                self.gamemap[x][y].tile=z
                self.monsterlist.append(Monster(x,y,z,self))
        for i in range(10):
            x=randint(0,15)
            y=randint(0,15)
            if self.tile(x,y).tile=="blank":
                self.gamemap[x][y].tile=choice(treasure)
        for i in self.gamemap:
            for j in i:
                pass
                j.mapcheck(wmap)
    def drawgrid(self,cellsize):
        self.draw.width=7+16*cellsize
        self.draw.height=7+16*cellsize
        self.grid=self.draw.create_rectangle(7,7,7+16*cellsize,7+16*cellsize,width=1,fill="#666")
        temp=7
        for i in range(1,16):
            self.draw.create_line(7,7+i*cellsize,7+16*cellsize,7+i*cellsize)
            self.draw.create_line(7+i*cellsize,7,7+i*cellsize,7+16*cellsize)           
        self.cellsize=cellsize
    def createui(self):
        self.ui=[Label(text="HP:"+str(self.maxhp)+"/"+str(self.hp)),Label(text="STR: "+str(self.str)),Label(text="AGI: "+str(self.agi)),Label(text="DEF: "+str(self.blk)),Label(text="Gold: "+str(self.gold))]
        for i in self.ui:
            i.pack(side="top")
    def drawui(self):
        ui=self.ui
        ui[0]["text"]="HP:"+str(self.maxhp)+"/"+str(self.hp)
        ui[1]["text"]="STR: "+str(self.str)
        ui[2]["text"]="AGI: "+str(self.agi)
        ui[3]["text"]="DEF: "+str(self.blk)
        ui[4]["text"]="Gold: "+str(self.gold)
    def drawtiles(self):
        for i in self.gamemap:
            for j in i:
                j.draw()
    def tileclick(self,x,y):
        if abs(self.playerx-x)>1 or abs(self.playery-y)>1:
            self.move(x,y)
        elif self.tile(x,y).tile=="blank":
            self.move(x,y)
        else:
            self.tile(x,y).interact()
    def tile(self,x,y):
        if -1<x<len(self.gamemap) and -1<y<len(self.gamemap):
            return self.gamemap[x][y]
        else:
            return Tile(x,y,self.cellsize,self.draw,self)
    def move(self,x,y):
        movx=0
        movy=0
        if self.playerx>x:
            movx=-1
        if self.playerx<x:
            movx=1
        if self.playery>y:
            movy=-1
        if self.playery<y:
            movy=1
        if self.tile(self.playerx+movx,self.playery+movy).standable():
            self.playerx+=movx
            self.playery+=movy
        elif self.tile(self.playerx,self.playery+movy).standable():
            self.playery+=movy
            movx=0
        elif self.tile(self.playerx+movx,self.playery).standable():
            self.playerx+=movx
            movy=0
        self.tile(self.playerx-movx,self.playery-movy).clear()
        self.tile(self.playerx-movx,self.playery-movy).draw()
        self.tile(self.playerx,self.playery).clear()
        self.tile(self.playerx,self.playery).uncap()
        self.tile(self.playerx,self.playery).draw()
    def turn(self):
        for i in self.monsterlist:
            i.turn()
class Tile:
    def __init__(self,x,y,cellsize,canvas,upper,tile="blank"):
        self.tile=tile
        self.capped=True
        self.x=x
        self.y=y
        self.cellsize=cellsize
        self.canvas=canvas
        self.upper=upper
        self.objects=[]
        self.monsters=["rat"]
        self.treasure=["gold"]
        self.ground=[]
    def mapcheck(self,wmap):
        if wmap[self.y][self.x]=="1":
            self.tile="wall"
    def draw(self):
        self.clear()
        if self.capped:
            self.objects.append(self.canvas.create_rectangle(7+(self.x)*self.cellsize,7+(self.y)*self.cellsize,7+(self.x+1)*self.cellsize,7+(self.y+1)*self.cellsize,fill="#666"))
            self.canvas.tag_bind(self.objects[0],"<Button-1>",self.action)
        else:
            if self.tile=="wall":
                self.objects.append(self.canvas.create_rectangle(7+(self.x)*self.cellsize,7+(self.y)*self.cellsize,7+(self.x+1)*self.cellsize,7+(self.y+1)*self.cellsize,fill="#111"))
            else:
                self.objects.append(self.canvas.create_rectangle(7+(self.x)*self.cellsize,7+(self.y)*self.cellsize,7+(self.x+1)*self.cellsize,7+(self.y+1)*self.cellsize,fill="#ccc"))
            if self.tile=="blank":
                monsters,treasure=self.search()
                nearby=monsters+treasure
                if monsters==0:
                    types="#0c0"
                elif treasure==0:
                    types="#c00"
                else:
                    types="#ee0"
                if nearby>0:
                    self.objects.append(self.canvas.create_text(7+(self.x+0.5)*self.cellsize,7+(self.y+0.5)*self.cellsize,text=nearby,fill=types,font=('Helvetica',str(int(self.cellsize*0.75)))))
            elif self.tile=="gold":
                self.objects.append(self.canvas.create_text(7+(self.x+0.5)*self.cellsize,7+(self.y+0.5)*self.cellsize,text="$",fill="#ff0",font=('Helvetica',str(int(self.cellsize*0.75)))))
            elif self.tile=="rat":
                self.objects.append(self.canvas.create_text(7+(self.x+0.5)*self.cellsize,7+(self.y+0.5)*self.cellsize,text="r",fill="#c40",font=('Helvetica',str(int(self.cellsize*0.75)))))
            elif self.tile=="cultist":
                self.objects.append(self.canvas.create_text(7+(self.x+0.5)*self.cellsize,7+(self.y+0.5)*self.cellsize,text="C",fill="#c00",font=('Helvetica',str(int(self.cellsize*0.75)))))
            for i in self.objects:
                self.canvas.tag_bind(i,"<Button-1>",self.action)
        if (self.x,self.y)==(self.upper.playerx,self.upper.playery):
            self.drawplayer()
    def drawplayer(self):
        self.uncap()
        self.objects.append(self.canvas.create_oval(9+(self.x)*self.cellsize,9+(self.y)*self.cellsize,5+(self.x+1)*self.cellsize,5+(self.y+1)*self.cellsize,fill="#fb0"))
    def clear(self):
        for i in self.objects:
            self.canvas.delete(i)
        self.objects=[]
    def uncap(self):
        self.capped=False
    def action(self,event):
        if self.capped:
            self.uncap()
            self.clear()
            self.draw()
        else:
            self.upper.tileclick(self.x,self.y)
        self.upper.turn()
    def updatenear(self):
        for i in range(-1,2):
            for j in range(-1,2):
                self.upper.tile(self.x+i,self.y+j).draw()        
    def interact(self):
        if self.tile=="gold":
            self.upper.gold+=10
            self.tile="blank"          
            self.draw()
            self.updatenear()
            self.upper.drawui()
    def standable(self):
        return (self.tile in ["blank"]+self.treasure+self.ground) and (not self.capped)
    def standablem(self):
        return (self.tile=="blank") and (not self.capped)
    def search(self):
        monsters=0
        treasure=0
        for i in range(-1,2):
            for j in range(-1,2):
                if self.upper.tile(self.x+i,self.y+j).tile in self.monsters:
                    monsters+=1
                if self.upper.tile(self.x+i,self.y+j).tile in self.treasure:
                    treasure+=1
        return [monsters,treasure]
class Monster:
    def __init__(self,x,y,tile,upper):
        self.x=x
        self.y=y
        self.tile=tile
        self.upper=upper
        if tile=="rat":
            self.hp=5
            self.dice=1
            self.dfaces=3
            self.agi=1
            self.str=-1
            self.blk=0
        elif tile=="cultist":
            self.hp=9
            self.dice=1
            self.dfaces=4
            self.agi=0
            self.str=0
            self.blk=0
    def turn(self):
        if abs(self.upper.playerx-self.x)>1 or abs(self.upper.playery-self.y)>1:
            self.move()
        else:
            pass
    def move(self):
        movx=0
        movy=0
        if not self.upper.tile(self.x,self.y).capped:
            if self.x>self.upper.playerx:
                movx=-1
            if self.x<self.upper.playerx:
                movx=1
            if self.y>self.upper.playery:
                movy=-1
            if self.y<self.upper.playery:
                movy=1
            if self.upper.tile(self.x+movx,self.y+movy).standablem():
                self.x+=movx
                self.y+=movy
            elif self.upper.tile(self.x,self.y+movy).standablem():
                self.y+=movy
                movx=0
            elif self.upper.tile(self.x+movx,self.y).standablem():
                self.x+=movx
                movy=0
            self.upper.tile(self.x-movx,self.y-movy).tile="blank"
            self.upper.tile(self.x-movx,self.y-movy).clear()
            self.upper.tile(self.x-movx,self.y-movy).draw()
            self.upper.tile(self.x-movx,self.y-movy).updatenear()
            self.upper.tile(self.x,self.y).tile=self.tile
            self.upper.tile(self.x,self.y).clear()
            self.upper.tile(self.x,self.y).draw()
            self.upper.tile(self.x,self.y).updatenear()
root=Tk()
app=App(master=root)
app.mainloop()
