import curses, random
from curses.textpad import rectangle
import os.path as filechecker

class Projectile:
    def __init__(self,stdscr,x,y,xf,yf):
        self.velocity = 3
        self.xp = x
        self.yp = y
        self.xf = xf
        self.yf = yf
        self.damage = 3
    def player_projectile_move(self,stdscr,limit,container,color):
        stdscr.addstr(self.yp,self.xp,"|",color | curses.A_BOLD)
        if self.yp > limit + 2:
            self.yp -= self.velocity
            stdscr.addstr(self.yp - 1, self.xp," ")
        else:
            stdscr.addstr(self.yp, self.xp, " ")
            container.remove(self)
class Fprojectile:
    def __init__(self,stdscr,xf,yf):
        self.velocity = 4
        self.xp = xf
        self.yp = yf
        self.damage = 3
    def foe_projectile_move(self,stdscr,limit,container,color):
        stdscr.addstr(self.yp,self.xp,"π",color | curses.A_BOLD)
        if self.yp < limit - 2:
            self.yp += self.velocity
            stdscr.addstr(self.yp + 1, self.xp," ")
        else:
            stdscr.addstr(self.yp, self.xp, " ")
            container.remove(self)
        
class Disc:
    charge = 25
    def __init__(self,stdscr,x,y):
        self.velocity = 3
        self.xp = x
        self.yp = y
        self.damage = 5

    def move(self,stdscr,limit,container,color):
        stdscr.addstr(self.yp,self.xp,"+",color | curses.A_BOLD)
        if self.yp > limit + 2:
            self.yp -= self.velocity
            stdscr.addstr(self.yp - 1, self.xp," ")
        else:
            stdscr.addstr(self.yp, self.xp, " ")
            container.remove(self)
        
class Foe:
    magazine = 0
    def __init__(self,stdscr,limit):
        self.velocity = random.randint(1,4)
        self.ys = [4,6,8]
        self.health = 3
        self.yf = random.choice(self.ys)
        self.sense = ["LEFT","RIGHT"]        
        self.direction = random.choice(self.sense)
        self.designs = ["<@>","<*>","<->"]
        if self.direction == "LEFT":
            self.xf = 2
        else:
            self.xf = limit
    def move(self,stdscr,limit,container,color):
        stdscr.addstr(self.yf,self.xf,random.choice(self.designs),color | curses.A_BOLD)
        if self.direction == "LEFT":
            if self.xf < limit - 3:
                self.xf += self.velocity
                stdscr.addstr(self.yf,self.xf - 1, " ")

        else:
            if self.xf > 3:
                self.xf -= self.velocity
                stdscr.addstr(self.yf,self.xf + 1, " ")
        if self.xf <= 3 or self.xf >= limit - 3:
            stdscr.addstr(self.yf, self.xf, " ")
            container.remove(self)
        self.foe_coords = (self.xf, self.yf)
    def launch(self,stdscr,container):
        if self.magazine <= 3:
                container.append(Fprojectile(stdscr,self.xf,self.yf))
                self.magazine += 1
def checkcollid(stdscr,item,itemlist,targetlist,score):
    x = item.xp
    y = item.yp
    for target in targetlist:
        tx = target.xf
        ty = target.yf
        if x in range(tx - 2, tx + 3) and y in range(ty - 1, ty + 2):
            target.health -= item.damage
            try:
                itemlist.remove(item)
            except:
                pass
            if target.health <= 0:
                stdscr.addstr(ty,tx," ")
                targetlist.remove(target)
                score += 1
    return score
    
def dcheckcollid(stdscr,item,itemlist,targetlist,pvs,score):
    x = item.xp
    y = item.yp
    for target in targetlist:
        tx = target.xf
        ty = target.yf
        if x in range(tx - 2, tx + 3) and y in range(ty - 1, ty + 2):
            target.health -= item.damage
            try:
                itemlist.remove(item)
            except:
                pass
            if target.health <= 0:
                stdscr.addstr(ty,tx," ")
                targetlist.remove(target)
                pvs += 10
                score += 1
    return pvs,score
    
