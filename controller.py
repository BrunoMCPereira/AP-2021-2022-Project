import model

def registar(player): #Adiciona e retorna True quando o jogador não existe, retorna None quando o jogador existe
    for i in range(len(model.jogadores)):
        if player == model.jogadores[i].get('Jogador'):
            return None #Já existe
    model.jogadores.append({'Jogador': player, 'Jogos': 0, 'Vitorias': 0, 'Empates': 0, 'Derrotas': 0})
    return True #Sucesso

def listar(): #Retorna os valores das chaves 'Jogador' de cada dicionário na lista jogadores
    resultado = []
    if len(model.jogadores)==0:
        return None #Sem jogadores
    else:
        for i in range(len(model.jogadores)):
            resultado.append(model.jogadores[i].get('Jogador'))
        return resultado #Sucesso, lista de jogadores

def iniciar(jogador_a, jogador_b): #Inicia um novo jogo entre dois jogadores e retorna a saída com sucesso ou insucesso
    flag = 0
    for i in range(len(model.jogadores)): #Incrementa um valor na flag em cada jogador encontrado, só conta uma vez se forem o mesmo
        if model.jogadores[i].get('Jogador') == jogador_a:
            flag += 1
        elif model.jogadores[i].get('Jogador') == jogador_b:
            flag += 1
    if flag == 2:
        if model.jogo != {}:
            return False #Jogo em curso
        model.jogo.update({'JogadorA': jogador_a, 'JogadorB': jogador_b})
        return True #Sucesso
    else: return None #Jogador Inexistente

def main():
    pass