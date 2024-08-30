import pygame
import sys
from collections import Counter
from button import Button
import pygame_gui
import pandas as pd
import function

pygame.init()
SCREEN = pygame.display.set_mode((1280, 650))
pygame.display.set_caption("INTERFACE")
manager = pygame_gui.UIManager((1600, 900))
clock = pygame.time.Clock()
text_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((180, 275), (900, 50)), manager=manager,
                                               object_id='#main_text_entry')
def get_font(size): 
    if size <= 50:
        return pygame.font.SysFont('arial',size,italic=True,bold=False,)
    else:
        return pygame.font.SysFont('arial',size,italic=True,bold=True,)
def paly_regle_ass(algo,data,pl,regle):
    while True:
        SCREEN.fill("White")
        if algo=="A":
            text="LES RÈGLES D'ASSOCIATION AVEC LIFT DIFFÈRENT DE 1"
        if algo=="C":
            text="LES RÈGLES D'ASSOCIATION"
        MENU_TEXT = get_font(50).render(text, True, "#1C2833")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 30))
        SCREEN.blit(MENU_TEXT, MENU_RECT)
        posx=30
        posy=70
        if algo=="A":
            regle_a=function.regle(data,pl)
            regle_a=function.fonction(regle_a)
            for p in regle_a:
                
                TEXT = get_font(20).render(str(p[0])+"==>"+str("{0:.5f}".format(p[2])), True, "#1C2833")
                RECT = TEXT.get_rect(topleft=(posx,posy))
                SCREEN.blit(TEXT,RECT)
                posy=posy+20
                if posy >600:
                    posx=640
                    posy=70
                    
        if algo =="C":
            for r in regle:
                for i in r:
                    TEXT = get_font(20).render(str(i)+" = 100%", True, "#1C2833")
                    RECT = TEXT.get_rect(topleft=(posx,posy))
                    SCREEN.blit(TEXT,RECT)
                    posy=posy+20
                    if posy >600:
                        posx=640
                        posy=70

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
    
x="SAISISSEZ UN MINSUP"
def paly_input_minsup(algo,x):
    while True:
        SCREEN.fill("White")
        MENU_TEXT = get_font(60).render(x, True, "#1C2833")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 80))
        SCREEN.blit(MENU_TEXT, MENU_RECT)
        UI_REFRESH_RATE = clock.tick(60)/1000
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if (event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and
                event.ui_object_id == '#main_text_entry'):
                    s=event.text
                    
                    if float(s)>1 or float(s)<0:
                        x="RÉESSAYER, LE MINSUP DOIT ÊTRE ENTRE 0 ET 1"
                        paly_input_minsup(algo,x)
                    else:
                        menu_pretraitement(algo,n=None,s=s)
                        
            manager.process_events(event)
            
        manager.update(UI_REFRESH_RATE)
        
        manager.draw_ui(SCREEN)
        
        pygame.display.update()
        

def play_itemset(algo,n1,n2,s):
    while True:
        SCREEN.fill("White")
        
        TITLE = get_font(70).render("LES ITEMES FREQUENTS SONT", True, "#1C2833")
        TITLE_RECT = TITLE.get_rect(center=(640,30))
        SCREEN.blit(TITLE,TITLE_RECT)
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        
        NEXT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(1100, 550), 
                            text_input="SUIVANT", font=get_font(50), base_color="#273746", hovering_color="#1A5276")
        
        posx=30
        posy=70
        data=None
        itemset=None
        regle=[]
        if algo=='A' and n1==1 and n2==1:
            import apriori_pretraitement1_minsup1 as a11
            pl=a11.pl 
            data=a11.data
        if algo=='A' and n1==1 and n2==2:
            import apriori_pretraitement1_minsup2 as a12
            pl=a12.pl
            data=a12.data
        if algo=='A' and n1==2 and n2==1:
            import apriori_pretraitement2_minsup1 as a21
            pl=a21.pl
            data=a21.data
        if algo=='A' and n1==2 and n2==2:
            import apriori_pretraitement2_minsup2 as a22
            pl=a22.pl
            data=a22.data
        if algo=='C' and n1==1 and n2==1:
            import close_pretraitement1_minsup1 as c11
            pl=c11.sl
            regle=c11.rules
        if algo=='C' and n1==1 and n2==2:
            import close_pretraitement1_minsup2 as c12
            pl=c12.sl
            regle=c12.rules
        if algo=='C' and n1==2 and n2==1:
            import close_pretraitement2_minsup1 as c21
            pl=c21.sl
            regle=c21.rules
        if algo=='C' and n1==2 and n2==2:
            import close_pretraitement2_minsup2 as c22
            pl=c22.sl
            regle=c22.rules

        if algo=='A' and n1==None and n2==1:
            
            watches =  pd.read_csv('watches.csv', sep=",")
            data=watches.loc[:,["brand_names","Gender","Type"]]
            data=data.to_numpy()
            data=function.upper_matrice(data)
            data=function.pretraitement1(data)

            itemset = []
            for l in data:
                for i in l:
                    if(i not in itemset):
                        itemset.append(i)
            itemset = sorted(itemset)
            mins=float(s)*len(itemset)
            pl=function.aprpri(data,itemset,mins)
            
        if algo=='A' and n1==None and n2==2:
            
            watches =  pd.read_csv('watches.csv', sep=",")
            data=watches.loc[:,["brand_names","Gender","Type"]]
            data=data.to_numpy()
            data=function.upper_matrice(data)
            data=function.pretraitement2(data)

            itemset = []
            for l in data:
                for i in l:
                     if(i not in itemset ):
                        itemset.append(i)
            itemset = sorted(itemset)
            mins=float(s)*len(itemset)
            pl=function.aprpri(data,itemset,mins)
            
        if algo=='C' and n1==None and n2==1:
            watches =  pd.read_csv('watches.csv', sep=",")
            data=watches.loc[:,["brand_names","Gender","Type"]]
            data=data.to_numpy()
            data=function.upper_matrice(data)
            data=function.pretraitement1(data)
            itemset = []
            for l in data:
                for i in l:
                    if(i not in itemset):
                        itemset.append(i)
            itemset = sorted(itemset)
            print(itemset)

            c = Counter()
            occurrence = set()
            for i in itemset:
                for d in data:
                    if(i in d):
                        c[i]+=1
                    occurrence.add(c[i])
            mins=float(s)*len(itemset)
            pl,regle=function.close(data,itemset,occurrence,c,mins)
            
        if algo=='C' and n1==None and n2==2:
            watches =  pd.read_csv('watches.csv', sep=",")
            data=watches.loc[:,["brand_names","Gender","Type"]]
            data=data.to_numpy()
            data=function.upper_matrice(data)
            data=function.pretraitement2(data)
            itemset = []
            for l in data:
                for i in l:
                    if(i not in itemset):
                        itemset.append(i)
            itemset = sorted(itemset)
            print(itemset)

            c = Counter()
            occurrence = set()
            for i in itemset:
                for d in data:
                    if(i in d):
                        c[i]+=1
                    occurrence.add(c[i])
            mins=float(s)*len(itemset)
            pl,regle=function.close(data,itemset,occurrence,c,mins)
            
        for p in pl :
            TEXT = get_font(20).render(str(list(p))+": "+str(pl[p]), True, "#1C2833")
            RECT = TEXT.get_rect(topleft=(posx,posy))
            SCREEN.blit(TEXT,RECT)
            posy=posy+20
                
        NEXT_BUTTON.changeColor(MENU_MOUSE_POS)
        NEXT_BUTTON.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if NEXT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    paly_regle_ass(algo,data,pl,regle)
                    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update() 
        