def fcheckcollid(stdscr,item,itemlist,tx,ty,pvs,message):
    h,w = stdscr.getmaxyx()
    x = item.xp
    y = item.yp
    game_ended = 0
    if x in range(tx - 3, tx + 4) and y in range(ty - 3, ty + 4):
        pvs -= item.damage
        itemlist.remove(item)
        if pvs <= 0:
            stdscr.addstr(h // 2, w // 2 - len(message) + 6,message, curses.A_BOLD)
            game_ended = 1
        
    return pvs,game_ended

def save_score(score):
    best_score = 0
    filename = "score.txt"
    if not filechecker.exists(filename):
        with open(filename,"w") as sc:
            sc.write("Best score: 0")
    else:
        with open(filename,"r") as sc:
            content = sc.read()
            if len(content) > 0:
                tabline = content.split(" ")
                best_score = int(tabline[-1])
        with open(filename,"w") as sc2:
            if score > best_score:
                sc2.write(f"Best score: {score}")
                
def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(50)
    h,w = stdscr.getmaxyx()
    h -= 2
    w -= 2
    
    curses.init_pair(1,curses.COLOR_GREEN,0)
    curses.init_pair(2,curses.COLOR_CYAN,0)
    curses.init_pair(3,curses.COLOR_YELLOW,0)
    curses.init_pair(4,curses.COLOR_RED,0)
    curses.init_pair(5,curses.COLOR_MAGENTA,0)
    curses.init_pair(6,curses.COLOR_WHITE,curses.COLOR_BLACK)
    colors = [curses.color_pair(1), curses.color_pair(2), curses.color_pair(3),curses.color_pair(4),curses.color_pair(5),curses.color_pair(6)]
    stdscr.bkgd(" ",colors[1])
    
    pvelocity = 2
    i = 0
    x = 2
    score = 0
    pvs = 20
    direction = curses.KEY_RIGHT
    projectiles = []
    discs = []
    foes = []
    fprojectiles = []
    game_ended = 0
    lefting = False
    while 1:
        i += 1
        rectangle(stdscr,1, 1,h,w)
        key = stdscr.getch()
        stdscr.clear()
    
        keylist = [curses.KEY_LEFT, curses.KEY_RIGHT, curses.KEY_UP, curses.KEY_DOWN, curses.KEY_BACKSPACE,curses.KEY_ENTER]
        foes_number = random.randint(1,6)
        if len(foes) <= foes_number:
            foes.append(Foe(stdscr,w - 2))
        if key in keylist:
            direction = key
        if direction == curses.KEY_BACKSPACE:
            break
        elif direction == curses.KEY_LEFT:
            lefting = True
            if x > 2:
                x -= pvelocity
        elif direction == curses.KEY_RIGHT:
            lefting = False
            if x < w - 4:
                x += pvelocity
        if direction == curses.KEY_UP:
            if lefting:
                direction = curses.KEY_LEFT
            else:
                direction = curses.KEY_RIGHT
            projectiles.append(Projectile(stdscr,x,h,0,0))
        if direction == curses.KEY_DOWN:
            Disc.charge -= 1
            if lefting:
                direction = curses.KEY_LEFT
            else:
                direction = curses.KEY_RIGHT
            if Disc.charge > 0:
                discs.append(Disc(stdscr,x,h))
        if Disc.charge > 0:
            stdscr.addstr(0,w-15,f"{Disc.charge} left",colors[4] | curses.A_BOLD)
        else:
            stdscr.addstr(0,w-15,"box empty",colors[4] | curses.A_BOLD)
        for p in projectiles:
            p.player_projectile_move(stdscr,2,projectiles,colors[5])
            score = checkcollid(stdscr,p,projectiles,foes,score)

        
        for d in discs:
            d.move(stdscr,2,discs,colors[4])
            pvs,score = dcheckcollid(stdscr,d,discs,foes,pvs,score)

        for f in foes:
            coords = f.move(stdscr,w,foes,colors[0])
            if f.xf in range(x - 4, x + 5) and i % 6 == 0:
                f.launch(stdscr,fprojectiles)
        for fp in fprojectiles:
            fp.foe_projectile_move(stdscr,h - 2,fprojectiles,colors[2])
            pvs,game_ended = fcheckcollid(stdscr,fp,fprojectiles,x,h,pvs,"Game over!")
        if game_ended:
            stdscr.nodelay(0)
            stdscr.getch()
            break
        textscore = f"Score: {score}"
        textpv = f"HPS: {pvs}"
        stdscr.addstr(0, w // 2 - len(textscore), textscore,colors[0] | curses.A_BOLD)
        stdscr.addstr(0, 0, textpv,colors[2] | curses.A_BOLD)
        stdscr.addstr(h - 1, x, "[=]",colors[1] | curses.A_BOLD)
    save_score(score)
        
    
    stdscr.refresh()
curses.wrapper(main)
