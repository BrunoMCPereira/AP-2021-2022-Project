import controller

def comando(instrucao):
    if instrucao[0]=='RJ' and len(instrucao)==2: #Registar Jogador (RJ NomeJogador)
        resultado = controller.registar(instrucao[1])
        if resultado == None:
            return "Jogador existente."
        else: return "Jogador registado com sucesso."
    
    elif instrucao[0]=='LJ' and len(instrucao)==1: #Listar Jogadores (LJ)
        resultado = controller.listar()
        if resultado == None:
            return "Sem jogadores registados."
        else: return resultado

    elif instrucao[0]=='IJ' and len(instrucao)==3: #Iniciar Jogo (IJ NomeJogadorA NomeJogadorB)
        resultado = controller.iniciar(instrucao[1], instrucao[2])
        if resultado == None:
            return "Jogador inexistente."
        elif resultado == False:
            return "Existe um jogo em curso."
        else: return "Jogo iniciado com sucesso."

    elif instrucao[0]=='IJA' and len(instrucao)==3: #Iniciar Jogo Automático (IJA NomeJogador Nível)
        pass

    elif instrucao[0]=='DJ' and len(instrucao)==1: #Detalhes de Jogo (DJ)
        pass

    elif instrucao[0]=='J' and len(instrucao)==3: #Efetuar Jogada (J NomeJogador Posição)
        pass

    elif instrucao[0]=='D' and len(instrucao)>1 and len(instrucao)<=3: #Desistir de Jogo (D NomeJogador NomeJogador)
        pass

    elif instrucao[0]=='G' and len(instrucao)==2: #Gravar (G NomeFicheiro)
        pass

    elif instrucao[0]=='L' and len(instrucao)==2: #Ler (L NomeFicheiro)
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
