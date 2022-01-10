import model
import os.path 
from os import path

def registar(player): 
    for i in range(len(model.jogadores)): #Verifica se o Jogador já está registado
        if player == model.jogadores[i].get('Jogador'):
            return "Jogador existente."
    model.jogadores.append({'Jogador': player, 'Jogos': 0, 'Vitorias': 0, 'Empates': 0, 'Derrotas': 0}) #Regista o Jogador
    return "Jogador registado com sucesso."

def listar(): #Retorna os valores das chaves 'Jogador' de cada dicionário na lista jogadores
    resultado = ""
    if len(model.jogadores)==0:
        return "Sem jogadores registados."
    else: #Organiza uma string com a scoreboard
        for i in range(len(model.jogadores)): 
            resultado += model.jogadores[i].get('Jogador') 
            resultado += (" ") + str(model.jogadores[i].get('Jogos'))
            resultado += (" ") + str(model.jogadores[i].get('Vitorias'))
            resultado += (" ") + str(model.jogadores[i].get('Empates'))
            resultado += (" ") + str(model.jogadores[i].get('Derrotas'))
            if i != len(model.jogadores)-1:
                resultado += ("\n") #Adiciona newline entre jogadores, de modo a não adicionar depois do último
        return resultado #Sucesso, lista de jogadores

def iniciar(jogador_a, jogador_b): #Inicia um novo jogo entre dois jogadores e retorna a saída com sucesso ou insucesso
    flag = 0
    for i in range(len(model.jogadores)): 
        #Incrementa um valor na flag em cada jogador encontrado, só conta uma vez se forem o mesmo
        if model.jogadores[i].get('Jogador') == jogador_a:
            flag += 1
        elif model.jogadores[i].get('Jogador') == jogador_b:
            flag += 1
    if flag == 2:
        if model.jogo != {}:
            return "Existe um jogo em curso."
        model.jogo.update({
        'JogadorA': jogador_a, 'A1':4, 'A2':4, 'A3':4, 'A4':4, 'A5':4, 'A6':4, 'A7':0, 
        'JogadorB': jogador_b, 'B1':4, 'B2':4, 'B3':4, 'B4':4, 'B5':4, 'B6':4, 'B7':0})
        return "Jogo iniciado com sucesso."
    else: return "Jogador inexistente."

def detalhes(): #Mostra o tabuleiro do jogo em curso
    if model.jogo == {}:
        return "Não existe jogo em curso."
    else:
        lista = list(model.jogo.values()) #Recolhe os valores do dicionário do jogo para dentro de uma lista
        resultado = str(lista[0])
        for i in range(6):
            resultado = resultado + ' [' + str(lista[i+1]) + ']'
        resultado = resultado + ' (' + str(lista[7]) + ')' + '\n' + str(lista[8])
        for i in range(6):
            resultado = resultado + ' [' + str(lista[i+9]) + ']'
        resultado = resultado + ' (' + str(lista[15]) + ')'
        return resultado #Sucesso, retorna uma string com os valores estruturados

def desistir(instrucao): #Mostra o tabuleiro do jogo em curso
    if model.jogo == {}:
        return "Não existe jogo em curso."
    else:
        instrucao.pop(0)
        if len(instrucao) == 1: #1 jogador
            if instrucao[0] != model.jogo.get('JogadorA') and instrucao[0] != model.jogo.get('JogadorB'):
                for i in range(len(model.jogadores)):
                    if model.jogadores[i].get('Jogador') == instrucao[0]:
                        return "Jogador não participa no jogo em curso."
                return "Jogador inexistente."
            else:
                for i in range(len(model.jogadores)):
                    if model.jogadores[i].get('Jogador') == instrucao[0]:
                        model.jogadores[i].update({
                            'Derrotas' : model.jogadores[i].get('Derrotas') + 1
                        })
                        break
                if instrucao[0] == model.jogo.get('JogadorA'):
                    for i in range(len(model.jogadores)):
                        if model.jogadores[i].get('Jogador') == model.jogo.get('JogadorB'):
                            model.jogadores[i].update({
                                'Vitorias' : model.jogadores[i].get('Vitorias') + 1
                            })
                            break
                else:
                    for i in range(len(model.jogadores)):
                        if model.jogadores[i].get('Jogador') == model.jogo.get('JogadorA'):
                            model.jogadores[i].update({
                                'Vitorias' : model.jogadores[i].get('Vitorias') + 1
                            })
                            break
                model.jogo = {}
        else: #2 jogadores
            flag = False #Mantém-se False se o primeiro não existir
            if (instrucao[0] != model.jogo.get('JogadorA') and instrucao[0] != model.jogo.get('JogadorB')) or (instrucao[1] != model.jogo.get('JogadorA') and instrucao[1] != model.jogo.get('JogadorB')) or (instrucao[0] == instrucao[1]): #Não estão em jogo ou são iguais
                for i in range(len(model.jogadores)):
                    if model.jogadores[i].get('Jogador') == instrucao[0]: #Se o primeiro existe
                        flag = True #Primeiro existe
                        break
                if flag == False: return "Jogador inexistente." #Se o primeiro não existe
                for i in range(len(model.jogadores)):
                    if model.jogadores[i].get('Jogador') == instrucao[1]: #Se o segundo existe
                        return "Jogador não participa no jogo em curso." #Ambos existem
                return "Jogador inexistente." #O segundo não existe
            else:
                for i in range(len(model.jogadores)):
                    if model.jogadores[i].get('Jogador') == instrucao[0]:
                        model.jogadores[i].update({
                            'Derrotas' : model.jogadores[i].get('Derrotas') + 1
                        })
                        break
                for i in range(len(model.jogadores)):
                    if model.jogadores[i].get('Jogador') == instrucao[1]:
                        model.jogadores[i].update({
                            'Derrotas' : model.jogadores[i].get('Derrotas') + 1
                        })
                        break
            model.jogo = {}
        return 'Jogo terminado com sucesso.' #Sucesso

