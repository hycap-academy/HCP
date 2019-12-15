import pygame

class MapMaker():
    def __init__(self):
        print("Map Maker Initialized")
        self.TILESIZE=50

    def getSurf(self, surfType):
        ss = spritesheet('overworld_tileset_grass.png')
        if surfType=="basered":
            return pygame.transform.scale(ss.image_at((2*16+1, 16*16+1, 16, 16)).convert_alpha(), (self.TILESIZE, self.TILESIZE))
        elif surfType =="baseblack":
            return pygame.transform.scale(ss.image_at((2*16+1, 17*16+1, 16, 16)).convert_alpha(), (self.TILESIZE, self.TILESIZE))
        elif surfType =="baseyellow":
            return pygame.transform.scale(ss.image_at((2*16+1, 18*16+1, 16, 16)).convert_alpha(), (self.TILESIZE, self.TILESIZE))
        elif surfType=="dozerblue":
            return pygame.transform.scale(pygame.image.load("DozerBlue.png").convert_alpha(), (self.TILESIZE, self.TILESIZE))
        elif surfType=="dozerred":
            return pygame.transform.scale(pygame.image.load("DozerRed.png").convert_alpha(), (self.TILESIZE, self.TILESIZE))

    def makeMap(self, map):
        self.map = map.replace("\n", "").replace("\t", "")
        
        ss = spritesheet('overworld_tileset_grass.png')

        #G = Grass (1-9)
        #C = Crops (1,2,3)
        #V = Sprouting Crops(1,2,3)
        #B = Harvest Crops(1,2,3)

        #R = Road
        #D = DirtRoad
        #W = Wall
        #T = Tree

        #QWE
        #ASD
        #ZXC

        #H=Horz
        #V=Vert

        g1= pygame.transform.scale(ss.image_at((0, 0, 16, 16)), (self.TILESIZE, self.TILESIZE))
        g2 = pygame.transform.scale(ss.image_at((16*1+1, 0, 16, 16)), (self.TILESIZE, self.TILESIZE))
        

        wq = pygame.transform.scale(ss.image_at((16*9+1, 16*1+1, 16, 16)), (self.TILESIZE, self.TILESIZE))
        ww = pygame.transform.scale(ss.image_at((16*10+1, 16*1+1, 16, 16)), (self.TILESIZE, self.TILESIZE))
        we = pygame.transform.scale(ss.image_at((16*11+1, 16*1+1, 16, 16)), (self.TILESIZE, self.TILESIZE))
        wa = pygame.transform.scale(ss.image_at((16*9+1, 16*2+1, 16, 16)), (self.TILESIZE, self.TILESIZE))
        ws = pygame.transform.scale(ss.image_at((16*10+1, 16*2+1, 16, 16)), (self.TILESIZE, self.TILESIZE))
        wd = pygame.transform.scale(ss.image_at((16*11+1, 16*2+1, 16, 16)), (self.TILESIZE, self.TILESIZE))
        wz = pygame.transform.scale(ss.image_at((16*9+1, 16*3+1, 16, 16)), (self.TILESIZE, self.TILESIZE))
        wx = pygame.transform.scale(ss.image_at((16*10+1, 16*3+1, 16, 16)), (self.TILESIZE, self.TILESIZE))
        wc = pygame.transform.scale(ss.image_at((16*11+1, 16*3+1, 16, 16)), (self.TILESIZE, self.TILESIZE))
        wh = pygame.transform.scale(ss.image_at((16*10+1, 0, 16, 16)), (self.TILESIZE, self.TILESIZE))
        wv = pygame.transform.scale(ss.image_at((16*8+1, 16*2+1, 16, 16)), (self.TILESIZE, self.TILESIZE))

        rq = pygame.transform.scale(ss.image_at((16*5+1, 16*1+1, 16, 16)), (self.TILESIZE, self.TILESIZE))
        rw = pygame.transform.scale(ss.image_at((16*6+1, 16*1+1, 16, 16)), (self.TILESIZE, self.TILESIZE))
        re = pygame.transform.scale(ss.image_at((16*7+1, 16*1+1, 16, 16)), (self.TILESIZE, self.TILESIZE))
        ra = pygame.transform.scale(ss.image_at((16*5+1, 16*2+1, 16, 16)), (self.TILESIZE, self.TILESIZE))
        rs = pygame.transform.scale(ss.image_at((16*6+1, 16*2+1, 16, 16)), (self.TILESIZE, self.TILESIZE))
        rd = pygame.transform.scale(ss.image_at((16*7+1, 16*2+1, 16, 16)), (self.TILESIZE, self.TILESIZE))
        rz = pygame.transform.scale(ss.image_at((16*5+1, 16*3+1, 16, 16)), (self.TILESIZE, self.TILESIZE))
        rx = pygame.transform.scale(ss.image_at((16*6+1, 16*3+1, 16, 16)), (self.TILESIZE, self.TILESIZE))
        rc = pygame.transform.scale(ss.image_at((16*7+1, 16*3+1, 16, 16)), (self.TILESIZE, self.TILESIZE))
        rh = pygame.transform.scale(ss.image_at((16*6+1, 0, 16, 16)), (self.TILESIZE, self.TILESIZE))
        rv = pygame.transform.scale(ss.image_at((16*4+1, 16*2+1, 16, 16)), (self.TILESIZE, self.TILESIZE))

        x=0
        mapTiles = []
        aryMap = map.split()
        for x in range(0, int(len(aryMap[0])/2)):
            mapCol=[]
            for y in range(0, int(len(aryMap))):
               
                mapcode = aryMap[y][x*2]+aryMap[y][x*2+1]
                print(mapcode)
                mapItem=[]
                # Type:  0 is passable, 1 is jumpable, 2 is impassable

                if mapcode[0]=="g":
                    if mapcode[1]=="1":
                        mapItem.append(g1)
                    elif mapcode[1]=="2":
                        mapItem.append(g2)
                    mapItem.append(0)
                    mapItem.append("grass")
                elif mapcode[0]=="w":
                    if mapcode[1]=="q":
                        mapItem.append(wq)
                    elif mapcode[1]=="w":
                        mapItem.append(ww)
                    elif mapcode[1]=="e":
                        mapItem.append(we)
                    elif mapcode[1]=="a":
                        mapItem.append(wa)
                    elif mapcode[1]=="s":
                        mapItem.append(ws)
                    elif mapcode[1]=="d":
                        mapItem.append(wd)
                    elif mapcode[1]=="z":
                        mapItem.append(wz)
                    elif mapcode[1]=="x":
                        mapItem.append(wx)
                    elif mapcode[1]=="c":
                        mapItem.append(wc)
                    elif mapcode[1]=="h":
                        mapItem.append(wh)
                    elif mapcode[1]=="v":
                        mapItem.append(wv)

                    mapItem.append(2)
                    mapItem.append("wall")
                elif mapcode[0]=="r":
                    if mapcode[1]=="q":
                        mapItem.append(wq)
                    elif mapcode[1]=="w":
                        mapItem.append(ww)
                    elif mapcode[1]=="e":
                        mapItem.append(we)
                    elif mapcode[1]=="a":
                        mapItem.append(wa)
                    elif mapcode[1]=="s":
                        mapItem.append(ws)
                    elif mapcode[1]=="d":
                        mapItem.append(wd)
                    elif mapcode[1]=="z":
                        mapItem.append(wz)
                    elif mapcode[1]=="x":
                        mapItem.append(wx)
                    elif mapcode[1]=="c":
                        mapItem.append(wc)
                    elif mapcode[1]=="h":
                        mapItem.append(wh)
                    elif mapcode[1]=="v":
                        mapItem.append(wv)
                    mapItem.append(0)
                    mapItem.append("road")
                
                mapCol.append(mapItem)
            mr = mapCol.copy()
            mapTiles.append(mr)
            mapCol.clear()
        return mapTiles

        

#https://www.pygame.org/wiki/Spritesheet
class spritesheet(object):
    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename).convert_alpha()
        except pygame.error as message:
            print ('Unable to load spritesheet image:', filename, ":", message)
            raise SystemExit(message)
    # Load a specific image from a specific rectangle
    def image_at(self, rectangle, colorkey = None):
        "Loads image from x,y,x+offset,y+offset"
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert_alpha()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        else:
            image.set_colorkey((0,0,0,255), pygame.RLEACCEL)
        
        return image
    # Load a whole bunch of images and return them as a list
    def images_at(self, rects, colorkey = None):
        "Loads multiple images, supply a list of coordinates" 
        return [self.image_at(rect, colorkey) for rect in rects]
    # Load a whole strip of images
    def load_strip(self, rect, image_count, colorkey = None):
        "Loads a strip of images and returns them as a list"
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)