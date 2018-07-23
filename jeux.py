import time
from random import *
import sqlite3
import pygame

data = "C:/Users/MSI-HASSAN/Desktop/FlappyMan/Donnees.sq3"
conn = sqlite3.connect(data)
cur = conn.cursor()
#cur.execute("CREATE TABLE membres (score integer)")
#cur.execute("insert into membres (score) values (0)")
#conn.commit()

background = pygame.image.load('image/background.png')
blanc = (255, 255, 255)

pygame.init()

window_width = 800
window_hight = 500
shwarzy_width = 50
shwarzy_hight = 66
cloud_width = 300
cloud_hight = 300
# Création de la fenêtre du jeu en paramètre la largeur et la hauteur
window = pygame.display.set_mode((window_width, window_hight))
# Création d'un nom pour notre fenêtre de jeu. J'ai mis le nom de mon jeu.
pygame.display.set_caption("FlappyMan")
# Horloge de pygame
horloge = pygame.time.Clock()

shwarzy_picture = pygame.image.load('image/muscle.png')
cloud_up = pygame.image.load('image/NuageBas.png')
cloud_down = pygame.image.load('image/NuageHaut.png')

pygame.display.flip()

# Musique du jeu
pygame.mixer.music.load("musique/Power Bots Loop.wav")
pygame.mixer.music.play(-1)


def score(iterrator):

    _police = pygame.font.Font('font/BradBunR.ttf', 24)
    _texte = _police.render("score : " + str(iterrator), True, (244, 66, 116))
    window.blit(_texte, [10, 0])


def hight_score(hs_iterrator):
    police_hs = pygame.font.Font('font/BradBunR.ttf', 24)
    text_hs = police_hs.render("high score : " + str(hs_iterrator), True, (244, 66, 116))
    window.blit(text_hs, [650, 0])


def cloud_display(x_cloud, y_cloud, space_beetween_cloud):
    # Affichage du 1er haltere. Pour le 1er haltere x et y ont la même valeur
    window.blit(cloud_up, (x_cloud, y_cloud))

    # Ici cela correspond a y + la hauteur du nuage + l'espace pour placer l'haltere en bas.
    window.blit(cloud_down, (x_cloud, y_cloud+cloud_width+space_beetween_cloud))


def play_or_quit():
    # Parcours les event keydown keyup et quit
    for event in pygame.event.get([pygame.KEYDOWN, pygame.KEYUP, pygame.QUIT]):
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        # On utilise le relachement de la touche pour que la personne appuie
        # à nouveau pour continuer et relache à nouveau
        elif event.type == pygame.KEYUP:
            continue
        # Retourne une touche du clavier
        return event.key
    return None


def create_text_object(text, police):
    window_text = police.render(text, True, (244, 66, 116))
    return window_text, window_text.get_rect()


def message(texte):
    # definit une police ainsi que sa taille
    game_over_texte = pygame.font.Font('font/BradBunR.ttf', 150)
    little_text = pygame.font.Font('font/BradBunR.ttf', 30)

    # Ici je met la variable en paramètre (texte) pour me facilité en cas de modification.
    # J'aurais uniquement à modifier la methode game over.
    game_over_texte_window, game_over_texte_rect = create_text_object(texte, game_over_texte)

    # pour centrer et espacer mes 2 messages.
    game_over_texte_rect.center = window_width/2, ((window_hight/2)-50)
    window.blit(game_over_texte_window, game_over_texte_rect)

    little_text_window, little_text_rect = create_text_object("Appuyer sur une touche pour continuer", little_text)
    little_text_rect.center = window_width / 2, ((window_hight / 2) + 50)
    window.blit(little_text_window, little_text_rect)

    # Mise à jour de la fenetre
    pygame.display.update()
    # Temps de latence avant de recommencer le jeu.
    time.sleep(1)

    # tant que la fonction ne renvoie rien
    while play_or_quit() is None:
        # Nombre d'image par seconde correspond a 0 , pour que ce ne soit pas renouveler.
        horloge.tick()
    boucleJeu()


