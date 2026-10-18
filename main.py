import math, os, pygame

os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

from modelo import ALTO, ANCHO, DURACION, Partida

FONDO = (12, 19, 35)
PANEL = (22, 34, 53)
BORDE = (45, 63, 84)
BLANCO = (233, 242, 250)
GRIS = (149, 168, 190)
VERDE = (77, 235, 174)
ORO = (255, 210, 90)
ROJO = (255, 107, 123)


class Juego:
    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("Coin Hunter 2D")
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
        color = BORDE if secundario else VERDE
        if hover:
            color = (65, 83, 104) if secundario else (116, 249, 196)
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
        self.pantalla.fill(FONDO)
        for x in range(24, ANCHO, 40):
            for y in range(24, ALTO, 40):
                pygame.draw.circle(self.pantalla, (28, 41, 59), (x, y), 1)

    def moneda(self, x, y):
        pygame.draw.circle(self.pantalla, (89, 66, 30), (x, y + 2), 16)
        pygame.draw.circle(self.pantalla, ORO, (x, y), 14)
        pygame.draw.circle(self.pantalla, (224, 162, 54), (x, y), 10, 2)
        pygame.draw.line(self.pantalla, (255, 239, 173), (x, y - 6), (x, y + 6), 3)

    def bomba(self, x, y):
        pygame.draw.line(self.pantalla, ORO, (x + 4, y - 11), (x + 9, y - 18), 3)
        pygame.draw.circle(self.pantalla, ROJO, (x + 10, y - 19), 3)
        pygame.draw.circle(self.pantalla, (75, 40, 58), (x, y), 14)
        pygame.draw.circle(self.pantalla, ROJO, (x, y), 14, 2)
        pygame.draw.line(self.pantalla, ROJO, (x - 4, y - 4), (x + 4, y + 4), 2)
        pygame.draw.line(self.pantalla, ROJO, (x + 4, y - 4), (x - 4, y + 4), 2)

    def inicio(self):
        self.texto("UN PEQUEÑO RETO. MUCHAS MONEDAS.", 400, 60, VERDE, "pequena", True)
        self.texto("Coin Hunter", 400, 91, fuente="titulo", centro=True)
        self.texto("Recoge monedas. Esquiva bombas. Supera tu marca.", 400, 159, GRIS, centro=True)
        pygame.draw.rect(self.pantalla, PANEL, (150, 220, 500, 280), border_radius=20)
        self.texto("¿Cómo te llamas?", 230, 248, fuente="media")
        campo = pygame.Rect(230, 300, 340, 53)
        pygame.draw.rect(self.pantalla, FONDO, campo, border_radius=10)
        pygame.draw.rect(self.pantalla, VERDE, campo, 1, border_radius=10)
        # Conserva hasta 50 caracteres y muestra el final si no caben en el campo.
        visible = self.nombre
        while self.fuentes["normal"].size(visible)[0] > campo.width - 34:
            visible = visible[1:]
        self.texto(visible or "Escribe tu nombre", 246, 312, BLANCO if visible else GRIS)
        if pygame.time.get_ticks() % 1000 < 500:
            cursor_x = 246 + self.fuentes["normal"].size(visible)[0]
            pygame.draw.line(self.pantalla, VERDE, (cursor_x, 312), (cursor_x, 338), 2)
        if self.error:
            self.texto(self.error, 400, 367, ROJO, "pequena", True)
        else:
            self.texto("45 segundos · 3 vidas · 10 puntos por moneda", 400, 367, GRIS, "pequena", True)
        self.boton(self.boton_principal, "Comenzar partida  →")
        self.texto("← → o A / D: moverse     P: pausa     Enter: comenzar", 400, 530, GRIS, "pequena", True)

    def tablero(self):
        partida = self.partida
        pygame.draw.rect(self.pantalla, PANEL, (16, 16, 768, 75), border_radius=16)
        self.texto("PUNTOS", 36, 27, GRIS, "pequena")
        self.texto(f"{partida.puntuacion:03}", 36, 46, ORO, "media")
        self.texto("VIDAS", 215, 27, GRIS, "pequena")
        for i in range(3):
            pygame.draw.circle(self.pantalla, ROJO if i < partida.vidas else BORDE, (227 + i * 25, 66), 8)
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
            pygame.draw.rect(self.pantalla, (27, 78, 75), cuerpo.move(0, 5), border_radius=10)
            pygame.draw.rect(self.pantalla, VERDE, cuerpo, border_radius=10)
            for dx in (20, 43):
                pygame.draw.circle(self.pantalla, FONDO, (cuerpo.x + dx, cuerpo.y + 13), 4)
        pygame.draw.line(self.pantalla, BORDE, (16, ALTO - 34), (ANCHO - 16, ALTO - 34))
        self.texto("← → / A D   MOVERSE", 28, ALTO - 26, GRIS, "pequena")
        self.texto("MONEDA +10     BOMBA −1 VIDA", 475, ALTO - 26, GRIS, "pequena")
        if partida.pausada:
            velo = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
            velo.fill((5, 10, 22, 215))
            self.pantalla.blit(velo, (0, 0))
            self.texto("Pausa", 400, 235, fuente="titulo", centro=True)
            self.texto("Pulsa P o Esc para continuar", 400, 315, GRIS, centro=True)

    def resultado(self):
        partida = self.partida
        self.texto("¡TIEMPO COMPLETADO!" if partida.vidas else "¡SIGUE INTENTÁNDOLO!", 400, 65, VERDE, "pequena", True)
        self.texto("Fin de la partida", 400, 96, fuente="titulo", centro=True)
        pygame.draw.rect(self.pantalla, PANEL, (150, 195, 500, 335), border_radius=20)
        self.texto("TU PUNTUACIÓN", 400, 223, GRIS, "pequena", True)
        self.texto(partida.puntuacion, 400, 248, ORO, "titulo", True)
        self.texto(f"Monedas recogidas: {partida.puntuacion // 10}", 400, 326, centro=True)
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