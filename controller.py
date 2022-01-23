import model
import os.path 
from os import path

def registar(player): 
    for i in range(len(model.jogadores)): #Verifica se o Jogador já está registado
        if player == model.jogadores[i].get('Jogador'):
            return "Jogador existente."
    if model.jogadores == []:
        model.jogadores.append({'Jogador': "CPU", 'Jogos': 0, 'Vitorias': 0, 'Empates': 0, 'Derrotas': 0})
    model.jogadores.append({'Jogador': player, 'Jogos': 0, 'Vitorias': 0, 'Empates': 0, 'Derrotas': 0}) #Regista o Jogador
    return "Jogador registado com sucesso."

def elementos_v(e):
    return e['Vitorias']

def elementos_j(e):
    return e['Jogador']

def listar(): #Retorna os valores das chaves 'Jogador' de cada dicionário na lista jogadores
    resultado = ""
    if len(model.jogadores)==0:
        model.jogadores.append({'Jogador': "CPU", 'Jogos': 0, 'Vitorias': 0, 'Empates': 0, 'Derrotas': 0})
        #return "Sem jogadores registados." #Nunca acontece
    #else: #Organiza uma string com a scoreboard
    model.jogadores.sort(reverse=True, key=elementos_v) #Organiza a lista de dicionários por valor de vitórias decrescente
    temp = []
    for _ in range(len(model.jogadores)-1): #Esta versão modificada de bubble sort faz com que os jogadores com o mesmo número de vitórias sejam ordenados alfabeticamente
        for i in range(len(model.jogadores)-1):
            if model.jogadores[i].get('Vitorias')==model.jogadores[i+1].get('Vitorias'):
                temp.append(model.jogadores[i])
                temp.append(model.jogadores[i+1])
                temp.sort(key=elementos_j)
                model.jogadores[i] = temp[0]
                model.jogadores[i+1] = temp[1]
                temp = []
    
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
        'JogadorB': jogador_b, 'B1':4, 'B2':4, 'B3':4, 'B4':4, 'B5':4, 'B6':4, 'B7':0,
        'Vez': jogador_a})
        return "Jogo iniciado com sucesso."
    else: return "Jogador inexistente."

def iniciar_auto(jogador, nivel):
    for i in range(len(model.jogadores)):
        if model.jogadores[i].get('Jogador') == jogador:
            if model.jogo !={}:
                return "Existe um jogo em curso."
            model.jogo.update({
            'JogadorA': jogador, 'A1':4, 'A2':4, 'A3':4, 'A4':4, 'A5':4, 'A6':4, 'A7':0, 
            'JogadorB': "CPU", 'B1':4, 'B2':4, 'B3':4, 'B4':4, 'B5':4, 'B6':4, 'B7':0, 
            'Vez': jogador, 'Nivel': nivel})
            return f"Jogo automático de nível {nivel} iniciado com sucesso."
    return "Jogador inexistente."

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

