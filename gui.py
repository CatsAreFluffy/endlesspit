from tkinter import *
from random import randint,choice,seed
class App(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        seed(0)
        self.cellsize=32
        self.createWidgets()
    def createWidgets(self):
        self.draw=Canvas(self,width=16*self.cellsize+6,height=16*self.cellsize+6)
        self.creategrid()
        self.draw.pack(side="left")
        self.gamemap[self.playerx][self.playery].uncap()
        self.drawgrid(self.cellsize)
        self.drawtiles()
    def buttonaevent(self):
        pass
    def buttonbevent(self):
        pass
    def creategrid(self):
        self.gamemap=[[Tile(j,i,self.cellsize,self.draw,self) for i in range(0,16)] for j in range(0,16)]
        self.playerx=randint(1,15)
        self.playery=randint(1,15)
        treasure=["gold"]
        monsters=["rat"]
        for i in range(10):
            self.gamemap[randint(0,15)][randint(0,15)].tile=choice(monsters)
        for i in range(10):
            self.gamemap[randint(0,15)][randint(0,15)].tile=choice(treasure)
    def drawgrid(self,cellsize):
        self.draw.width=7+16*cellsize
        self.draw.height=7+16*cellsize
        self.grid=self.draw.create_rectangle(7,7,7+16*cellsize,7+16*cellsize,width=1,fill="#666")
        temp=7
        for i in range(1,16):
            self.draw.create_line(7,7+i*cellsize,7+16*cellsize,7+i*cellsize)
            self.draw.create_line(7+i*cellsize,7,7+i*cellsize,7+16*cellsize)           
        self.cellsize=cellsize
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
        print(movx,movy)
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
    def draw(self):
        if self.capped:
            self.objects.append(self.canvas.create_rectangle(7+(self.x)*self.cellsize,7+(self.y)*self.cellsize,7+(self.x+1)*self.cellsize,7+(self.y+1)*self.cellsize,fill="#666"))
            self.canvas.tag_bind(self.objects[0],"<Button-1>",self.action)
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
    def interact(self):
        pass
    def standable(self):
        return (self.tile in ["blank"]+self.treasure+self.ground) and (not self.capped)
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
root=Tk()
app=App(master=root)
app.mainloop()
