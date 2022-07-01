#! /usr/bin/env python3


# Módulo Game

import sys
import random
from time import sleep
from enumeration import Goal, Status, Action
from entidade import Agent, Knowledge, Cave
from conhecimento import perceive, tell, update, ask
from movimento import bump_wall



def print_intro():
  print("Hunt The Wumpus")
  print("\n")


def print_actions():
  print("---------- Menu ----------\n")
  print("1) Mover para frente")
  print("2) Virar a esquerda")
  print("3) Virar a direita")
  print("4) Pegar")
  print("5) Atirar")


def print_perceptions(perceptions):
  wumpus, pit, gold = perceptions
  if wumpus == Status.Present:
    print('Nossa, que mal cheiro.')
  if pit == Status.Present:
    print('Ventinho gostoso.')
  if gold == Status.Present:
    print('Algo brilhante  no caminho.')
  if perceptions == (Status.Absent,) * 3:
    print('Sem percepções.')
  print()


def parse_action(action):
  if action == 1:
    return Action.Move, (0,)
  elif action == 2:
    return Action.Turn, -1
  elif action == 3:
    return Action.Turn, 1
  elif action == 4:
    return Action.Grab, None
  elif action == 5:
    return Action.Shoot, None
  else:
    print('ERROOUU!!! Escolha um dos números listados acima para fazer uma ação!')


def print_cave(loc, direction):
  print(direction)
  setas = {
          0: '↑',
          1: '→',
          2: '↓',
          3: '←',
      }
  print()
  print()
  print('---------- Caverna ----------')
  print('   ', '   '.join([str(i) for i in range(0, 4)]))
  print('  __________________')
  y = 0
  cont = 0  
  #cont para numerar os quadros da matriz
  while y < 4:
    x = 0
    while x < 4:
      #agr o agente mostra seu direcionamento
      print(
        ''.join(
              [
                str(cont) if x == 0 else '', '|_{}_|'.format(
                setas[direction]) if (x, y) == loc else '|___|']), end='')
      x += 1
    print()
    y += 1
    if cont <= 3:
      cont += 1
  print()


if __name__ == '__main__':

  # Init seed
  if '-seed' in sys.argv:
    # Definição de um valor padrão 1 para seed
    seed = 1
    try:
      #Era acessado a posição do argumento seed, isso gerava um erro, add try para corrigir
      seed = sys.argv[int(sys.argv.index('-seed'))]
    except ValueError:
      pass
    random.seed(seed)

  # Define as entidades
  cave = Cave()
  kb = Knowledge()
  agent = Agent()

  # Mostra a introdução
  print_intro()

  # Executa o jogo
  while True:
    print('Agente:\n{}'.format(agent))
    print_cave(agent.location, agent.direction)

    # Percepção na localidade corrente
    perceptions = perceive(cave, agent.location)
    if perceptions is None:
      print('Game Over. Você Morreu!')
      break

    # Ativa o módulo de Inteligência Artificial
    print_perceptions(perceptions)

    if '-ai' in sys.argv:
      tell(kb, perceptions, agent.location)
      update(kb, agent.location)
      goal = Goal.SeekGold if not agent.has_gold else Goal.BackToEntry
      action = ask(kb, agent.location, agent.direction, goal)
      print('Ação:\n{} {}\n'.format(*action)) #agr a ai n tem necessidade de input
      sleep(2)
    else:
      print_actions()
      action = int(input('Qual sua Próxima Ação? '))
      print()
      action = parse_action(action)

    # Realiza ação
    if agent.perform(action, cave, kb):
      print('Você ouviu um grito.\n')

    # Verifica se o jogo terminou e o agente venceu
    if agent.has_gold and agent.location == (0, 0):
      print_cave(agent.location, agent.direction)
      print('Você Venceu!!')
      break
    # O agente n consegue sair da matriz
    if agent.location is None:
      print_cave(agent.location, agent.direction)
      bump_wall(agent.location -1, agent.direction-1)