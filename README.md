# Robot Combat

> Are you able to design an unbeatable automated virtual robot?

This project provides the structure to run virtual robot combats.
Robots can be controlled manually (with the [ManualRobot]() class) or automated (with the [AutomatedRobot]() class).

It requires the following Python packages:
* pygame
* numpy

 ## Combat rules
 
 Estas reglas habría que programarlas en una clase superior que gestione un torneo.
 
 * Los robots se enfrentan en una serie de tres duelos. El ganador será aquel que gane más duelos.
 * Si uno de los dos robots muere durante el duelo, el duelo finaliza. El robot superviviente será el ganador. Si ambos murieran simultaneamente, ese duelo no tendría ganador.
 * Si un robot alcanza el nivel ``N_targert=20`` (aún sin determinar) el duelo finalizará en un máximo de ``T=30`` segundos (aún sin determinar). Si el tiempo acaba y ambos robots sobreviven, aquellos que hayan logrado el nivel ``N_target`` serán los ganadores.
 * En caso de que ambos robots hayan sido declarados ganadores en el mismo número de duelos, el desempate ser hará comparando la suma de los puntos de experiencia obtenidos por cada uno en aquellos duelos en los que hayan sido declarados ganadores. Si ambos robots han obtenido la misma puntuación, se dará un empate técnico.
