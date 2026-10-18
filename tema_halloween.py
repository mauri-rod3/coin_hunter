import math

import pygame

from modelo import ALTO, ANCHO

FONDO = (18, 12, 31)
PANEL = (36, 24, 53)
BORDE = (88, 61, 110)
BLANCO = (250, 237, 220)
GRIS = (190, 172, 205)
NARANJA = (250, 158, 66)
ORO = (255, 211, 115)
ROJO = (249, 112, 131)
VERDE = (190, 218, 126)


class TemaHalloween:
    """Prepara una vez el escenario y anima detalles pequeños en cada fotograma."""

    def __init__(self):
        self.escenario = pygame.Surface((ANCHO, ALTO)).convert()
        self._crear_escenario()

    @staticmethod
    def _murcielago(superficie, x, y, escala, aleteo=0):
        puntos = [
            (-16, -5 - aleteo), (-8, -2), (-3, 1), (-2, -4),
            (0, -2), (2, -4), (3, 1), (8, -2), (16, -5 - aleteo),
            (12, 5), (7, 2), (3, 6), (0, 4), (-3, 6), (-7, 2), (-12, 5),
        ]
        pygame.draw.polygon(
            superficie, (12, 9, 25),
            [(round(x + px * escala), round(y + py * escala)) for px, py in puntos],
        )

    @staticmethod
    def _arbol(superficie, x, base, alto, espejo=1):
        color = (16, 12, 30)
        cima = base - alto
        pygame.draw.polygon(superficie, color, [
            (x - 12, base), (x - 5, cima + 43), (x + 6, cima),
            (x + 2, cima + 105), (x + 14, base),
        ])
        for origen, destino, ancho in [
            ((x, cima + 90), (x - 48 * espejo, cima + 47), 8),
            ((x - 48 * espejo, cima + 47), (x - 52 * espejo, cima + 12), 4),
            ((x - 31 * espejo, cima + 62), (x - 72 * espejo, cima + 42), 4),
            ((x + 2, cima + 132), (x + 46 * espejo, cima + 82), 7),
            ((x + 46 * espejo, cima + 82), (x + 41 * espejo, cima + 45), 4),
            ((x + 32 * espejo, cima + 98), (x + 69 * espejo, cima + 85), 4),
        ]:
            pygame.draw.line(superficie, color, origen, destino, ancho)

    @staticmethod
    def calabaza(superficie, x, y, tamano=1.0, apagada=False):
        """Linterna decorativa; se reutiliza en el indicador de vidas."""
        ancho = max(8, round(27 * tamano))
        alto = max(7, round(21 * tamano))
        cuerpo = pygame.Rect(x - ancho // 2, y - alto // 2, ancho, alto)
        color = BORDE if apagada else (225, 113, 41)
        pygame.draw.ellipse(superficie, color, cuerpo)
        for desplazamiento in (-0.22, 0.22):
            surco = cuerpo.inflate(-round(ancho * 0.55), 0)
            surco.centerx = x + round(ancho * desplazamiento)
            pygame.draw.ellipse(superficie, (65, 43, 83) if apagada else (177, 75, 34), surco, 1)
        pygame.draw.line(superficie, (105, 120, 66), (x, cuerpo.top + 1), (x + 2, cuerpo.top - 4), 3)
        brillo = (105, 80, 124) if apagada else ORO
        for signo in (-1, 1):
            ojo_x = x + signo * ancho * 0.21
            pygame.draw.polygon(superficie, brillo, [
                (round(ojo_x), round(y - alto * 0.22)),
                (round(ojo_x - ancho * 0.10), round(y)),
                (round(ojo_x + ancho * 0.10), round(y)),
            ])
        pygame.draw.lines(superficie, brillo, False, [
            (x - ancho // 4, y + alto // 5), (x, y + alto // 3),
            (x + ancho // 4, y + alto // 5),
        ], max(1, round(tamano * 2)))

    def _crear_escenario(self):
        fondo = self.escenario
        for y in range(ALTO):
            mezcla = y / ALTO
            color = (round(22 + 18 * mezcla), round(14 + 9 * mezcla), round(42 + 14 * mezcla))
            pygame.draw.line(fondo, color, (0, y), (ANCHO, y))

        # Semillas visuales fijas: el fondo no altera el azar de las partidas.
        for i in range(65):
            x, y = (i * 131 + 29) % ANCHO, (i * 67 + 18) % 390
            pygame.draw.circle(fondo, (112, 86, 139), (x, y), 1)

        halo = pygame.Surface((220, 220), pygame.SRCALPHA)
        for radio, opacidad in [(104, 9), (85, 12), (67, 17)]:
            pygame.draw.circle(halo, (*NARANJA, opacidad), (110, 110), radio)
        fondo.blit(halo, (554, 36))
        pygame.draw.circle(fondo, (241, 191, 113), (664, 146), 48)
        for x, y, radio in [(645, 126, 8), (683, 153, 11), (653, 171, 5)]:
            pygame.draw.circle(fondo, (215, 157, 91), (x, y), radio)

        pygame.draw.polygon(fondo, (41, 29, 58), [
            (0, 410), (100, 341), (210, 392), (355, 325),
            (490, 391), (605, 335), (800, 409), (800, ALTO), (0, ALTO),
        ])
        # Casa embrujada al fondo, con ventanas encendidas.
        casa = (26, 19, 41)
        pygame.draw.rect(fondo, casa, (594, 325, 139, 153))
        pygame.draw.polygon(fondo, casa, [(578, 332), (664, 267), (747, 332)])
        pygame.draw.rect(fondo, casa, (608, 272, 29, 70))
        pygame.draw.polygon(fondo, casa, [(602, 277), (622, 248), (643, 277)])
        for x, y in [(615, 350), (680, 350), (615, 399), (680, 399)]:
            pygame.draw.rect(fondo, (162, 101, 66), (x, y, 15, 23), border_radius=6)
            pygame.draw.line(fondo, casa, (x + 7, y), (x + 7, y + 23), 2)
        pygame.draw.rect(fondo, (17, 13, 30), (650, 423, 25, 55), border_radius=12)

        self._arbol(fondo, 57, 566, 305)
        self._arbol(fondo, 766, 566, 275, -1)
        pygame.draw.ellipse(fondo, (23, 17, 36), (-140, 487, 1080, 270))
        for x, y, ancho in [(109, 481, 29), (176, 512, 24), (670, 499, 30), (720, 523, 22)]:
            tumba = pygame.Rect(x, y, ancho, 47)
            pygame.draw.rect(fondo, (58, 45, 71), tumba, border_top_left_radius=14, border_top_right_radius=14)
            pygame.draw.line(fondo, (91, 71, 104), (x + ancho // 2, y + 12), (x + ancho // 2, y + 31), 2)
            pygame.draw.line(fondo, (91, 71, 104), (x + 7, y + 20), (x + ancho - 7, y + 20), 2)

        for x, y, tamano in [(36, 550, 1.3), (81, 553, 0.8), (735, 551, 1.1), (775, 550, 0.85)]:
            self.calabaza(fondo, x, y, tamano)

        # Telarañas de las esquinas.
        for esquina, signo in [(0, 1), (ANCHO - 1, -1)]:
            for dx, dy in [(80, 0), (68, 32), (45, 60), (0, 83)]:
                pygame.draw.line(fondo, (75, 57, 94), (esquina, 0), (esquina + dx * signo, dy), 1)
            for escala in (0.35, 0.65, 1):
                puntos = [(round(esquina + dx * signo * escala), round(dy * escala)) for dx, dy in [(80, 0), (68, 32), (45, 60), (0, 83)]]
                pygame.draw.lines(fondo, (75, 57, 94), False, puntos, 1)

    def fondo(self, pantalla, segundos):
        pantalla.blit(self.escenario, (0, 0))
        for i, (x, y, escala) in enumerate([(165, 148, 1), (531, 198, 0.7), (713, 228, 0.8)]):
            self._murcielago(pantalla, x + math.sin(segundos * 0.7 + i) * 12, y, escala, math.sin(segundos * 3 + i) * 3)
        niebla = pygame.Surface((ANCHO, 52), pygame.SRCALPHA)
        for i in range(5):
            x = round((i * 200 + segundos * 8) % (ANCHO + 180)) - 150
            pygame.draw.ellipse(niebla, (140, 113, 163, 12), (x, i % 2 * 10, 220, 29))
        pantalla.blit(niebla, (0, 503))

    @staticmethod
    def dulce(pantalla, x, y):
        pygame.draw.polygon(pantalla, (179, 128, 219), [(x - 14, y - 7), (x - 5, y), (x - 14, y + 7)])
        pygame.draw.polygon(pantalla, (179, 128, 219), [(x + 14, y - 7), (x + 5, y), (x + 14, y + 7)])
        pygame.draw.circle(pantalla, (174, 82, 37), (x, y + 2), 10)
        pygame.draw.circle(pantalla, NARANJA, (x, y), 10)
        pygame.draw.arc(pantalla, (255, 235, 181), (x - 6, y - 6, 12, 12), 0, math.pi * 1.5, 2)
        pygame.draw.circle(pantalla, ORO, (x, y), 3)

    @staticmethod
    def bomba(pantalla, x, y):
        pygame.draw.line(pantalla, ORO, (x + 3, y - 11), (x + 8, y - 18), 3)
        pygame.draw.circle(pantalla, ROJO, (x + 9, y - 19), 3)
        pygame.draw.circle(pantalla, (21, 15, 32), (x, y), 14)
        pygame.draw.circle(pantalla, (160, 98, 173), (x, y), 14, 2)
        for signo in (-1, 1):
            pygame.draw.polygon(pantalla, NARANJA, [(x + signo * 3, y - 5), (x + signo * 9, y - 2), (x + signo * 3, y + 1)])
        pygame.draw.lines(pantalla, ROJO, False, [(x - 6, y + 5), (x - 3, y + 8), (x, y + 5), (x + 3, y + 8), (x + 6, y + 5)], 2)

    @staticmethod
    def fantasma(pantalla, cuerpo):
        """El dibujo permanece dentro del rectángulo de colisión del jugador."""
        x, y, ancho, alto = cuerpo
        pygame.draw.ellipse(pantalla, (12, 8, 22), (x + 3, y + alto - 5, ancho - 6, 5))
        pygame.draw.rect(pantalla, (234, 225, 247), (x + 4, y, ancho - 8, alto - 6), border_radius=16)
        pygame.draw.polygon(pantalla, (234, 225, 247), [
            (x + 4, y + 18), (x + ancho - 4, y + 18), (x + ancho - 4, y + alto - 1),
            (x + ancho - 14, y + alto - 7), (x + ancho - 23, y + alto - 1),
            (x + 32, y + alto - 7), (x + 22, y + alto - 1), (x + 13, y + alto - 7), (x + 4, y + alto - 1),
        ])
        for dx in (22, 42):
            pygame.draw.ellipse(pantalla, FONDO, (x + dx - 3, y + 9, 7, 9))
            pygame.draw.circle(pantalla, BLANCO, (x + dx - 1, y + 11), 1)
        pygame.draw.ellipse(pantalla, (149, 99, 173), (x + 29, y + 20, 6, 5))
        pygame.draw.circle(pantalla, (239, 172, 167), (x + 15, y + 20), 3)
        pygame.draw.circle(pantalla, (239, 172, 167), (x + 49, y + 20), 3)
