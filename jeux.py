import pygame
from pygame.locals import Color
import time
from random import *

import sqlite3

Donnees = "C:/Users/Hassan.akar/PycharmProjects/FlappyMan/Donnees.sq3"
conn = sqlite3.connect(Donnees)
cur = conn.cursor()
#cur.execute("CREATE TABLE membres (score integer)")
#cur.execute("insert into membres (score) values (0)")
#conn.commit()




background = pygame.image.load('image/background.png')
blanc = (255,255,255)


pygame.init()

fenetreLargeur = 800
fenetreHauteur = 500
mrMuscleLargeur = 50
mrMuscleHauteur = 66
haltereLargeur = 300
haltereHauteur = 300


fenetre = pygame.display.set_mode((fenetreLargeur,fenetreHauteur))#Création de la fenêtre du jeu en paramètre la largeur et la hauteur
pygame.display.set_caption("FlappyMan") #Création d'un nom pour notre fenêtre de jeu. J'ai mis le nom de mon jeu.
horloge = pygame.time.Clock() #Horloge de pygame


imageMuscle = pygame.image.load('image/muscle.png')
haltereHaut = pygame.image.load('image/NuageBas.png')
haltereBas = pygame.image.load('image/NuageHaut.png')

pygame.display.flip()

pygame.mixer.music.load("musique/Power Bots Loop.wav") #Musique du jeu
pygame.mixer.music.play(-1)




def score(iterateur):

    police = pygame.font.Font('font/BradBunR.ttf',24)
    texte = police.render("score : " + str(iterateur) , True ,(244,66,116))
    fenetre.blit(texte,[10,0])

def highScore(iterateur):

    police = pygame.font.Font('font/BradBunR.ttf',24)
    texte = police.render("high score : " + str(iterateur) , True ,(244,66,116))
    fenetre.blit(texte,[650,0])


def halteres(x_haltere,y_halere,espace):


    fenetre.blit(haltereHaut , (x_haltere,y_halere)) #Affichage du 1er haltere. Pour le 1er haltere x et y ont la même valeur

    fenetre.blit(haltereBas, (x_haltere, y_halere+haltereLargeur+espace))  # Ici cela correspond a y + la hauteur du nuage + l'espace pour placer l'haltere en bas.


def playOrQuit():
    for event in pygame.event.get([pygame.KEYDOWN , pygame.KEYUP , pygame.QUIT]): #Parcours les event keydown keyup et quit
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYUP: #On utilise le relachement de la touche pour que la personne appuie à nouveau pour continuer et relache à nouveau
            continue
        return event.key #Retourne une touche du clavier
    return None



def creaTexteObj(text,police):
    textFenetre = police.render(text,True,(244,66,116))
    return  textFenetre, textFenetre.get_rect()


def message(texte):
    gameOverTexte = pygame.font.Font('font/BradBunR.ttf',150) #definit une police ainsi que sa taille
    petitTexte = pygame.font.Font('font/BradBunR.ttf', 30)

    gameOverTexteFenetre, gameOverTexteRect =creaTexteObj(texte,gameOverTexte) #Ici je met la variable en paramètre (texte) pour me facilité en cas de modification. J'aurais uniquement à modifier la methode game over
    gameOverTexteRect.center = fenetreLargeur/2, ((fenetreHauteur/2)-50)# pour centrer et espacer mes 2 messages.
    fenetre.blit(gameOverTexteFenetre,gameOverTexteRect)

    petitTexteFenetre, petitTexteRect = creaTexteObj("Appuyer sur une touche pour continuer", petitTexte)
    petitTexteRect.center = fenetreLargeur / 2, ((fenetreHauteur / 2) + 50)
    fenetre.blit(petitTexteFenetre, petitTexteRect)

    pygame.display.update() #Mise à jour de la fenetre
    time.sleep(1) #Temps de latence avant de recommencer le jeu.

    while playOrQuit() == None: # tant que la fonction ne renvoie rien
        horloge.tick()  #Nombre d'image par seconde correspond a 0 , pour que ce ne soit pas renouveler
    boucleJeu()



