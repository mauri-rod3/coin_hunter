## Explicaciones

## Prompt 1: Estructuración del proyecto
Actúa como mi asistente de programación para una actividad de vibecoding.

Quiero desarrollar Coin Hunter 2D, un minijuego sencillo en Python con
Pygame para una demostración de clase. Estoy aprendiendo, así que utiliza
código claro, nombres descriptivos en español y comentarios que expliquen
las decisiones importantes.

Todo el proyecto debe estar únicamente dentro de una carpeta llamada
juego. No incluyas Angular, TypeScript, frontend, backend, APIs ni bases
de datos.

Organiza los archivos así:

juego/
├── main.py
├── modelo.py
├── requirements.txt
├── .gitignore
├── README.md

Responsabilidades:
- main.py: ventana, eventos, controles y dibujo con Pygame.
- modelo.py: reglas y estado de la partida, independientes de Pygame.
- requirements.txt: dependencias necesarias.
- .gitignore: excluir el entorno virtual y los archivos temporales.
- README.md: instalación, ejecución, controles y explicación del proyecto.
- tests/test_modelo.py: pruebas de las reglas cuando se implementen.

Comencemos con una versión mínima: una ventana de 800 × 600, un personaje
rectangular que se mueva horizontalmente con las flechas y que no pueda
salir de la pantalla.

Completa correctamente el bucle de eventos, la actualización de pantalla,
el control de fotogramas y el cierre del programa.

## Prompt 2: Juego completo
Sobre la versión anterior de Coin Hunter 2D, implementa estas mejoras
manteniendo toda la aplicación dentro de juego:

1. Pantalla inicial para escribir el nombre del jugador.
2. Movimiento con las flechas izquierda/derecha y con A/D.
3. Monedas que caen y suman 10 puntos al recogerlas.
4. Bombas que caen y restan una vida al tocar al jugador.
5. Tres vidas y partidas de 45 segundos.
6. Un segundo de protección después de recibir un golpe.
7. Pausa y reanudación con P o Escape.
8. Pausa automática cuando la ventana pierde el foco.
9. Pantalla final con puntuación y opciones para repetir o cambiar jugador.

Separa las reglas en modelo.py y la presentación en main.py.
Calcula el movimiento usando el tiempo transcurrido para que no dependa
de la velocidad del equipo.

Dibuja los elementos con Pygame, sin necesitar imágenes externas.
No guardes partidas ni añadas servicios externos.

## Prompt 3: Validaciones
Revisa Coin Hunter 2D y ayúdame a validar su funcionamiento.

Añade pruebas con unittest para las reglas de modelo.py:
- Validación del nombre.
- Límites del movimiento.
- Puntuación al recoger monedas.
- Pérdida de vidas y protección temporal.
- Pausa.
- Fin por tiempo o por pérdida de vidas.
- Reinicio de una partida.

Las pruebas deben ejecutarse sin abrir una ventana y sin necesitar Pygame.

Comprueba que las monedas no puntúen varias veces y que una partida
terminada no siga modificando sus resultados.

También explica cómo resolver el error “Cannot find module pygame”
cuando está instalado en venv_game, pero el editor utiliza el Python
global. Proporciona comandos para comprobar el intérprete y la instalación.