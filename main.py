import pygame
import random

class Hirvio:
    def __init__(self,max_x:int,max_y:int):
        self.__max_x=max_x
        self.__max_y=max_y
        self.__nopeusx=1
        self.__nopeusy=1
        self.__x= 10
        self.__y= 10
    
    #Current place of the Monster
    def paikka(self):
        return (self.__x,self.__y)
    
    # Setting Monster to random place
    def aseta_paikka(self):
        self.__x= random.randint(0,self.__max_x)
        self.__y= random.randint(0,self.__max_y)
        arvo_uusi=True
        
        while arvo_uusi==True:
            if self.__x> 250 and self.__x < 450:
                if self.__y > 360:
                    self.__x= random.randint(0,self.__max_x)
                    self.__y= random.randint(0,self.__max_y)
                else:
                    arvo_uusi=False
            else:
                arvo_uusi=False
        
    # Calculatin new place for Monster
    def liikuta(self):
        if self.__nopeusx > 0 and self.__x >=  self.__max_x:
            self.__nopeusx = -self.__nopeusx
        
        if self.__nopeusx < 0 and self.__x <= 0:
            self.__nopeusx = -self.__nopeusx
            
        if self.__nopeusy > 0 and self.__y >=  self.__max_y:
            self.__nopeusy = -self.__nopeusy
        
        if self.__nopeusy < 0 and self.__y <= 0:
            self.__nopeusy = -self.__nopeusy
        
        self.__x+=self.__nopeusx
        self.__y+=self.__nopeusy
        
        return (self.__x,self.__y)
    
class Robotti():
    def __init__(self,max_x:int,max_y:int):
        self.__max_x=max_x
        self.__max_y=max_y
        self.__x = 320
        self.__y = 420
        self.__suunta=0 # 1 = right, 2 = down, 3 = left, 4 = up
        self.__liike=0
        
    # Current place of the Robot    
    def paikka(self):
        return (self.__x,self.__y)
    
    # Setting Robot to starting place 
    def aseta_paikka(self):
        self.__x= 320
        self.__y= 420
    
    # Moving Robot with keys
    def liikuta(self,suunta:int,liiku:int):
        
        if self.__liike != liiku and liiku >= 0:
            self.__liike = liiku
            self.__suunta = suunta
            
        if self.__liike==1:
            if self.__suunta == 1:
                if self.__x <= self.__max_x:
                    self.__x += 1
            elif self.__suunta == 2:
                if self.__y <= self.__max_y:
                    self.__y += 1
            elif self.__suunta == 3:
                if self.__x >= 0:
                    self.__x -= 1
            elif self.__suunta == 4:
                if self.__y >= 0:
                    self.__y -= 1      
                    
class Kolikko:
    def __init__(self):
        self.__x = random.randint(0,640-50)
        self.__y = random.randint(0,480-50)
    
    #Current place of the Kolikko 
    def paikka(self):
        return (self.__x,self.__y)
    
    #Setting Kolikko to new random place
    def arvopaikka(self):
        self.__x = random.randint(0,640-50)
        self.__y = random.randint(0,480-50)
        
