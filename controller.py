import model

def registar(player): #Adiciona e retorna True quando o jogador não existe, retorna None quando o jogador existe
    if player not in model.jogadores:
        model.jogadores.append(player)
        return True
    else: return None

def main():
    pass