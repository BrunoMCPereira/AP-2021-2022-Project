import controller

def comando(instrucao):
    if instrucao[0]=='RJ' and len(instrucao)==2: #Registar Jogador
        resultado = controller.registar(instrucao[1])
        if resultado == None:
            return "Jogador existente."
        else: return "Jogador registado com sucesso."
    
    elif instrucao[0]=='LJ' and len(instrucao)==1: #Listar Jogadores
        resultado = controller.listar()
        if resultado == None:
            return "Sem jogadores registados."
        else: return resultado

    elif instrucao[0]=='IJ' and len(instrucao)==3: #Iniciar Jogo
        pass

    elif instrucao[0]=='IJA' and len(instrucao)==3: #Iniciar Jogo Automático
        pass

    elif instrucao[0]=='DJ' and len(instrucao)==1: #Detalhes de Jogo
        pass

    elif instrucao[0]=='J' and len(instrucao)==3: #Efetuar Jogada
        pass

    elif instrucao[0]=='D' and len(instrucao)>1 and len(instrucao)<=3: #Desistir de Jogo
        pass

    elif instrucao[0]=='G' and len(instrucao)==2: #Gravar
        pass

    elif instrucao[0]=='L' and len(instrucao)==2: #Ler
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
