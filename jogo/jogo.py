import pyxel 
import math
from random import randint
from datetime import datetime


class Jogador:
    def __init__(self):
        self.x = 16   
        self.y = 120  
        self.largura = 16  
        self.altura = 16  
        self.dx = 0  
        self.dy = 0 
        self.esta_pulando = False 
        self.gravidade = 0.2  
        self.velocidade_pulo = -4  
        self.velocidade = 2 
        self.quadro = 1  
        self.velocidade_animacao = 5 
        self.direcao = 1  
        self.esta_se_movendo = False  
        self.tiros = []

    def disparar(self):
        if pyxel.btnp(pyxel.KEY_Z): 
            direcao = 1 if self.direcao == 1 else -1  
            novo_tiro = Tiro(self.x + self.largura // 2, self.y + self.altura // 2, direcao)
            self.tiros.append(novo_tiro)  


    def atualizar(self):
        self.dx = 0  
        self.esta_se_movendo = False  
        self.disparar()  
        for tiro in self.tiros:
            tiro.atualizar()  
        

        if pyxel.btn(pyxel.KEY_LEFT):
            self.dx = -self.velocidade  
            self.direcao = -1  
            self.esta_se_movendo = True  
         
        elif pyxel.btn(pyxel.KEY_RIGHT):
            self.dx = self.velocidade  
            self.direcao = 1  
            self.esta_se_movendo = True  

        # Controle da animação de movimento
        if self.esta_se_movendo:
            self.quadro = (self.quadro + 1) % (3 * self.velocidade_animacao)  # Avança o quadro da animação
        else:
            self.quadro = 0  # Reseta a animação ao parar

        # Pulo
        if pyxel.btnp(pyxel.KEY_SPACE) and not self.esta_pulando:
            self.dy = self.velocidade_pulo  
            self.esta_pulando = True  

        #gravidade
        self.dy += self.gravidade
        self.x += self.dx
        self.y += self.dy

       
        if self.y + self.altura >= 144:  
            self.y = 144 - self.altura  
            self.dy = 0  
            self.esta_pulando = False 

    def desenhar(self, camera_x):
        indice_quadro = (self.quadro // self.velocidade_animacao) % 2 + 1 if self.esta_se_movendo else 0
        sprite_x = indice_quadro * self.largura 
        
        pyxel.blt(
            self.x - camera_x,  
            self.y,  
            0,  
            sprite_x, 
            0,  
            self.largura * self.direcao,  
            self.altura,  
            0,  
        )
        for tiro in self.tiros:
            tiro.desenhar(camera_x) 


class Chao:
    def __init__(self):
        self.x = 0  
        self.y = 144  
        self.velocidade = 1  
        self.largura = 160  
        self.altura = 16 

    def atualizar(self, jogador):  
        if jogador.esta_se_movendo:
            self.x -= self.velocidade 
        if self.x <= -self.largura: 
            self.x += self.largura

    def desenhar(self):
        pyxel.blt(self.x, self.y, 0, 0, 32, self.largura, self.altura, 0)
        pyxel.blt(self.x + self.largura, self.y, 0, 0, 32, self.largura, self.altura, 0)

class Fantasma:

    def __init__(self, x, y, velocidade):
        self.x = x  
        self.y = y  
        self.largura = 16 
        self.altura = 16  
        self.velocidade = velocidade  
        self.base_y = y  
        self.quadro = 0  
        self.velocidade_animacao = 10 


    def atualizar(self):
        self.y = self.base_y + 10 * math.sin(pyxel.frame_count * self.velocidade * 0.1)
        
        self.quadro = (self.quadro + 1) % (3 * self.velocidade_animacao)


    def desenhar(self, camera_x):
        indice_quadro = (self.quadro // self.velocidade_animacao) % 3
        sprite_x = indice_quadro * self.largura  
        
        pyxel.blt(
            self.x - camera_x,  
            self.y, 0,
            sprite_x + 64, 0,
            self.largura, 
            self.altura, 
            0,  
        )


class Moeda:

    def __init__(self, x, y):
        self.x = x  
        self.y = y
        self.largura = 8
        self.altura = 8  
        self.coletada = False


    def desenhar(self, camera_x):
        if not self.coletada:
            pyxel.blt(self.x - camera_x, self.y, 0, 0, 56, self.largura, self.altura, 0)


    def coletar(self, jogador):
        
        if (
            jogador.x + jogador.largura > self.x
            and jogador.x < self.x + self.largura
            and jogador.y + jogador.altura > self.y
            and jogador.y < self.y + self.altura
        ):
            self.coletada = True 


class Tiro:

    def __init__(self, x, y, direcao):
        self.x = x
        self.y = y
        self.largura = 8  
        self.altura = 4  
        self.direcao = direcao  
        self.velocidade = 4  


    def atualizar(self):
        self.x += self.velocidade * self.direcao


    def desenhar(self, camera_x):
        pyxel.rect(self.x - camera_x, self.y, self.largura, self.altura, pyxel.COLOR_RED)


class Jogo:

    def __init__(self):
        pyxel.init(160, 160, title="Pink Ball ADVENTURES")
        pyxel.load("kirby.pyxres")  
        self.nome_jogador = "" 
        self.jogador = Jogador()  
        self.chao = Chao() 
        self.fantasmas = [
            Fantasma(randint(80, 90), randint(70, 160), 1),
            Fantasma(randint(100, 120), randint(70, 180), 1),
            Fantasma(randint(100, 250), randint(60, 120), 1),
            Fantasma(randint(100, 200), randint(60, 120), 1),
            Fantasma(randint(205, 225), randint(60, 120), 1),
            Fantasma(randint(200, 350), randint(60, 120), 1),
            Fantasma(randint(400, 420), randint(60, 120), 1),
            Fantasma(randint(450, 480), randint(60, 120), 1),
            Fantasma(randint(500, 510), randint(60, 120), 1),
            Fantasma(randint(515, 530), randint(60, 120), 1),
            Fantasma(randint(550, 570), randint(60, 120), 1),
            Fantasma(randint(580, 600), randint(60, 120), 1),
            Fantasma(randint(610, 650), randint(60, 120), 1),
            Fantasma(randint(700, 800), randint(60, 120), 1)]
        
        self.fantasmas.extend([

            Fantasma(randint(800, 900), randint(60, 120), 1),
            Fantasma(randint(900, 1000), randint(60, 120), 1),
            Fantasma(randint(1000, 1100), randint(60, 120), 1),
            Fantasma(randint(1100, 1200), randint(60, 120), 1),
            Fantasma(randint(1200, 1300), randint(60, 120), 1),
            Fantasma(randint(1300, 1400), randint(60, 120), 1),
            Fantasma(randint(1400, 1500), randint(60, 120), 1),
            Fantasma(randint(1500, 1600), randint(60, 120), 1),
            Fantasma(randint(1600, 1700), randint(60, 120), 1),
            Fantasma(randint(1700, 1800), randint(60, 120), 1),
            Fantasma(randint(1800, 1900), randint(60, 120), 1),
            Fantasma(randint(1900, 2000), randint(60, 120), 1),
            Fantasma(randint(2000, 2100), randint(60, 120), 1),
            Fantasma(randint(2100, 2200), randint(60, 120), 1),
            Fantasma(randint(2200, 2300), randint(60, 120), 1),
            Fantasma(randint(2300, 2400), randint(60, 120), 1),
            Fantasma(randint(2400, 2500), randint(60, 120), 1),
            Fantasma(randint(2500, 2600), randint(60, 120), 1),
            Fantasma(randint(2600, 2700), randint(60, 120), 1),
            Fantasma(randint(2700, 2800), randint(60, 120), 1),
            Fantasma(randint(2800, 2900), randint(60, 120), 1),
            Fantasma(randint(2900, 3000), randint(60, 120), 1)])
        
        self.moedas = [
            Moeda(randint(50, 3000), randint(80, 140)) for _ in range(50)]
        self.camera_x = 0  
        self.vidas = 3  
        self.pontuacao = 0 
        self.ranking = []
        self.tempo_inicio = None  
        self.estado = "menu"  
        pyxel.run(self.atualizar, self.desenhar)

    # Organizar pois ainda não esta bom.
    def atualizar_vitoria(self):
            if self.pontuacao >= 20:
            # Verifica se o jogador já existe no ranking
                jogador_existente = next((item for item in self.ranking if item[0] == self.nome_jogador), None)
                if jogador_existente:
                # Atualiza a pontuação e a data, caso a pontuação atual seja maior
                    if self.pontuacao > jogador_existente[1]:
                        jogador_existente[1] = self.pontuacao
                        jogador_existente[2] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                else:
                # Adiciona um novo jogador ao ranking
                    self.ranking.append([self.nome_jogador, self.pontuacao, datetime.now().strftime("%d/%m/%Y %H:%M:%S")])

            #  Ordena o ranking por pontuação em ordem decrescente
                self.ranking.sort(key=lambda x: x[1], reverse=True)
                self.ranking = self.ranking[:3]  # Limita o ranking aos 3 melhores
                self.estado = "ranking"  # Muda para a tela de ranking

    def atualizar_ranking(self):
        pyxel.cls(1)
        pyxel.text(40, 20, "Ranking de Pontuação", pyxel.COLOR_WHITE)
        # Exibe os melhores jogadores
        for i, (nome, pontuacao, data) in enumerate(self.ranking):
            pyxel.text(10, 40 + i * 10, f"{i+1}. {nome}: {pontuacao} ({data})", pyxel.COLOR_YELLOW)

        pyxel.text(5, 140, "Pressione 'Q' para iniciar novo jogo", pyxel.COLOR_WHITE)
        pyxel.text(5, 150, "Pressione 'S' para sair do jogo", pyxel.COLOR_WHITE)

        if pyxel.btnp(pyxel.KEY_Q):
            self.reiniciar_jogo()
        elif pyxel.btnp(pyxel.KEY_S):
            pyxel.quit()
    


    def atualizar(self):
        if self.estado == "menu":
            self.atualizar_menu()
        elif self.estado == "jogo":
            self.atualizar_jogo()
        elif self.estado == "gameover":
            self.atualizar_gameover()
        elif self.estado == "vitoria":
            self.atualizar_vitoria()
        elif self.estado == "ranking": 
            self.atualizar_ranking()



    def atualizar_jogo(self):
        if self.tempo_inicio is None: 
            self.tempo_inicio = pyxel.frame_count
        self.jogador.atualizar()
        self.chao.atualizar(self.jogador)
        
        for fantasma in self.fantasmas:
            fantasma.atualizar()
        self.camera_x = self.jogador.x - 16
        
        for moeda in self.moedas:
            moeda.coletar(self.jogador)
            if moeda.coletada and moeda.x != -1:
                self.pontuacao += 1
                moeda.x = -1     
        if self.pontuacao >= 20:
            self.estado = "vitoria"
        
        for fantasma in self.fantasmas:
            if (self.jogador.x + self.jogador.largura > fantasma.x
                and self.jogador.x < fantasma.x + fantasma.largura
                and self.jogador.y + self.jogador.altura > fantasma.y
                and self.jogador.y < fantasma.y + fantasma.altura):
                self.vidas -= 1
                self.jogador.x, self.jogador.y = 16, 120
                
                if self.vidas == 0:
                    self.estado = "gameover"

        for tiro in self.jogador.tiros[:]:
            for fantasma in self.fantasmas[:]:
                if (tiro.x + tiro.largura > fantasma.x
                        and tiro.x < fantasma.x + fantasma.largura
                        and tiro.y + tiro.altura > fantasma.y
                        and tiro.y < fantasma.y + fantasma.altura):
                    self.fantasmas.remove(fantasma)
                    self.jogador.tiros.remove(tiro)
                    break


        self.camera_x = self.jogador.x - 16

    def atualizar_menu(self):
        if len(self.nome_jogador) < 6:
            if pyxel.btnp(pyxel.KEY_BACKSPACE) and len(self.nome_jogador) > 0:
                self.nome_jogador = self.nome_jogador[:-1]
            for tecla in range(pyxel.KEY_A, pyxel.KEY_Z + 1):
                if pyxel.btnp(tecla):
                    self.nome_jogador += chr(tecla)
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.nome_jogador += " "

        if pyxel.btnp(pyxel.KEY_RETURN) and self.nome_jogador:
            self.estado = "jogo"

    def atualizar_jogo(self):
        
        if self.tempo_inicio is None: 
            self.tempo_inicio = pyxel.frame_count  # 
        self.jogador.atualizar()
        self.chao.atualizar(self.jogador)
        
        for fantasma in self.fantasmas:
            fantasma.atualizar()
        self.camera_x = self.jogador.x - 16
       
        for moeda in self.moedas:
            moeda.coletar(self.jogador)
            if moeda.coletada and moeda.x != -1:  
                self.pontuacao += 1
                moeda.x = -1     
        if self.pontuacao >= 20:
            self.estado = "vitoria"
       
        for fantasma in self.fantasmas:
            if (self.jogador.x + self.jogador.largura > fantasma.x
                and self.jogador.x < fantasma.x + fantasma.largura
                and self.jogador.y + self.jogador.altura > fantasma.y
                and self.jogador.y < fantasma.y + fantasma.altura):
                self.vidas -= 1
                self.jogador.x, self.jogador.y = 16, 120
                
                if self.vidas == 0:
                    self.estado = "gameover"
                    self.ranking.append((self.nome_jogador, self.pontuacao))
                    self.ranking.sort(key=lambda x: x[1], reverse=True)
                
        for tiro in self.jogador.tiros[:]:
            for fantasma in self.fantasmas[:]:
                if (tiro.x + tiro.largura > fantasma.x
                    and tiro.x < fantasma.x + fantasma.largura
                    and tiro.y + tiro.altura > fantasma.y
                    and tiro.y < fantasma.y + fantasma.altura):
                    self.fantasmas.remove(fantasma)  
                    self.jogador.tiros.remove(tiro)  
                    break  

        self.camera_x = self.jogador.x - 16
        

    def atualizar_vitoria(self):
        if self.pontuacao >= 20:
            jogador_existente = next((item for item in self.ranking if item[0] == self.nome_jogador), None)
            if jogador_existente:
                if self.pontuacao > jogador_existente[1]:
                    jogador_existente[1] = self.pontuacao
                    jogador_existente[2] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            else:
                self.ranking.append([self.nome_jogador, self.pontuacao, datetime.now().strftime("%d/%m/%Y %H:%M:%S")])

            self.ranking.sort(key=lambda x: x[1], reverse=True)
            self.ranking = self.ranking[:3]
            self.estado = "ranking"


    def atualizar_gameover(self):

        pyxel.text(40, 60, "GAME OVER", pyxel.COLOR_WHITE)
        pyxel.text(40, 80, "Pressione 'S' para sair", pyxel.COLOR_WHITE)

        if pyxel.btnp(pyxel.KEY_S):  
            pyxel.quit() 


    def desenhar(self):

        pyxel.cls(1)

        if self.estado == "menu":
            cores = [pyxel.COLOR_WHITE, pyxel.COLOR_YELLOW, pyxel.COLOR_RED]  # Cores para alternar
            cor_titulo = cores[(pyxel.frame_count // 5) % len(cores)]
            pyxel.text(40, 10, "Pink Ball Adventures", cor_titulo) 
            pyxel.text(40, 40, "Digite seu nome:", pyxel.COLOR_WHITE)
            pyxel.text(40, 60, self.nome_jogador, pyxel.COLOR_YELLOW)

            if self.nome_jogador:
                pyxel.text(40, 80, "Pressione ENTER para jogar!", pyxel.COLOR_WHITE)

        elif self.estado == "jogo":
            if self.tempo_inicio is not None:
                tempo_decorrido = pyxel.frame_count - self.tempo_inicio
                minutos = tempo_decorrido // 60
                segundos = tempo_decorrido % 60
                pyxel.text(70, 10, f"Tempo: {minutos:02}:{segundos:02}", pyxel.COLOR_WHITE)
            self.jogador.desenhar(self.camera_x)
            self.chao.desenhar()
           
            for fantasma in self.fantasmas:
                fantasma.desenhar(self.camera_x)
           
            for moeda in self.moedas:
                moeda.desenhar(self.camera_x)
            pyxel.text(5, 5, f"Pontuação: {self.pontuacao}", pyxel.COLOR_WHITE)
            pyxel.text(5, 15, f"Vidas: {self.vidas}", pyxel.COLOR_WHITE)

        elif self.estado == "gameover":
            pyxel.text(50, 40, "GAME OVER", pyxel.COLOR_RED)
            pyxel.text(50, 60, f"Pontuação: {self.pontuacao}", pyxel.COLOR_WHITE)
            pyxel.text(50, 80, "Pressione 'S' para sair", pyxel.COLOR_WHITE)

        elif self.estado == "ranking":
            pyxel.text(40, 60, "Ranking", pyxel.COLOR_WHITE)
            for i, (nome, pontuacao, data) in enumerate(self.ranking[:5]):
                pyxel.text(5, 80 + i * 10, f"{i+1}. {nome} - {pontuacao} ({data})", pyxel.COLOR_YELLOW)
            pyxel.text(5, 140, "Pressione ENTER ou 'S' para sair", pyxel.COLOR_WHITE)

        pyxel.text(5, 150, "Miria Evangelista - Matricula: 166627", pyxel.COLOR_BLACK)
Jogo()