class Kolikonmetsastys:
    screen_width=640
    screen_height=480
    __maks_pisteet=0
    
    def __init__(self):
        pygame.init()
        
        self.naytto = pygame.display.set_mode((Kolikonmetsastys.screen_width, Kolikonmetsastys.screen_height+20))
        self.fontti = pygame.font.SysFont("Arial", 24)
        self.kello = pygame.time.Clock()
        
        self.lataa_kuvat()
        self.__pisteet=0
        self.__loppu=False
        self.hirviot=[]
        
        pygame.display.set_caption("Kolikon metsästys")   
        ##Hirvio(screen width,screen height)
        
        for i in range (0,6):
            self.hirviot.append(Hirvio(Kolikonmetsastys.screen_width-self.kuvat[0].get_width(), Kolikonmetsastys.screen_height-self.kuvat[0].get_height()))
            self.hirviot[i].aseta_paikka()
            
        self.robotti=Robotti(Kolikonmetsastys.screen_width-self.kuvat[1].get_width(), Kolikonmetsastys.screen_height-self.kuvat[1].get_height())
        self.kolikko=Kolikko()
        
        self.silmukka()
    
    # Loading pictures for game objects
    def lataa_kuvat(self):
        self.kuvat = []
        for nimi in ["hirvio", "robo","kolikko"]:
            self.kuvat.append(pygame.image.load(nimi + ".png"))   
    
    # This is the game loop which controlls the whole game
    def silmukka(self):
        while True:
            self.tutki_tapahtumat()
            self.piirra_naytto()
    
    # This checks if Monster has got caught the Robot 
    def peli_ohi(self):
        robottipaikka=self.robotti.paikka()
        
        for hirvio in self.hirviot:
            hirviopaikka=hirvio.paikka()
            if hirviopaikka[0]+self.kuvat[0].get_width()-5>robottipaikka[0] and hirviopaikka[0]+5 < robottipaikka[0]+self.kuvat[1].get_width():
                if hirviopaikka[1]+self.kuvat[0].get_height()-5>robottipaikka[1] and hirviopaikka[1]+5 < robottipaikka[1]+self.kuvat[1].get_height():
                    if Kolikonmetsastys.__maks_pisteet<self.__pisteet:
                        Kolikonmetsastys.__maks_pisteet=self.__pisteet
                    return True
        
        return False   
    
    # This checks if Robot has caught Kolikko
    def poimikolikko(self):
        robottipaikka=self.robotti.paikka()
        kolikkopaikka=self.kolikko.paikka()
        
        if kolikkopaikka[0]+self.kuvat[0].get_width()-5>robottipaikka[0] and kolikkopaikka[0]+5 < robottipaikka[0]+self.kuvat[1].get_width():
            if kolikkopaikka[1]+self.kuvat[0].get_height()-5>robottipaikka[1] and kolikkopaikka[1]+5 < robottipaikka[1]+self.kuvat[1].get_height():
                self.__pisteet +=1
                self.kolikko.arvopaikka()
    
    # Initializes new game and sets variables
    def uusi_peli(self):
        for hirvio in self.hirviot:    
                hirvio.aseta_paikka()
        self.robotti.liikuta(0,0)
        self.robotti.aseta_paikka()
        self.kolikko.arvopaikka()
        self.__loppu=False
        self.__pisteet=0
        
    # Check user actions 
    def tutki_tapahtumat(self):
        ei_tapahtumia=0
        
        for tapahtuma in pygame.event.get():
            
            if tapahtuma.type == pygame.KEYDOWN:
                #print(tapahtuma)
                ei_tapahtumia=1
                
                if tapahtuma.key == pygame.K_RIGHT and self.__loppu==False:
                    self.robotti.liikuta(1,1)
                if tapahtuma.key == pygame.K_DOWN and self.__loppu==False:
                    self.robotti.liikuta(2,1)
                if tapahtuma.key == pygame.K_LEFT and self.__loppu==False:
                    self.robotti.liikuta(3,1)
                if tapahtuma.key == pygame.K_UP and self.__loppu==False:
                    self.robotti.liikuta(4,1)
                if tapahtuma.key == pygame.K_F2:
                    self.uusi_peli()
                if tapahtuma.key == pygame.K_ESCAPE:
                    exit()
                    
            if tapahtuma.type == pygame.KEYUP:                
                ei_tapahtumia=1
                
                if tapahtuma.key == pygame.K_LEFT and self.__loppu==False:
                    self.robotti.liikuta(0,0)
                if tapahtuma.key == pygame.K_RIGHT and self.__loppu==False:
                    self.robotti.liikuta(0,0)
                if tapahtuma.key == pygame.K_UP and self.__loppu==False:
                    self.robotti.liikuta(0,0)
                if tapahtuma.key == pygame.K_DOWN and self.__loppu==False:
                    self.robotti.liikuta(0,0)
            
            if tapahtuma.type == pygame.QUIT:
                        exit()
                        
        # If game is not ended
        if self.__loppu==False:
            if ei_tapahtumia==0:
                self.robotti.liikuta(0,-1)
                
            for hirvio in self.hirviot:    
                hirvio.liikuta()
                
            self.__loppu=self.peli_ohi()
            self.poimikolikko()
    
    # Drawing the screen
    def piirra_naytto(self):
        
        self.naytto.fill((0,102,204))
        
        for hirvio in self.hirviot:   
            self.naytto.blit(self.kuvat[0], hirvio.paikka())
            
        self.naytto.blit(self.kuvat[1], self.robotti.paikka())
        self.naytto.blit(self.kuvat[2], self.kolikko.paikka())
        
        # If game is ended
        if self.__loppu == True:
            teksti = self.fontti.render("Valitettavasti mörkö sai sinut kiinni!", True, (0, 0, 0))
            pygame.draw.rect(self.naytto, (0,152,254), (180, 200, teksti.get_width(), teksti.get_height()))
            self.naytto.blit(teksti, (180, 200))
            teksti = self.fontti.render(f"Pisteesi: {self.__pisteet}", True, (0, 0, 0))
            pygame.draw.rect(self.naytto, (0,152,254), (180, 230, teksti.get_width(), teksti.get_height()))
            self.naytto.blit(teksti, (180, 230))
            
        else:
            self.kello.tick(200)
        
        # Draw points, and "guide"    
        pygame.draw.rect(self.naytto, (0,152,254), (0, Kolikonmetsastys.screen_height-10, Kolikonmetsastys.screen_width,Kolikonmetsastys.screen_height))    
        teksti = self.fontti.render(f"Pisteet: {self.__pisteet}" , True, (0, 0, 0))
        self.naytto.blit(teksti, (50, Kolikonmetsastys.screen_height-10))
        
        teksti = self.fontti.render("F2 = uusi peli", True, (0, 0, 0))
        self.naytto.blit(teksti, (200, Kolikonmetsastys.screen_height-10))

        teksti = self.fontti.render("Esc = sulje peli", True, (0, 0, 0))
        self.naytto.blit(teksti, (400, Kolikonmetsastys.screen_height-10))
        
        if Kolikonmetsastys.__maks_pisteet>0:
            teksti = self.fontti.render(f"Suurin pistemäärä: {Kolikonmetsastys.__maks_pisteet}", True, (0, 0, 0))
            self.naytto.blit(teksti, (10, 10))
        
        pygame.display.flip()

if __name__ == "__main__":
    Kolikonmetsastys()