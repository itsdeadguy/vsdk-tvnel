from ventilastation.director import director, stripes
from ventilastation.scene import Scene
from ventilastation.sprites import Sprite

from apps.vasura_scripts.managers.balas_manager import *
from apps.vasura_scripts.managers.enemigos_manager import *
from apps.vasura_scripts.managers.gameplay_manager import *

from apps.vasura_scripts.managers.spawner_enemigos import SpawnerEnemigos

from apps.vasura_scripts.entities.nave import Nave
from apps.vasura_scripts.entities.planeta import Planeta

import gc


class VasuraEspacial(Scene):
    stripes_rom = "vasura_espacial"

    def on_enter(self):
        super(VasuraEspacial, self).on_enter()

        #Inicializacion
        self.planet = Planeta(self)

        self.manager_balas = BalasManager(self)
        self.manager_enemigos = EnemigosManager(self)
        self.spawner_enemigos = SpawnerEnemigos(self.manager_enemigos)
        
        self.nave = Nave(self, self.manager_balas)
        
        self.gameplay_manager = GameplayManager(self.nave)

        #Suscripciones a eventos
        self.planet.al_ser_golpeado.suscribir(self.gameplay_manager.on_planet_hit)
        
        self.gameplay_manager.al_perder_vida.suscribir(self.planet.al_perder_vida)
        self.gameplay_manager.game_over.suscribir(self.muerte)

        self.manager_enemigos.al_morir_enemigo.suscribir(self.gameplay_manager.al_morir_enemigo)
        self.call_later(1000 * 30, self.juntar_basura)

        self.reproducir_bgm()

    def juntar_basura(self):
        gc.collect()
        self.call_later(1000 * 30, self.juntar_basura)

    def step(self):
        self.nave.step()
        self.manager_enemigos.step()
        self.manager_balas.step()
        self.gameplay_manager.step()
        self.spawner_enemigos.step()

        if director.was_pressed(director.BUTTON_D):
            self.finished()

    def on_exit(self):
        self.nave.limpiar_eventos()
        self.planet.limpiar_eventos()

        self.manager_enemigos.limpiar()
        self.gameplay_manager.limpiar()
        self.manager_balas.limpiar()

        director.music_off()

    def finished(self):
        gc.collect()
        director.pop()
        raise StopIteration()

    def reproducir_bgm(self):
        director.music_play("vasura_espacial/cancion_no_robada")
        self.call_later(85000, self.reproducir_bgm)
    
    def muerte(self):
        director.music_play("vasura_espacial/game_over")
        self.finished()


def main():
    return VasuraEspacial()
