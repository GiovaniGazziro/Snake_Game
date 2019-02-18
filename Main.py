import pygame
import sys
import time
import datetime
import random
import timeit
import pygame.freetype  # Import the freetype module.
from MongoDAO import MongoDAO


class game():
    velocidade = 18
    def __init__(self):
        self.fruta = None
        self.posicao_self = [100,50]
        self.corpo_cobra = [[200, 200], [210, 200], [220, 200],[230, 200],[240, 200],[250, 200],[260, 200] ]
        self.self_skin = pygame.Surface((10,10))
        self.self_skin.fill((124,252,0))
        
        self.informacoes_partida = {}
        self.informacoes_comeu_fruta = []   
        self.mongo = MongoDAO()



    try:

        def verifica_colisao_cobra(self, c1, c2):
            return (c1[0] == c2[0]) and (c1[1] == c2[1])

        def on_grid_random(self):
            try:
                p1 = self.corpo_cobra[0][0]
                p2 = self.corpo_cobra[0][1]

                p1 = p1 + random.randint(10,125)
                p2 = p2 + random.randint(10,125)

                if(p1 > 600):
                    p1 = random.randint(400,570)
                if(p2 > 600):
                    p2 = random.randint(400,570)

                p1 = p1//10*10
                p2 = p2//10*10
                
                return (p1, p2)

            except:
                print("Unexpected error:", sys.exc_info()[0])

        def registra_informacoes(self):
            try:
                tempo_vivo = timeit.default_timer() - self.tempo_partida
                self.informacoes_partida.update({'score':self.score, 'tempo_partida':tempo_vivo, 'eat':self.informacoes_comeu_fruta})
                self.mongo.insert_mongo(self.informacoes_partida)


            except:
                print("Unexpected error:", sys.exc_info()[0])
        

        def regula_velocidade(self):
            try:
                    if(self.score == 10):
                        self.self_skin.fill((255, 204, 0))
                    if(game.velocidade < 30):
                        game.velocidade += 2
            except:
                print("Unexpected error:", sys.exc_info()[0])
        



        def pause(self, screen):
            try:
                pause = True
                while pause:
                    small_font = pygame.font.SysFont('OpenSans-BoldItalic.ttf', 55)
                    text = small_font.render("PAUSADO", True, (255,0,0))
                    text2 = small_font.render("P to resume", True, (0,0,0))

                    screen.blit(text, [300,300])
                    screen.blit(text2, [300,330])

                    pygame.display.update()

                    for event in pygame.event.get():
                        if event.key == pygame.K_BACKSPACE:
                            pygame.quit()
                            sys.exit()
                        if(event.key==pygame.K_p):
                            pause = False
                        else:
                            pass


            except Exception as e:
                print("\n")
                print("type error: " + str(e))

        def score(self, screen):
            try:
                pass
                # small_font = pygame.font.SysFont('OpenSans-BoldItalic.ttf', 25)
                # text = small_font.render("Score: "+ str(self.score), True, (0,0,0))
                # screen.blit(text, [0,0])
            except:
                print("Unexpected error:", sys.exc_info()[0])
        def main(self):
            try:
                print('Enter your name:')
                nome = input()
                self.informacoes_partida.update({'Nome':nome})



                clock = pygame.time.Clock() #FPS do jogo
                pygame.init()

                size = width, height = 600, 600 #tamanho da tela
                screen = pygame.display.set_mode(size) #instancia a tela
                pygame.display.set_caption("Mongo Snake")
                # self.score(screen)

                self.fruta = pygame.Surface((10,10)) #define o tamanho da fruta
                self.fruta.fill((255,0,0)) #define a cor da fruta
                self.fruta_posicao = (900,900) #instancia da fruta

                UP = 0
                RIGHT = 1
                DOWN = 2
                LEFT = 3




                my_direction = LEFT #direcao inicial
                self.pronto_comer = True

                inicio = timeit.default_timer()

                self.tempo_partida = timeit.default_timer() 
                self.score = 0


                while True:
                    # self.score(screen)
                    # print(game.velocidade)
                    clock.tick(game.velocidade)

                    for event in pygame.event.get(): #for principal do jogo
                        if event.type == pygame.QUIT: #fechar o jogo 
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.KEYDOWN:

                            if(my_direction == UP or my_direction == DOWN):
                                if event.key == pygame.K_LEFT:
                                    my_direction = LEFT
                                if event.key == pygame.K_RIGHT:
                                    my_direction = RIGHT

                            if(my_direction == LEFT or my_direction == RIGHT):
                                if event.key == pygame.K_UP:
                                    my_direction = UP
                                if event.key == pygame.K_DOWN:
                                    my_direction = DOWN                            


                                                
                            if(event.key == pygame.K_c):
                                self.pause(screen)

                            if event.key == pygame.K_BACKSPACE:
                                pygame.quit()
                                sys.exit()

                    #andar
                    for i in range(len(self.corpo_cobra) - 1, 0, -1):
                        self.corpo_cobra[i] = (self.corpo_cobra[i-1][0], self.corpo_cobra[i-1][1])

                    #MUDAR A DIRECAO DA COBRA
                    if my_direction == UP:
                        self.corpo_cobra[0] = (self.corpo_cobra[0][0], self.corpo_cobra[0][1] - 10)
                    if my_direction == DOWN:
                        self.corpo_cobra[0] = (self.corpo_cobra[0][0], self.corpo_cobra[0][1] + 10)
                    if my_direction == RIGHT:
                        self.corpo_cobra[0] = (self.corpo_cobra[0][0] + 10, self.corpo_cobra[0][1])
                    if my_direction == LEFT:
                        self.corpo_cobra[0] = (self.corpo_cobra[0][0] - 10, self.corpo_cobra[0][1])

                    if(self.corpo_cobra[0] == self.fruta_posicao[0]):
                        self.corpo_cobra[0] = (self.corpo_cobra[0][0] - 10, self.corpo_cobra[0][1])
                    
                    
                    
                    
                    if(self.corpo_cobra[0] in self.corpo_cobra[1:]): #trombou com o corpo
                        self.registra_informacoes()
                        pygame.quit()
                        sys.exit()
                    if(self.corpo_cobra[0][0] < 0 or self.corpo_cobra[0][0] > size[0]): #saiu da tela
                        self.registra_informacoes()
                        pygame.quit()
                        sys.exit()

                    if(self.corpo_cobra[0][1] < 0 or self.corpo_cobra[0][1] > size[0]): #saiu da tela
                        self.registra_informacoes()
                        pygame.quit()
                        sys.exit()
                        

                    screen.fill((255,255,255))

                    agora = timeit.default_timer()
                    tempo_passado = agora - inicio
                    # print(tempo_passado)
                    if(tempo_passado > 3.0 and self.pronto_comer == True): #espero 3 segundos para poder comer de novo 
                        self.pronto_comer = False  
                        # inicio = timeit.default_timer()
                        self.fruta_posicao = self.on_grid_random()

                    
                    screen.blit(self.fruta, self.fruta_posicao) #coloca na tela a fruta
                    

                    if self.verifica_colisao_cobra(self.corpo_cobra[0], self.fruta_posicao): #comeu a fruta
                        self.regula_velocidade()
                    
                        x = self.fruta_posicao[0]
                        y = self.fruta_posicao[1]
                        self.score += 1
                        self.informacoes_comeu_fruta.append({'x':x, 'y':y, 'tempo_comer':tempo_passado, 'score':self.score})

                        inicio = timeit.default_timer() #reinicio o tempo do cronometro que demorou para comer
                        self.corpo_cobra.append((0,0)) #acrecendo gomo a cobra
                        self.corpo_cobra.append((0,0))
                        self.fruta_posicao = (700,700) #jogo a fruta em uma posicao fora da tela para esperar os 3 segundos do respaw
                        self.pronto_comer = True #deixo pronto para comer novamente


                    for pos in self.corpo_cobra:
                            screen.blit(self.self_skin, pos) #coloca na tela a cobra


                    small_font = pygame.font.SysFont('OpenSans-BoldItalic.ttf', 25)
                    text = small_font.render("Score: "+ str(self.score), True, (0,0,0))
                    screen.blit(text, [0,0])
                    pygame.display.update()

            except SystemExit:
                pass
            except:
                print("Unexpected error:", sys.exc_info()[0])


    except:
        print("Unexpected error:", sys.exc_info()[0])


g = game()
g.main()