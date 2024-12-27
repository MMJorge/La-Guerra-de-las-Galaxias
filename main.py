import pygame
import random
import math
from pygame import mixer

# Inicializar a pygame
pygame.init()

#Crear la pantalla
pantalla = pygame.display.set_mode([800,600])

#Título e ícono
pygame.display.set_caption('La guerra de las galaxias')
icono_ovni = pygame.image.load('ovni.png')
pygame.display.set_icon(icono_ovni)
fondo = pygame.image.load('digital-world-banner-background-remixed-from-public-domain-by-nasa.jpg')

#agregar música
mixer.music.load('battle-station-155353.mp3')
mixer.music.set_volume(0.01)
mixer.music.play(-1)


#Variables del Jugador
img_protagonista = pygame.image.load('estrella.png')
protagonista_x = 368
protagonista_y = 500
protagonista_x_cambio = 0

#Variables del Enemigo
img_enemigo = []
enemigo_x = []
enemigo_y = []
enemigo_x_cambio = []
enemigo_y_cambio = []
cantidad_enemigos = 8

for e in range(cantidad_enemigos):
    img_enemigo.append(pygame.image.load('enemigo.png'))
    enemigo_x.append(random.randint(0,736))
    enemigo_y.append(random.randint(50,200))
    enemigo_x_cambio.append(0.3)
    enemigo_y_cambio.append(50)

#Variables del Enemigo
balas = []
img_bala = pygame.image.load('bala.png')
bala_x = 0
bala_y = 500
bala_x_cambio = 0
bala_y_cambio = 1
bala_visible = False


#Puntacion
puntuacion = 0
fuente = pygame.font.Font('freesansbold.ttf',25)
texto_x = 10
texto_y = 10

#Texto final de juego
fuente_final =pygame.font.Font('freesansbold.ttf', 40)

def texto_final():
    mi_fuente_final = fuente_final.render("Game Over", True, (255,255,255))
    pantalla.blit(mi_fuente_final,(60,200))


#Funcion mostrar puntuacion
def mostrar_puntuacion(x,y):
    texto = fuente.render(f"Puntuación: {puntuacion}", True,(255,255,255))
    pantalla.blit(texto, (x,y))

#Funcion jugador
def jugador(x,y):
    pantalla.blit(img_protagonista,[x,y])

#Funcion enemigo
def enemigo(x,y,ene):
    pantalla.blit(img_enemigo[ene],[x,y])

#Funcion disparar bala
def disparar_bala(x,y):
    global bala_visible
    bala_visible = True
    pantalla.blit(img_bala,(x + 16,y + 10))

#Funcion colisiones
def hay_colision(x_1,y_1,x_2,y_2):
    distancia = math.sqrt(math.pow(x_1 - x_2,2) + math.pow(y_2 - y_1,2))
    if distancia < 27:
        return True
    else:
        False

#Loop del juego
se_ejecuta = True
while se_ejecuta:

    #imagen de fondo
    pantalla.blit(fondo,(0,0))

    #Iterar eventos
    for evento in pygame.event.get():

        #Evento cerrar
        if evento.type == pygame.QUIT:
            se_ejecuta = False

        #Evento presionar teclas
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                protagonista_x_cambio = -0.3
            if evento.key == pygame.K_RIGHT:
                protagonista_x_cambio = 0.3
            if evento.key == pygame.K_SPACE:
                sonido_bala = mixer.Sound('mouse-click-153941.mp3')
                sonido_bala.play()
                nueva_bala = {"x": protagonista_x, "y" : protagonista_y, "velocidad": -5}
                balas.append(nueva_bala)
                if not bala_visible:
                    bala_x = protagonista_x
                    disparar_bala(bala_x,bala_y)

        #Evento soltar flechas
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                protagonista_x_cambio = 0

    #Modificar ubicacion del protagonista
    protagonista_x += protagonista_x_cambio

    #Mantener dentro de bordes al protagonista
    if protagonista_x <= 0 :
        protagonista_x = 0
    if protagonista_x >= 736:
        protagonista_x = 736

    #Modificar ubicacion del enemigo
    for e in range(cantidad_enemigos):

        #FIn del juego
        if enemigo_y[e] > 450:
            for k in range(cantidad_enemigos):
                enemigo_y[k] = 1000
            texto_final()
            break

        enemigo_x[e] += enemigo_x_cambio[e]

        #Mantener dentro de bordes al enemigo
        if enemigo_x[e] <= 0 :
            enemigo_x_cambio[e] = 0.3
            enemigo_y[e] += enemigo_y_cambio[e]
        elif enemigo_x[e] >= 736:
            enemigo_x_cambio[e] = -0.3
            enemigo_y[e] += enemigo_y_cambio[e]

        #Colision
        for bala in balas:
            colision_bala_enemigo = hay_colision(enemigo_x[e],enemigo_y[e],bala["x"],bala["y"])
            if colision_bala_enemigo:
                sonido_colision = mixer.Sound('metal-click-145553.mp3')
                sonido_colision.play()
                balas.remove(bala)
                puntuacion += 1
                enemigo_x[e] = random.randint(0, 736)
                enemigo_y[e] = random.randint(50, 200)

        enemigo(enemigo_x[e], enemigo_y[e],e)

    #Movimiento bala
    for bala in balas:
        bala["y"] += bala["velocidad"]
        pantalla.blit(img_bala, (bala["x"] + 16, bala["y"] + 10))
        if bala["y"] < 0:
            balas.remove(bala)

    if bala_y <= -32:
        bala_y = 500
        bala_visible = False

    if bala_visible:
        disparar_bala(bala_x,bala_y)
        bala_y -= bala_y_cambio

    jugador(protagonista_x,protagonista_y)
    mostrar_puntuacion(texto_x,texto_y)

    #Actualizar
    pygame.display.update()