def gravar(nome_ficheiro): #Grava o programa num ficheiro
    jogadores_string_values = "" #String onde guardo os values dos dicionarios dos jogadores
    with open(f'{nome_ficheiro}.txt', 'w') as f: #
        for i in model.jogadores: #i representa cada dicionário de jogador
            for j in i.values():#j representa cada valor do dicionario de jogador
                jogadores_string_values += str(j) + (" ")
        f.write(jogadores_string_values) #escreve os values de todos os dicionários de jogadorees com (" ") entre eles
        f.write("\n") #Enter para manter os valores dos jogadores na primeira linha e os valores do jogo na segunda linha
        jogo_string_values = "" #String onde guardo os values do dicionário do jogo
        for i in model.jogo.values(): #cada i representa um valor do dicionário do jogo
            jogo_string_values += str(i) + (" ") 
        f.write(jogo_string_values) #escreve os values do dicionário do jogo com (" ") entre eles
    return 'Jogo gravado com sucesso.'

def ler(nome_ficheiro): #Abertura do ficheiro em modo leitura
    if path.isfile(f"{nome_ficheiro}.txt") == True:
        model.jogadores.clear() #limpa lista de dicionarios dos jogadores
        f = open(f"{nome_ficheiro}.txt", "r", encoding="utf-8") #encoding="utf-8"serve para ler os sinais de pontuação
        ficheiro = f.readlines() #guarda informação do ficheiro a ser lido na variável ficheiro
        jogadores_lista_values = ficheiro[0].split(" ") #string -> lista | ((" ") -> (","))
        jogadores_lista_values.pop(len(jogadores_lista_values)-1) #elimina o ultimo elemento porque é um (" ")
        for i in range(0, (len(jogadores_lista_values) - 4), 5): #i começa a 0 e a len(lista) é sempre reduzida por 4 para contar com os incrementos que damos ao i nas posições da lista, é sempre incremetado por 5 porque em cada loop alteramos 5 keys. elementos da lista usados em cada dicionário = (1º dicionario -> 0, 1, 2, 3, 4), (2º dicionario -> 5, 6, 7, 8, 9) etc...
            model.jogadores.append({'Jogador': jogadores_lista_values[i], 'Jogos': int(jogadores_lista_values[i+1]), 'Vitorias': int(jogadores_lista_values[i+2]), 'Empates': int(jogadores_lista_values[i+3]), 'Derrotas': int(jogadores_lista_values[i+4])}) #Ultimos 4 values tem de ser int para poderem ser alterados nas outra funções (ex: D)
        if len(ficheiro)==2: #apenas lê dicionário de jogo se existir dados de jogo no ficheiro (se tiver sido gravado a meio de um jogo)
            jogo_lista_values = ficheiro[1].split(" ") #string -> lista | ((" ") -> (","))
            jogo_lista_values.pop(len(jogo_lista_values)-1) #elimina ultimo elemento (" ")
            model.jogo.update({ #muda keys do dicionário de jogo atual para keys de dicionário de jogo do ficheiro
                'JogadorA': jogo_lista_values[0], 'A1':int(jogo_lista_values[1]), 'A2':int(jogo_lista_values[2]), 'A3':int(jogo_lista_values[3]), 'A4':int(jogo_lista_values[4]), 'A5':int(jogo_lista_values[5]), 'A6':int(jogo_lista_values[6]), 'A7':int(jogo_lista_values[7]), 
                'JogadorB': jogo_lista_values[8], 'B1':int(jogo_lista_values[9]), 'B2':int(jogo_lista_values[10]), 'B3':int(jogo_lista_values[11]), 'B4':int(jogo_lista_values[12]), 'B5':int(jogo_lista_values[13]), 'B6':int(jogo_lista_values[14]), 'B7':int(jogo_lista_values[15])})
        return 'Jogo lido com sucesso.'
    return 'Ficheiro inexistente.'