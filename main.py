"""Ejecuta con: python main.py (requiere pygame)."""

import math
import os

os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

import pygame

from modelo import ALTO, ANCHO, DURACION, Partida
from tema_halloween import (
    BLANCO, BORDE, FONDO, GRIS, NARANJA, ORO, PANEL, ROJO, VERDE,
    TemaHalloween,
)


class Juego:
    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("Coin Hunter 2D · Noche de Halloween")
        self.tema = TemaHalloween()
        icono = pygame.Surface((40, 40), pygame.SRCALPHA)
        self.tema.calabaza(icono, 20, 22, 1.2)
        pygame.display.set_icon(icono)
        self.reloj = pygame.time.Clock()
        self.fuentes = {
            "pequena": pygame.font.SysFont("segoeui", 16),
            "normal": pygame.font.SysFont("segoeui", 21),
            "media": pygame.font.SysFont("segoeui", 29, bold=True),
            "titulo": pygame.font.SysFont("segoeui", 52, bold=True),
        }
        self.estado = "inicio"
        self.nombre = ""
        self.error = ""
        self.partida = None
        self.ejecutando = True
        self.boton_principal = pygame.Rect(230, 409, 340, 52)
        self.boton_secundario = pygame.Rect(230, 475, 340, 40)
        pygame.key.start_text_input()

    def texto(self, contenido, x, y, color=BLANCO, fuente="normal", centro=False):
        superficie = self.fuentes[fuente].render(str(contenido), True, color)
        rect = superficie.get_rect()
        if centro:
            rect.midtop = (x, y)
        else:
            rect.topleft = (x, y)
        self.pantalla.blit(superficie, rect)

    def boton(self, rect, etiqueta, secundario=False):
        hover = rect.collidepoint(pygame.mouse.get_pos())
        color = BORDE if secundario else NARANJA
        if hover:
            color = (112, 78, 138) if secundario else (255, 186, 99)
        pygame.draw.rect(self.pantalla, (13, 8, 23), rect.move(0, 4), border_radius=12)
        pygame.draw.rect(self.pantalla, color, rect, border_radius=12)
        self.texto(
            etiqueta, rect.centerx, rect.y + (7 if secundario else 12),
            BLANCO if secundario else FONDO, centro=True,
        )

    def comenzar(self):
        try:
            self.partida = Partida(self.nombre)
        except ValueError as error:
            self.error = str(error)
            return
        self.estado = "jugando"
        self.error = ""
        pygame.key.stop_text_input()

    def volver_inicio(self):
        self.estado = "inicio"
        self.error = ""
        pygame.key.start_text_input()

    def eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.ejecutando = False
            elif evento.type == pygame.WINDOWFOCUSLOST:
                if self.estado == "jugando":
                    self.partida.pausada = True
            elif evento.type == pygame.TEXTINPUT and self.estado == "inicio":
                entrada = "".join(c for c in evento.text if c.isprintable())
                self.nombre = (self.nombre + entrada)[:50]
                self.error = ""
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    if self.estado == "jugando":
                        self.partida.alternar_pausa()
                    else:
                        self.ejecutando = False
                elif self.estado == "inicio":
                    if evento.key == pygame.K_BACKSPACE:
                        self.nombre = self.nombre[:-1]
                    elif evento.key == pygame.K_RETURN:
                        self.comenzar()
                elif self.estado == "jugando" and evento.key == pygame.K_p:
                    self.partida.alternar_pausa()
                elif self.estado == "resultado":
                    if evento.key in (pygame.K_RETURN, pygame.K_r):
                        self.comenzar()
                    elif evento.key == pygame.K_n:
                        self.volver_inicio()
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if self.estado in ("inicio", "resultado"):
                    if self.boton_principal.collidepoint(evento.pos):
                        self.comenzar()
                    elif self.estado == "resultado" and self.boton_secundario.collidepoint(evento.pos):
                        self.volver_inicio()

    def fondo(self):
        self.tema.fondo(self.pantalla, pygame.time.get_ticks() / 1000)

    def moneda(self, x, y):
        self.tema.dulce(self.pantalla, x, y)

    def bomba(self, x, y):
        self.tema.bomba(self.pantalla, x, y)

    def inicio(self):
        self.texto("TRUCO, TRATO... ¡Y MUCHOS DULCES!", 400, 60, NARANJA, "pequena", True)
        self.texto("Coin Hunter", 400, 91, fuente="titulo", centro=True)
        self.texto("Atrapa dulces. ¡Cuidado con las bombas!", 400, 159, GRIS, centro=True)
        pygame.draw.rect(self.pantalla, PANEL, (150, 220, 500, 280), border_radius=20)
        pygame.draw.rect(self.pantalla, BORDE, (150, 220, 500, 280), 1, border_radius=20)
        self.texto("¿Cómo te llamas?", 230, 248, fuente="media")
        campo = pygame.Rect(230, 300, 340, 53)
        pygame.draw.rect(self.pantalla, FONDO, campo, border_radius=10)
        pygame.draw.rect(self.pantalla, NARANJA, campo, 1, border_radius=10)
        # Conserva hasta 50 caracteres y muestra el final si no caben en el campo.
        visible = self.nombre
        while self.fuentes["normal"].size(visible)[0] > campo.width - 34:
            visible = visible[1:]
        self.texto(visible or "Escribe tu nombre", 246, 312, BLANCO if visible else GRIS)
        if pygame.time.get_ticks() % 1000 < 500:
            cursor_x = 246 + self.fuentes["normal"].size(visible)[0]
            pygame.draw.line(self.pantalla, NARANJA, (cursor_x, 312), (cursor_x, 338), 2)
        if self.error:
            self.texto(self.error, 400, 367, ROJO, "pequena", True)
        else:
            self.texto("45 segundos · 3 vidas · 10 puntos por dulce", 400, 367, GRIS, "pequena", True)
        self.boton(self.boton_principal, "¡Dulce o travesura!  →")
        self.texto("← → o A / D: moverse     P: pausa     Enter: comenzar", 400, 530, GRIS, "pequena", True)

    def tablero(self):
        partida = self.partida
        pygame.draw.rect(self.pantalla, PANEL, (16, 16, 768, 75), border_radius=16)
        self.texto("PUNTOS", 36, 27, GRIS, "pequena")
        self.texto(f"{partida.puntuacion:03}", 36, 46, ORO, "media")
        self.texto("VIDAS", 215, 27, GRIS, "pequena")
        for i in range(3):
            self.tema.calabaza(self.pantalla, 227 + i * 28, 66, 0.65, apagada=i >= partida.vidas)
        self.texto("TIEMPO", 410, 27, GRIS, "pequena")
        self.texto(f"{math.ceil(partida.restante):02}s", 410, 46, VERDE, "media")
        nombre = partida.nombre_jugador
        while self.fuentes["pequena"].size(nombre)[0] > 190:
            nombre = nombre[:-2] + "…"
        self.texto(nombre, 580, 33, fuente="pequena")
        self.texto("P / Esc: pausa", 580, 57, GRIS, "pequena")
        pygame.draw.rect(self.pantalla, BORDE, (16, 98, 768, 3), border_radius=1)
        pygame.draw.rect(self.pantalla, VERDE, (16, 98, round(768 * partida.restante / DURACION), 3))
        for objeto in partida.objetos:
            centro = (round(objeto.x + objeto.ancho / 2), round(objeto.y + objeto.alto / 2))
            if objeto.tipo == "moneda":
                self.moneda(*centro)
            else:
                self.bomba(*centro)
        if not partida.inmune or pygame.time.get_ticks() % 160 < 80:
            cuerpo = pygame.Rect(round(partida.jugador_x), partida.jugador_y, partida.jugador_ancho, partida.jugador_alto)
            self.tema.fantasma(self.pantalla, cuerpo)
        pygame.draw.line(self.pantalla, BORDE, (16, ALTO - 34), (ANCHO - 16, ALTO - 34))
        self.texto("← → / A D   MOVERSE", 28, ALTO - 26, GRIS, "pequena")
        self.texto("DULCE +10     BOMBA −1 VIDA", 490, ALTO - 26, GRIS, "pequena")
        if partida.pausada:
            velo = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
            velo.fill((14, 8, 26, 225))
            self.pantalla.blit(velo, (0, 0))
            self.tema.calabaza(self.pantalla, 400, 200, 1.6)
            self.texto("Pausa embrujada", 400, 235, fuente="titulo", centro=True)
            self.texto("Pulsa P o Esc para continuar", 400, 315, GRIS, centro=True)

    def resultado(self):
        partida = self.partida
        self.texto("¡SOBREVIVISTE A LA NOCHE!" if partida.vidas else "¡LAS BOMBAS TE ASUSTARON!", 400, 65, NARANJA, "pequena", True)
        self.texto("Fin de la cacería", 400, 96, fuente="titulo", centro=True)
        pygame.draw.rect(self.pantalla, PANEL, (150, 195, 500, 335), border_radius=20)
        pygame.draw.rect(self.pantalla, BORDE, (150, 195, 500, 335), 1, border_radius=20)
        self.texto("TU PUNTUACIÓN", 400, 223, GRIS, "pequena", True)
        self.texto(partida.puntuacion, 400, 248, ORO, "titulo", True)
        self.texto(f"Dulces recogidos: {partida.puntuacion // 10}", 400, 326, centro=True)
        self.texto("Esta versión todavía no guarda las partidas.", 400, 368, GRIS, "pequena", True)
        self.boton(self.boton_principal, "Volver a jugar  ·  Enter")
        self.boton(self.boton_secundario, "Cambiar jugador  ·  N", secundario=True)
        self.texto("Esc: salir", 400, 550, GRIS, "pequena", True)

    def ejecutar(self):
        try:
            while self.ejecutando:
                # Limita saltos grandes después de arrastrar o minimizar la ventana.
                dt = min(self.reloj.tick(60) / 1000, 0.05)
                self.eventos()
                if not self.ejecutando:
                    break
                if self.estado == "jugando":
                    teclas = pygame.key.get_pressed()
                    direccion = int(teclas[pygame.K_RIGHT] or teclas[pygame.K_d]) - int(teclas[pygame.K_LEFT] or teclas[pygame.K_a])
                    self.partida.actualizar(dt, direccion)
                    if self.partida.terminada:
                        self.estado = "resultado"
                self.fondo()
                if self.estado == "inicio":
                    self.inicio()
                elif self.estado == "jugando":
                    self.tablero()
                else:
                    self.resultado()
                pygame.display.flip()
        finally:
            pygame.quit()

if __name__ == "__main__":
    Juego().ejecutar()