def menu_pretraitement(algo,n,s):
    while True:
        SCREEN.fill("White")
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        TEXT = get_font(70).render("CHOISIR LA MÉTHODE DE PRÉTRAITEMENT", True, "#1C2833")
        RECT = TEXT.get_rect(center=(640, 80))

        BUTTON1 = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 230), 
                            text_input="PRÉTRAITEMENT 1", font=get_font(50), base_color="#273746", hovering_color="#1A5276")
        BUTTON2 = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 380), 
                            text_input="PRÉTRAITEMENT 2", font=get_font(50), base_color="#273746", hovering_color="#1A5276")
        
        SCREEN.blit(TEXT, RECT)

        for button in [BUTTON1, BUTTON2]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BUTTON1.checkForInput(MENU_MOUSE_POS):
                    play_itemset(algo,n,1,s)
                    
                if BUTTON2.checkForInput(MENU_MOUSE_POS):
                    play_itemset(algo,n,2,s)
                    
        pygame.display.update()

def menu_minsup(algo):
    while True:
        SCREEN.fill("White")
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        TEXT = get_font(70).render("CHOISIR LA MÉTHODE DE MINSUP", True, "#1C2833")
        RECT = TEXT.get_rect(center=(640, 80))

        BUTTON1 = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 230), 
                            text_input="MINSUP 1", font=get_font(50), base_color="#273746", hovering_color="#1A5276")
        BUTTON2 = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 380), 
                            text_input="MINSUP 2", font=get_font(50), base_color="#273746", hovering_color="#1A5276")
        
        SCREEN.blit(TEXT, RECT)

        for button in [BUTTON1, BUTTON2]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BUTTON1.checkForInput(MENU_MOUSE_POS):
                    menu_pretraitement(algo,1,s=None)

                if BUTTON2.checkForInput(MENU_MOUSE_POS):
                    menu_pretraitement(algo,2,s=None)
        pygame.display.update()
           
def main_menu2(algo):
    while True:
        SCREEN.fill("White")
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        if algo=='A':
            text="ALGORITHME APRIORI"
        if algo=='C':
            text="ALGORITHME CLOSE"
        TEXT = get_font(100).render(text, True, "#1C2833")
        RECT = TEXT.get_rect(center=(640, 80))

        BUTTON1 = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 230), 
                            text_input="MINSUP AUTOMATIQUE", font=get_font(50), base_color="#273746", hovering_color="#1A5276")
        BUTTON2 = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 380), 
                            text_input="CHOISISSEZ LE MINSUP", font=get_font(50), base_color="#273746", hovering_color="#1A5276")
        
        SCREEN.blit(TEXT, RECT)

        for button in [BUTTON1, BUTTON2]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BUTTON1.checkForInput(MENU_MOUSE_POS):
                    menu_minsup(algo)
                    
                if BUTTON2.checkForInput(MENU_MOUSE_POS):
                    paly_input_minsup(algo,x)
                    
        pygame.display.update()
        
def main_menu():
    while True:
        SCREEN.fill("White")

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        TEXT = get_font(60).render("CHOISISSEZ L'ALGORITHME QUI VOUS CONVIENT", True, "#1C2833")
        RECT = TEXT.get_rect(center=(640, 80))

        BUTTON1 = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 230), 
                            text_input="APRIOPRI", font=get_font(50), base_color="#273746", hovering_color="#1A5276")
        BUTTON2 = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 380), 
                            text_input="CLOSE", font=get_font(50), base_color="#273746", hovering_color="#1A5276")
        
        SCREEN.blit(TEXT, RECT)

        for button in [BUTTON1, BUTTON2]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BUTTON1.checkForInput(MENU_MOUSE_POS):
                    main_menu2("A")
                    
                if BUTTON2.checkForInput(MENU_MOUSE_POS):
                    main_menu2("C")
                
        pygame.display.update()

main_menu()