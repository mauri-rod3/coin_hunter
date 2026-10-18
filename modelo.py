from dataclasses import dataclass
import random

ANCHO = 800
ALTO = 600
LIMITE_SUPERIOR = 105
DURACION = 45.0
VIDAS = 3
PUNTOS_MONEDA = 10
VELOCIDAD_JUGADOR = 370
INTERVALO_CAIDA = 0.55


@dataclass
class Objeto:
    x: float
    y: float
    tipo: str
    velocidad: float
    ancho: int = 28
    alto: int = 28


def se_superponen(ax, ay, ancho_a, alto_a, bx, by, ancho_b, alto_b):
    return (
        ax < bx + ancho_b
        and ax + ancho_a > bx
        and ay < by + alto_b
        and ay + alto_a > by
    )


class Partida:
    """Una instancia representa una partida; actualizar recibe segundos reales."""

    jugador_ancho = 64
    jugador_alto = 34
    jugador_y = ALTO - 76

    def __init__(self, nombre_jugador: str, rng=None):
        nombre = nombre_jugador.strip()
        if not nombre or len(nombre) > 50:
            raise ValueError("Escribe un nombre de entre 1 y 50 caracteres.")
        self.nombre_jugador = nombre
        self.puntuacion = 0
        self.vidas = VIDAS
        self.restante = DURACION
        self.jugador_x = (ANCHO - self.jugador_ancho) / 2
        self.objetos: list[Objeto] = []
        self.terminada = False
        self.pausada = False
        self._hasta_caida = 0.25
        self._inmunidad = 0.0
        self._rng = rng if rng is not None else random.Random()

    @property
    def inmune(self):
        return self._inmunidad > 0

    def alternar_pausa(self):
        if not self.terminada:
            self.pausada = not self.pausada

    def _crear_objeto(self):
        tipo = "bomba" if self._rng.random() < 0.28 else "moneda"
        self.objetos.append(
            Objeto(
                x=self._rng.uniform(22, ANCHO - 50),
                y=LIMITE_SUPERIOR,
                tipo=tipo,
                velocidad=self._rng.uniform(175, 250),
            )
        )

    def actualizar(self, dt: float, direccion: int = 0):
        if self.terminada or self.pausada or dt <= 0:
            return
        dt = min(dt, self.restante)
        self.restante = max(0.0, self.restante - dt)
        self._inmunidad = max(0.0, self._inmunidad - dt)
        direccion = max(-1, min(1, direccion))
        self.jugador_x = max(
            16,
            min(
                ANCHO - self.jugador_ancho - 16,
                self.jugador_x + direccion * VELOCIDAD_JUGADOR * dt,
            ),
        )
        self._hasta_caida -= dt
        while self._hasta_caida <= 0:
            self._crear_objeto()
            self._hasta_caida += INTERVALO_CAIDA

        restantes = []
        for objeto in self.objetos:
            objeto.y += objeto.velocidad * dt
            toca = se_superponen(
                self.jugador_x, self.jugador_y,
                self.jugador_ancho, self.jugador_alto,
                objeto.x, objeto.y, objeto.ancho, objeto.alto,
            )
            if toca:
                if objeto.tipo == "moneda":
                    self.puntuacion += PUNTOS_MONEDA
                elif not self.inmune:
                    self.vidas -= 1
                    self._inmunidad = 1.0
                    if self.vidas == 0:
                        self.terminada = True
                        break
            elif objeto.y < ALTO:
                restantes.append(objeto)
        self.objetos = restantes
        self.terminada = self.terminada or self.restante <= 0

    def resultado(self):        
        return {
            "nombre_jugador": self.nombre_jugador,
            "puntuacion": self.puntuacion,
        }