def gameOver(actual_score):
    a = str(actual_score)
    data_score = "C:/Users/MSI-HASSAN/Desktop/FlappyMan/Donnees.sq3"
    connection_data = sqlite3.connect(data_score)
    cursor_connection = connection_data.cursor()
    cursor_connection.execute("SELECT * from membres")
    liste = list(cursor_connection)
    hscore = []

    for i in range(0, len(liste)):
        hscore += liste[i]
    if int(hscore[-1]) < actual_score:
        cursor_connection.execute("INSERT into membres(score) values(?)", (a,))
        connection_data.commit()
        cursor_connection.close()
        connection_data.close()

    message("Perdu!")


def deplacement_image(x, y, image):
    # La méthode blit permet d'ajouter par dessus notre fenetre notre image
    window.blit(image, (x, y))


def boucleJeu():
    # largeur. plus le nombre est élevé plus notre tête sera avancé.
    x = 150
    # Longueur. Plus le nombre est élevé plus notre tête descend
    y = 200
    y_mouvement = 0
    # charge l'image dans la variable imageMuscle
    scharzy_picture = pygame.image.load('image/muscle.png')

    x_cloud = window_width
    # Nombre entier aleatoire pour déterminer position du nuage
    y_cloud = randint(-300, 10)
    space_beetween_cloud = shwarzy_hight*3
    cloud_speed = 6
    score_actuel = 0
    # permet de fermer la fenetre de notre jeu. Boucle de base de notre jeu.
    game_over = False
    while not game_over:

        # Parcours tous les evenement grace au for
        for event in pygame.event.get():

            # Si c'est un evenement de type QUIT on arrete
            if event.type == pygame.QUIT:
                game_over = True

            # Apuuie sur la touche
            if event.type == pygame.KEYDOWN:
                # Fleche haute
                if event.key == pygame.K_UP:
                    # Les moins en y vont vers le haut
                    y_mouvement = -6
                    # Relache la touche
            if event.type == pygame.KEYUP:
                # +6 pour que sa redescende de 6
                y_mouvement = 6

        # pour mettre a jour constamment la position de y en fonction des evenements
        y = y+y_mouvement

        # Rafraichit l'écran pour qu'il prend bien en compte la l'image
        window.blit(background, [0, 0])
        deplacement_image(x, y, scharzy_picture)

        cloud_display(x_cloud, y_cloud, space_beetween_cloud)

        score(score_actuel)
        cur.execute("select * from membres")
        liste = list(cur)
        print(cur)
        print(liste)

        hscore = []
        for i in range(0, len(liste)):
            hscore += liste[i]
        print(hscore)

        hight_score(hscore[-1])

        x_cloud -= cloud_speed

        # Si position actuelle image est supérieur à la hauteur de la fenetre.
        # Point 0 de l'image est tout en haut. On laisse une petite marge du coup.
        if y > window_hight -65 or y < -1:
            gameOver(score_actuel)

        # -1 pour qu'on sort de l'écran , c'est l'axe des x!
        if x_cloud < (-1*cloud_width):
            # On réinitialise la potition du nuage
            x_cloud = window_width
            # Du coup on veut que la position du nuage soit de nouveau placé au pif pour éviter qu'il
            # conserve sa place avant que l'haltere se barre.
            y_cloud = randint(-300, 10)

            # augmenter la difficulté du jeu en fonction du score.
            # Plus le score sera eleve plus la vitesse de defilement du jeu augmenteras.
            if 3 <= score_actuel <= 5:
                cloud_speed = 15
                space_beetween_cloud = shwarzy_hight * 2.7

            if 5 <= score_actuel <= 8:
                cloud_speed = 7
                space_beetween_cloud = shwarzy_hight * 2.6
            if 7 <= score_actuel <= 10:
                cloud_speed = 7.5
                space_beetween_cloud = shwarzy_hight * 2.4
        if (x + shwarzy_width) > x_cloud + 40 and x + 40 < (x_cloud + cloud_width):
            if y + 20 < (y_cloud + cloud_hight) or y + shwarzy_hight > (y_cloud + cloud_hight + space_beetween_cloud + 30):
                gameOver(score_actuel)

        if x_cloud < (x-cloud_width) < x_cloud + cloud_speed+1:
            score_actuel = score_actuel+1

        pygame.display.update()


boucleJeu()
pygame.quit()
quit()

