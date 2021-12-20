import model

def registar(player): #Adiciona e retorna True quando o jogador não existe, retorna None quando o jogador existe
    if player not in model.jogadores:
        model.jogadores.append({'Jogador': player, 'Jogos': 0, 'Vitorias': 0, 'Empates': 0, 'Derrotas': 0})
        return True
    else: return None

def listar(): #Retorna os valores das chaves 'Jogador' de cada dicionário na lista jogadores
    resultado = []
    for i in range(len(model.jogadores)):
        resultado.append(model.jogadores[i].get('Jogador'))
    return resultado

def main():
    pass