def gameOver(scoreActuel):
    a = str(scoreActuel)
    Donnees =  "C:/Users/Hassan.akar/PycharmProjects/FlappyMan/Donnees.sq3"
    conn = sqlite3.connect(Donnees)
    cur = conn.cursor()
    cur.execute("SELECT * from membres")
    liste = list(cur)
    hscore = []

    for i in range(0, len(liste)):
        hscore += liste[i]
    if (int(hscore[-1]) < scoreActuel):
        cur.execute("INSERT into membres(score) values(?)", (a,))
        conn.commit()
        cur.close()
        conn.close()




    message("Perdu!")


def deplacementImage(x,y,image):
    fenetre.blit(image, (x,y)) # La méthode blit permet d'ajouter par dessus notre fenetre notre image

def boucleJeu():
    x = 150 # largeur. plus le nombre est élevé plus notre tête sera avancé.
    y = 200 # Longueur. Plus le nombre est élevé plus notre tête descend
    y_mouvement = 0
    imageMuscle = pygame.image.load('image/muscle.png')  # charge l'image dans la variable imageMuscle

    x_haltere = fenetreLargeur
    y_haltere = randint(-300,10) # Nombre entier aleatoire
    espace = mrMuscleHauteur*3
    haltere_vitesse = 6

    score_actuel = 0


    game_over = False  # permet de fermer la fenetre de notre jeu. Boucle de base de notre jeu.
    while not game_over:

        for event in pygame.event.get():  # Parcours tous les evenement grace au for
            if event.type == pygame.QUIT: #Si c'est un evenement de type QUIT on arrete
                game_over = True
            if event.type ==  pygame.KEYDOWN: #Apuuie sur la touche
                if event.key == pygame.K_UP: #Fleche haute
                    y_mouvement = -6 # Les moins en y vont vers le haut
            if event.type == pygame.KEYUP: #Relache la touche
                y_mouvement = 6 #+5 pour que sa redescende de 5

        y = y+y_mouvement # pour mettre a jour constamment la position de y en fonction des evenements
        fenetre.blit(background,[0,0])  # Rafraichit l'écran pour qu'il prend bien en compte la l'image
        deplacementImage(x, y, imageMuscle)

        halteres(x_haltere,y_haltere , espace)

        score(score_actuel)
        cur.execute("select * from membres")
        liste = list(cur)
        print(cur)
        print(liste)

        hscore=[]
        for i in range (0, len(liste)):
            hscore += liste[i]
        print(hscore)

        highScore(hscore[-1])

        x_haltere -= haltere_vitesse

        if y > fenetreHauteur -65 or y < -1: #Si position actuelle image est supérieur à la hauteur de la fenetre. Point 0 de l'image est tout en haut. On laisse une petite marge du coup.
            gameOver(score_actuel)

        if x_haltere < (-1*haltereLargeur):  #-1 pour qu'on sort de l'écran , c'est l'axe des x!
            x_haltere = fenetreLargeur # On réinitialise la potition de l'haltere
            y_haltere = randint(-300,10) #Du coup on veut que la position de l'haltere soit de nouveau placé au pif pour éviter qu'il conserve sa place avant que l'haltere se barre.
            if score_actuel > 3 and score_actuel < 5:  # augmenter la difficulté du jeu en fonction du score. Plus le score sera eleve plus la vitesse de defilement du jeu augmenteras.
                haltere_vitesse = 6.5
                espace = mrMuscleHauteur * 2.7

            if score_actuel > 5 and score_actuel < 8:
                haltere_vitesse = 7
                espace = mrMuscleHauteur * 2.6


            if score_actuel > 7 and score_actuel < 10:
                haltere_vitesse = 7.5
                espace = mrMuscleHauteur * 2.4


        if (x + mrMuscleLargeur) > x_haltere + 40 and x + 40 < (x_haltere + haltereLargeur):
            if y + 20 < (y_haltere + haltereHauteur) or y + mrMuscleHauteur > (y_haltere + haltereHauteur + espace + 30):
                gameOver(score_actuel)

        if x_haltere < (x-haltereLargeur) < x_haltere + haltere_vitesse+1:
            score_actuel = score_actuel+1

        pygame.display.update()

boucleJeu()
pygame.quit()
quit()