def jogada_valida(vez, pos, jogador):
    lado = vez
    num = model.jogo.get(lado+str(pos))
    model.jogo.update({lado+str(pos): 0})
    pos += 1
    while num > 0: #Distribui as sementes pelas casas seguintes sequencialmente
        while ((lado == vez and pos <= 7) or (lado != vez and pos < 7)) and num > 0:
            model.jogo.update({lado+str(pos) : model.jogo.get(lado+str(pos))+1})
            pos += 1
            num -= 1
        if lado == 'A':
            lado = 'B'
        else: lado = 'A'
        if num > 0: pos = 1
    pos -= 1
    if vez == 'A':
        oponente = 'B'
    else: oponente = 'A'
    if pos == 7:
        return f"O jogador {jogador} tem direito a outra jogada."
    if vez != lado and model.jogo.get(vez+str(pos)) == 1 and model.jogo.get(oponente+str(pos)) != 0: #Se a última casa estava vazia e a do oponente tem algo
        model.jogo.update({ #Retira as sementes da casa oposta para o poço
        vez+'7' : model.jogo.get(vez+'7')+model.jogo.get(oponente+str(pos)) + model.jogo.get(vez+str(pos)),
        oponente+str(pos) : 0,
        vez+str(pos) : 0 
        })
    resultado = None
    if model.jogo.get(vez+'1') == 0 and model.jogo.get(vez+'2') == 0 and model.jogo.get(vez+'3') == 0 and model.jogo.get(vez+'4') == 0 and model.jogo.get(vez+'5') == 0 and model.jogo.get(vez+'6') == 0: #Isto tem de ser visto
        model.jogo.update({ #Se o jogador ficou sem sementes, o oponente move todas as sementes restantes para o seu poço
        oponente+'7': model.jogo.get(oponente+'7')+model.jogo.get(oponente+'6')+model.jogo.get(oponente+'5')+model.jogo.get(oponente+'4')
        +model.jogo.get(oponente+'3')+model.jogo.get(oponente+'2')+model.jogo.get(oponente+'1'),
        oponente+'6': 0, oponente+'5': 0, oponente+'4': 0, oponente+'3': 0, oponente+'2': 0, oponente+'1': 0
        })
        resultado = f"Jogo terminado.\n{model.jogo.get('JogadorA')} {model.jogo.get('A7')}\n{model.jogo.get('JogadorB')} {model.jogo.get('B7')}"
    elif model.jogo.get(oponente+'1') == 0 and model.jogo.get(oponente+'2') == 0 and model.jogo.get(oponente+'3') == 0 and model.jogo.get(oponente+'4') == 0 and model.jogo.get(oponente+'5') == 0 and model.jogo.get(oponente+'6') == 0:
        model.jogo.update({ #Se o oponente ficou sem sementes, o jogador move todas as sementes restantes para o seu poço. Isto acontece quando o jogador captura as ultimas sementes do oponente através de uma casa vazia
        vez+'7': model.jogo.get(vez+'7')+model.jogo.get(vez+'6')+model.jogo.get(vez+'5')+model.jogo.get(vez+'4')
        +model.jogo.get(vez+'3')+model.jogo.get(vez+'2')+model.jogo.get(vez+'1'),
        vez+'6': 0, vez+'5': 0, vez+'4': 0, vez+'3': 0, vez+'2': 0, vez+'1': 0
        })
        resultado = f"Jogo terminado.\n{model.jogo.get('JogadorA')} {model.jogo.get('A7')}\n{model.jogo.get('JogadorB')} {model.jogo.get('B7')}"
    if resultado != None:
        if model.jogo.get(vez+'7') > model.jogo.get(oponente+'7'):
            for i in range(len(model.jogadores)):
                if model.jogadores[i].get('Jogador') == model.jogo.get('Jogador'+vez):
                    model.jogadores[i].update({
                        'Jogos' : model.jogadores[i].get('Jogos') + 1,
                        'Vitorias' : model.jogadores[i].get('Vitorias') + 1
                    })
                    break
            for i in range(len(model.jogadores)):
                if model.jogadores[i].get('Jogador') == model.jogo.get('Jogador'+oponente):
                    model.jogadores[i].update({
                        'Jogos' : model.jogadores[i].get('Jogos') + 1,
                        'Derrotas' : model.jogadores[i].get('Derrotas') + 1
                    })
                    break
        elif model.jogo.get(vez+'7') < model.jogo.get(oponente+'7'):
            for i in range(len(model.jogadores)):
                if model.jogadores[i].get('Jogador') == model.jogo.get('Jogador'+oponente):
                    model.jogadores[i].update({
                        'Jogos' : model.jogadores[i].get('Jogos') + 1,
                        'Vitorias' : model.jogadores[i].get('Vitorias') + 1
                    })
                    break
            for i in range(len(model.jogadores)):
                if model.jogadores[i].get('Jogador') == model.jogo.get('Jogador'+vez):
                    model.jogadores[i].update({
                        'Jogos' : model.jogadores[i].get('Jogos') + 1,
                        'Derrotas' : model.jogadores[i].get('Derrotas') + 1
                    })
                    break
        else:
            for i in range(len(model.jogadores)):
                if model.jogadores[i].get('Jogador') == model.jogo.get('Jogador'+vez):
                    model.jogadores[i].update({
                        'Jogos' : model.jogadores[i].get('Jogos') + 1,
                        'Empates' : model.jogadores[i].get('Empates') + 1
                    })
                    break
            for i in range(len(model.jogadores)):
                if model.jogadores[i].get('Jogador') == model.jogo.get('Jogador'+oponente):
                    model.jogadores[i].update({
                        'Jogos' : model.jogadores[i].get('Jogos') + 1,
                        'Empates' : model.jogadores[i].get('Empates') + 1
                    })
                    break
        model.jogo = {}
        return resultado
    if vez == 'A':
        model.jogo.update({'Vez': model.jogo.get('JogadorB')})
    else: model.jogo.update({'Vez': model.jogo.get('JogadorA')})
    return resultado


