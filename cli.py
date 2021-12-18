import controller

def comando(instrucao):
    if instrucao[0]=='RJ' and len(instrucao)==2: #Registar Jogador
        resultado = controller.registar(instrucao[1])
        if resultado == None:
            return "Jogador existente."
        else: return "Jogador registado com sucesso."
    
    elif instrucao[0]=='LJ': #Listar Jogadores
        pass

    elif instrucao[0]=='IJ': #Iniciar Jogo
        pass

    elif instrucao[0]=='IJA': #Iniciar Jogo Automático
        pass

    elif instrucao[0]=='DJ': #Detalhes de Jogo
        pass

    elif instrucao[0]=='J': #Efetuar Jogada
        pass

    elif instrucao[0]=='D': #Desistir de Jogo
        pass

    elif instrucao[0]=='G': #Gravar
        pass

    elif instrucao[0]=='L': #Ler
        pass

    else: return None

def main():
    while True:
        inserir = input()
        instrucao = inserir.split()
        resultado = comando(instrucao)
        if resultado == None:
            print("Instrução inválida.")
        else: print (resultado)
