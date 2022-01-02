from typing import List, Optional

import pygame

from structures import Point, Cercle, Rectangle
from tir import Tir

TITRE = "Simulation de tirs"
RESOLUTION = (900, 900)
BG_COLOR = "white"

S_COLOR = "red"
T_COLOR = "blue"
PRECISION = 1
SIZE = 15


class Scene:
    screen: pygame.Surface
    target: Optional[Cercle]
    shooter: Optional[Cercle]
    tirs: List[Tir]
    murs: List[Rectangle]
    temp_point: Optional[Point]
    mode: int

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.target = None
        self.shooter = None
        self.tirs = []
        self.murs = []
        self.temp_point = None
        self.mode = 0

    def change_mode(self):
        self.mode = (self.mode + 1) % 2

    def draw_all(self):
        if self.target:
            self.target.draw(self.screen)
        if self.shooter:
            self.shooter.draw(self.screen)
        for tir in self.tirs:
            tir.draw(self.screen)
        for mur in self.murs:
            mur.draw(self.screen)


def handle_events(scene: Scene):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

        elif event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
            scene.change_mode()
            print(scene.mode)

        elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
            if scene.target and scene.shooter:
                for angle in range(0, 360 * PRECISION):
                    tir = Tir(scene.shooter.pos, angle / PRECISION, scene.target)
                    tir.calculer()

                    scene.tirs.append(tir)

        if scene.mode == 0:
            if event.type == pygame.MOUSEBUTTONUP:
                poser_rond(event, scene)

        else:
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                poser_obstacle(event, scene)

    return True


def poser_rond(event: pygame.event.Event, scene: Scene):
    if event.button == 1:  # Gauche
        scene.target = Cercle(Point(event.pos[0], event.pos[1]), SIZE, T_COLOR)

    elif event.button == 3:  # Droite
        scene.shooter = Cercle(Point(event.pos[0], event.pos[1]), SIZE, S_COLOR)

    scene.tirs.clear()


def poser_obstacle(event: pygame.event.Event, scene: Scene):
    if event.button == 1:
        if event.type == pygame.MOUSEBUTTONDOWN:
            scene.temp_point = Point(event.pos[0], event.pos[1])

        elif event.type == pygame.MOUSEBUTTONUP:
            mur = Rectangle(scene.temp_point, Point(event.pos[0], event.pos[1]))
            if not (mur.is_in(scene.shooter.pos) or mur.is_in(scene.target.pos)):
                scene.murs.append(mur)
                scene.temp_point = None

    elif event.button == 3:
        pass


def main():
    pygame.display.set_caption(TITRE)
    screen = pygame.display.set_mode(RESOLUTION)
    screen.fill(BG_COLOR)
    pygame.init()

    scene = Scene(screen)
    running = True

    while running:
        running = handle_events(scene)

        screen.fill(BG_COLOR)
        scene.draw_all()
        pygame.display.flip()


if __name__ == '__main__':
    main()
    pygame.quit()