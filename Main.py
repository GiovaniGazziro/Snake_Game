import pygame
import sys
import time
import datetime
import logging
import random
from math import sqrt
import timeit
import pygame.freetype  # Import the freetype module.
from MongoDAO import MongoDAO


class game():
    velocidade = 18
    def __init__(self):
        self.fruta = None
        self.posicao_self = [100,50]
        self.corpo_cobra = [[200, 200], [210, 200], [220, 200],[230, 200],[240, 200],[250, 200], [260, 200], [270, 200], [280, 200], [290, 200], [300, 200],    ]
        self.self_skin = pygame.Surface((10,10))
        self.self_skin.fill((124,252,0))
        
        self.informacoes_partida = {}
        self.informacoes_comeu_fruta = []   
        self.mongo = MongoDAO()



    def manhattan(self):

        return abs(self.corpo_cobra[0][0] - self.fruta_posicao[0]) + abs(self.corpo_cobra[0][1] - self.fruta_posicao[1])

    def loggar(self):
        lista_frame = []
        lista_frame.extend((self.fruta_posicao[0], self.fruta_posicao[1])) #posicao da fruta
        lista_frame.extend((self.corpo_cobra[0][0], self.corpo_cobra[0][1])) #posicao da cabeca


        lista_frame.extend((600 - self.corpo_cobra[0][0], 600 - self.corpo_cobra[0][1])) #distancia entre cabeca e parede X

        manhattan = self.manhattan()

        if(manhattan == 0):
            lista_frame.extend((manhattan, 1)) #distancia ate a fruta
        else:
            lista_frame.extend((manhattan, 0)) #distancia ate a fruta

        t = self.preve_colisao()
        lista_frame.extend((self.my_direction, self.morte, t[0], t[1], t[2]))

        

        print(lista_frame)
        logging.info(str(lista_frame))
        lista_frame.clear()



    def verifica_colisao_cobra(self, c1, c2):
        return (c1[0] == c2[0]) and (c1[1] == c2[1])

    def respaw_maca(self):
        try:
            p1 = self.corpo_cobra[0][0]
            p2 = self.corpo_cobra[0][1]
                
                #TO HUMANS
                # p1 = p1 + random.randint(10,125)
                # p2 = p2 + random.randint(10,125)

                # if(p1 > 600):
                #     p1 = random.randint(400,570)
                # if(p2 > 600):
                #     p2 = random.randint(400,570)

                #TO IA
            p1 = random.randint(10,590)
            p2 = random.randint(10,590)

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
                if(game.velocidade < 26):
                    game.velocidade += 2
        except:
            print("Unexpected error:", sys.exc_info()[0])
    

    def preve_colisao(self):
        lista = [0,0,0]

        if(self.my_direction == 3):
            morte = (self.corpo_cobra[0][1]-10, self.corpo_cobra[0][1]+10)  


            variavel = (self.corpo_cobra[0][0]-10, self.corpo_cobra[0][1])  
            
            # print("cabeca:"+str(self.corpo_cobra[0]))
            # print("corpo:"+str(self.corpo_cobra[1:]))

            if(variavel[0] == 0):
                lista[0] = 1
            for corpo in self.corpo_cobra[1:]:

                if(variavel == corpo):
                    lista[0] = 1

        
        if(self.my_direction == 2):
            variavel = (self.corpo_cobra[0][0], self.corpo_cobra[0][1]+10)  
            if(variavel[1] == 610):
                lista[0] = 1
            for corpo in self.corpo_cobra[1:]:
                if(variavel == corpo):
                    lista[0] = 1

        if(self.my_direction == 1):
            variavel = (self.corpo_cobra[0][0]+10, self.corpo_cobra[0][1])  
            if(variavel[0] == 610):
                lista[0] = 1
            for corpo in self.corpo_cobra[1:]:
                if(variavel == corpo):
                    lista[0] = 1

        if(self.my_direction == 0):
            variavel = (self.corpo_cobra[0][0], self.corpo_cobra[0][1]-10)  
            if(variavel[1] == 0):
                lista[0] = 1
            for corpo in self.corpo_cobra[1:]:
                if(variavel == corpo):
                    lista[0] = 1




        if((self.corpo_cobra[0][0]+10 > 590) or (self.corpo_cobra[0][0]-10 < 0)): #SE VIRAR DIREITA MORRE
            lista[1] = 1
        if((self.corpo_cobra[0][1]+10 > 590) or (self.corpo_cobra[0][1]-10 < 0)): #SE VIRAR ESQUERDA MORRE
            lista[2] = 1

        return lista[0], lista[1], lista[2]
            

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

    
    def main(self):
        try:
            # print('Enter your name:')
            # nome = input()
            nome = 'teste'
            self.informacoes_partida.update({'Nome':'teste'})
            logging.basicConfig(filename="logfilename.log", level=logging.INFO)


            clock = pygame.time.Clock() #FPS do jogo
            pygame.init()

            size = width, height = 600, 600 #tamanho da tela
            screen = pygame.display.set_mode(size) #instancia a tela
            pygame.display.set_caption("Mongo Snake")

            self.fruta = pygame.Surface((10,10)) #define o tamanho da fruta
            self.fruta.fill((255,0,0)) #define a cor da fruta
            self.fruta_posicao = (-10, -10) #instancia da fruta

            UP = 0
            RIGHT = 1
            DOWN = 2
            LEFT = 3

            self.morte = 0
            self.my_direction = LEFT #direcao inicial
            
                #TO HUMANS
            self.pronto_comer = True

            inicio = timeit.default_timer()

            self.tempo_partida = timeit.default_timer() 
            self.score = 0

                #TO IA
            self.fruta_posicao = self.respaw_maca()


            while True:
                # self.distancia = self.distancia_pontos()
                # print("cabeca: " + str(self.corpo_cobra[0]))
                
                # print("corpo:" + str(self.corpo_cobra[1:]))
                self.loggar()
                clock.tick(25)
                for event in pygame.event.get(): #for principal do jogo
                    if event.type == pygame.QUIT: #fechar o jogo 
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:

                        if(self.my_direction == UP or self.my_direction == DOWN):
                            if event.key == pygame.K_LEFT:
                                self.my_direction = LEFT
                                self.loggar()

                            if event.key == pygame.K_RIGHT:
                                self.my_direction = RIGHT
                                self.loggar()


                        if(self.my_direction == LEFT or self.my_direction == RIGHT):
                            if event.key == pygame.K_UP:
                                self.my_direction = UP
                                self.loggar()

                            if event.key == pygame.K_DOWN:
                                self.my_direction = DOWN                            
                                self.loggar()


                                            
                        if(event.key == pygame.K_c):
                            self.pause(screen)

                        if event.key == pygame.K_BACKSPACE:
                            pygame.quit()
                            sys.exit()

                #andar
                for i in range(len(self.corpo_cobra) - 1, 0, -1):
                    self.corpo_cobra[i] = (self.corpo_cobra[i-1][0], self.corpo_cobra[i-1][1])

                

                #MUDAR A DIRECAO DA COBRA
                if self.my_direction == UP:
                    self.corpo_cobra[0] = (self.corpo_cobra[0][0], self.corpo_cobra[0][1] - 10)
                if self.my_direction == DOWN:
                    self.corpo_cobra[0] = (self.corpo_cobra[0][0], self.corpo_cobra[0][1] + 10)
                if self.my_direction == RIGHT:
                    self.corpo_cobra[0] = (self.corpo_cobra[0][0] + 10, self.corpo_cobra[0][1])
                if self.my_direction == LEFT:
                    self.corpo_cobra[0] = (self.corpo_cobra[0][0] - 10, self.corpo_cobra[0][1])

                # if(self.corpo_cobra[0] == self.fruta_posicao[0]):
                #     self.corpo_cobra[0] = (self.corpo_cobra[0][0] - 10, self.corpo_cobra[0][1])
                
                
                
                
                if(self.corpo_cobra[0] in self.corpo_cobra[1:]): #trombou com o corpo
                    self.morte = 1
                    self.loggar()
                    self.registra_informacoes()
                    game.velocidade=1                    
                    pygame.quit()
                    sys.exit()
                if(self.corpo_cobra[0][0] < 0 or self.corpo_cobra[0][0] > 590): #saiu da tela
                    self.morte = 1
                    self.loggar()
                    self.registra_informacoes()
                    game.velocidade=1                    
                    pygame.quit()
                    sys.exit()

                if(self.corpo_cobra[0][1] < 0 or self.corpo_cobra[0][1] > 590): #saiu da tela
                    self.morte = 1
                    self.loggar()
                    self.registra_informacoes()
                    game.velocidade=1                    
                    pygame.quit()
                    sys.exit()
                    

                screen.fill((255,255,255))

                agora = timeit.default_timer()
                tempo_passado = agora - inicio

                    #TO HUMANS
                # if(tempo_passado > 3.0 and self.pronto_comer == True): #espero 3 segundos para poder comer de novo 
                #     self.pronto_comer = False  
                #     self.fruta_posicao = self.respaw_maca()

                
                screen.blit(self.fruta, self.fruta_posicao) #coloca na tela a fruta
                

                if self.verifica_colisao_cobra(self.corpo_cobra[0], self.fruta_posicao): #comeu a fruta
                    self.loggar()
                    self.regula_velocidade()
                
                    x = self.fruta_posicao[0]
                    y = self.fruta_posicao[1]
                    self.pronto_comer = False

                    self.score += 1
                    self.informacoes_comeu_fruta.append({'x':x, 'y':y, 'tempo_comer':tempo_passado, 'score':self.score})


                    inicio = timeit.default_timer() #reinicio o tempo do cronometro que demorou para comer
                    self.corpo_cobra.append((0,0)) #acrecendo gomo a cobra
                    self.corpo_cobra.append((0,0))

                        #TO HUMANS
                    # self.fruta_posicao = (-10, -10) #jogo a fruta em uma posicao fora da tela para esperar os 3 segundos do respaw
                    
                        #TO IA
                    self.fruta_posicao = self.respaw_maca()

                    self.pronto_comer = True #deixo pronto para comer novamente


                for pos in self.corpo_cobra:
                        screen.blit(self.self_skin, pos) #coloca na tela a cobra


                small_font = pygame.font.SysFont('OpenSans-BoldItalic.ttf', 25)
                text = small_font.render("Score: "+ str(self.score), True, (0,0,0))
                nome_jogando = small_font.render("Jogador: "+ nome, True, (0,0,0))
                
                screen.blit(text, [0,0])
                screen.blit(nome_jogando, [400, 0])




                pygame.display.update()

        except:
            print("Unexpected error:", sys.exc_info())


g = game()
g.main()