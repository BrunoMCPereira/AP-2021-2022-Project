import model

def registar(player): #Adiciona e retorna True quando o jogador não existe, retorna None quando o jogador existe
    for i in range(len(model.jogadores)):
        if player == model.jogadores[i].get('Jogador'):
            return None #Já existe
    model.jogadores.append({'Jogador': player, 'Jogos': 0, 'Vitorias': 0, 'Empates': 0, 'Derrotas': 0})
    return True #Sucesso

def listar(): #Retorna os valores das chaves 'Jogador' de cada dicionário na lista jogadores
    resultado = ""
    if len(model.jogadores)==0:
        return None #Sem jogadores
    else:
        for i in range(len(model.jogadores)):
            resultado += model.jogadores[i].get('Jogador') 
            resultado += (" ") + str(model.jogadores[i].get('Jogos'))
            resultado += (" ") + str(model.jogadores[i].get('Vitorias'))
            resultado += (" ") + str(model.jogadores[i].get('Empates'))
            resultado += (" ") + str(model.jogadores[i].get('Derrotas'))
            if i != len(model.jogadores)-1:
                resultado += ("\n")   
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
            return False #Jogo em curso
        model.jogo.update({
        'JogadorA': jogador_a, 'A1':4, 'A2':4, 'A3':4, 'A4':4, 'A5':4, 'A6':4, 'A7':0, 
        'JogadorB': jogador_b, 'B1':4, 'B2':4, 'B3':4, 'B4':4, 'B5':4, 'B6':4, 'B7':0})
        return True #Sucesso
    else: return None #Jogador Inexistente

def detalhes(): #Mostra o tabuleiro do jogo em curso
    if model.jogo == {}:
        return None #Não existe jogo em curso
    else:
        lista = list(model.jogo.values())
        resultado = str(lista[0])
        for i in range(6):
            resultado = resultado + ' [' + str(lista[i+1]) + ']'
        resultado = resultado + ' (' + str(lista[7]) + ')' + '\n' + str(lista[8])
        for i in range(6):
            resultado = resultado + ' [' + str(lista[i+9]) + ']'
        resultado = resultado + ' (' + str(lista[15]) + ')'
        return resultado #Sucesso

def desistir(instrucao): #Mostra o tabuleiro do jogo em curso
    if model.jogo == {}:
        return None #Não existe jogo em curso
    else:
        instrucao.remove('D')
        if len(instrucao) == 1:
            if instrucao[0] != model.jogo.get('JogadorA') and instrucao[0] != model.jogo.get('JogadorB'):
                return False #Jogador não está em jogo
            else:
                for i in range(len(model.jogadores)):
                    if model.jogadores[i].get('Jogador') == instrucao[0]:
                        derrotas = model.jogadores[i].get('Derrotas') + 1
                        model.jogadores[i].update({
                            'Derrotas' : derrotas
                        })
                        break
                if instrucao[0] == model.jogo.get('JogadorA'):
                    for i in range(len(model.jogadores)):
                        if model.jogadores[i].get('Jogador') == model.jogo.get('JogadorB'):
                            vitorias = model.jogadores[i].get('Vitorias') + 1
                            model.jogadores[i].update({
                                'Vitorias' : vitorias
                            })
                            break
                else:
                    for i in range(len(model.jogadores)):
                        if model.jogadores[i].get('Jogador') == model.jogo.get('JogadorA'):
                            vitorias = model.jogadores[i].get('Vitorias') + 1
                            model.jogadores[i].update({
                                'Vitorias' : vitorias
                            })
                            break
                resultado = f'Desistiu o {instrucao[0]}'
                model.jogo = {}
        else: 
            if (instrucao[0] != model.jogo.get('JogadorA') and instrucao[0] != model.jogo.get('JogadorB')) or (instrucao[1] != model.jogo.get('JogadorA') and instrucao[1] != model.jogo.get('JogadorB')) or (instrucao[0] == instrucao[1]):
                return False #Jogador não está em jogo ou são iguais
            else:
                for i in range(len(model.jogadores)):
                    if model.jogadores[i].get('Jogador') == instrucao[0]:
                        derrotas = model.jogadores[i].get('Derrotas') + 1
                        model.jogadores[i].update({
                            'Derrotas' : derrotas
                        })
                        break
                for i in range(len(model.jogadores)):
                    if model.jogadores[i].get('Jogador') == instrucao[1]:
                        derrotas = model.jogadores[i].get('Derrotas') + 1
                        model.jogadores[i].update({
                            'Derrotas' : derrotas
                        })
                        break
            resultado = 'Desistiram os dois'
            model.jogo = {}
        return resultado #Sucesso