def jogada(jogador, pos):
    pos = int(pos)
    if model.jogo == {}:
        return "Não existe jogo em curso."
    for i in range(len(model.jogadores)):
        if model.jogadores[i].get('Jogador') == jogador:
            if jogador != model.jogo.get('JogadorA') and jogador != model.jogo.get('JogadorB'):
                return "Jogador não participa no jogo em curso."
            if jogador == model.jogo.get('Vez'):
                if jogador == model.jogo.get('JogadorA'):
                    vez = 'A'
                else: vez = 'B'
            else: return f"Não é a vez de {jogador}"
            if model.jogo.get(vez+str(pos)) > 0:
                resultado = jogada_valida(vez, pos, jogador)
                if model.jogo.get('JogadorB') == 'CPU' and resultado != f"O jogador {jogador} tem direito a outra jogada.":
                    if model.jogo.get('Nivel') == 'Normal':
                        while True:
                            for i in range(1,6):
                                if model.jogo.get('B'+str(i))!=0:
                                    pos = i
                                    break
                            resultado_bot = jogada_valida('B', pos, 'CPU')
                            if resultado_bot != f"O jogador CPU tem direito a outra jogada.": break
                        if resultado_bot == f"Jogo terminado.\n{model.jogo.get('JogadorA')} {model.jogo.get('A7')}\n{model.jogo.get('JogadorB')} {model.jogo.get('B7')}":
                            resultado = resultado_bot
                    elif model.jogo.get('Nivel') == 'Avançado':
                        while True:
                            flag = False
                            if flag == False:
                                for i in range(1,7):
                                    jogo_temp = {}
                                    jogo_temp.update(model.jogo)
                                    if jogo_temp.get('B'+str(i))!=0: #Propõe uma posição
                                        temp_pos = i
                                        #Simula a distribuição das sementes pelas casas seguintes sequencialmente
                                        temp_lado = 'B'
                                        temp_num = jogo_temp.get(temp_lado+str(temp_pos))
                                        jogo_temp.update({temp_lado+str(temp_pos): 0})
                                        temp_pos += 1
                                        print(model.jogo)
                                        while temp_num > 0:
                                            while ((temp_lado == 'B' and temp_pos <= 7) or (temp_lado != 'B' and temp_pos < 7)) and temp_num > 0:
                                                jogo_temp.update({temp_lado+str(temp_pos) : jogo_temp.get(temp_lado+str(temp_pos))+1})
                                                temp_pos += 1
                                                temp_num -= 1
                                            if temp_lado == 'A':
                                                temp_lado = 'B'
                                            else: temp_lado = 'A'
                                            if temp_num > 0: temp_pos = 1
                                        temp_pos -= 1
                                        if jogo_temp.get(temp_lado+str(temp_pos))==1 and temp_lado == 'B' and temp_pos != 7: #Se a casa não tinha nada, era do lado do CPU e não era o poço
                                            if jogo_temp.get('A'+str(temp_pos)) != 0: #Se a casa oposta tem algo
                                                pos = i #Escolhe a posição proposta
                                                flag = True
                                                print("Escolhi uma pos")
                                                break
                            if flag == False:
                                for i in range(1,7):
                                    if model.jogo.get('B'+str(i))!=0:
                                        pos = i
                                        print("Escolhi a mais à esquerda")
                                        break 
                            resultado_bot = jogada_valida('B', pos, 'CPU') #Nesta lógica, se existirem mais situações, escolhe a que estiver mais à esquerda
                            if resultado_bot != f"O jogador CPU tem direito a outra jogada.": break
                        if resultado_bot == f"Jogo terminado.\n{model.jogo.get('JogadorA')} {model.jogo.get('A7')}\n{model.jogo.get('JogadorB')} {model.jogo.get('B7')}":
                            resultado = resultado_bot        
                if resultado != None:
                    return resultado
                return "Jogada efetuada com sucesso."
            else: return "Jogada inválida"
    return "Jogador inexistente"

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
                            'Jogos' : model.jogadores[i].get('Jogos') + 1,
                            'Derrotas' : model.jogadores[i].get('Derrotas') + 1
                        })
                        break
                if instrucao[0] == model.jogo.get('JogadorA'):
                    for i in range(len(model.jogadores)):
                        if model.jogadores[i].get('Jogador') == model.jogo.get('JogadorB'):
                            model.jogadores[i].update({
                                'Jogos' : model.jogadores[i].get('Jogos') + 1,
                                'Vitorias' : model.jogadores[i].get('Vitorias') + 1
                            })
                            break
                else:
                    for i in range(len(model.jogadores)):
                        if model.jogadores[i].get('Jogador') == model.jogo.get('JogadorA'):
                            model.jogadores[i].update({
                                'Jogos' : model.jogadores[i].get('Jogos') + 1,
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
                            'Jogos' : model.jogadores[i].get('Jogos') + 1,
                            'Derrotas' : model.jogadores[i].get('Derrotas') + 1
                        })
                        break
                for i in range(len(model.jogadores)):
                    if model.jogadores[i].get('Jogador') == instrucao[1]:
                        model.jogadores[i].update({
                            'Jogos' : model.jogadores[i].get('Jogos') + 1,
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