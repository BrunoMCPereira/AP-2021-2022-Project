import controller

def comando(instrucao):
    if instrucao[0]=='RJ' and len(instrucao)==2: #Registar Jogador (RJ NomeJogador)
        return controller.registar(instrucao[1])
    
    elif instrucao[0]=='LJ' and len(instrucao)==1: #Listar Jogadores (LJ)
        return controller.listar()

    elif instrucao[0]=='IJ' and len(instrucao)==3: #Iniciar Jogo (IJ NomeJogadorA NomeJogadorB)
        return controller.iniciar(instrucao[1], instrucao[2])

    elif instrucao[0]=='IJA' and len(instrucao)==3: #Iniciar Jogo Automático (IJA NomeJogador Nível)
        return controller.iniciar_auto(instrucao[1], instrucao[2])

    elif instrucao[0]=='DJ' and len(instrucao)==1: #Detalhes de Jogo (DJ)
        return controller.detalhes()

    elif instrucao[0]=='J' and len(instrucao)==3: #Efetuar Jogada (J NomeJogador Posição)
        return controller.jogada(instrucao[1], instrucao[2])

    elif instrucao[0]=='D' and len(instrucao)>1 and len(instrucao)<=3: #Desistir de Jogo (D NomeJogador NomeJogador)
        return controller.desistir(instrucao)

    elif instrucao[0]=='G' and len(instrucao)==2: #Gravar (G NomeFicheiro)
        return controller.gravar(instrucao[1])

    elif instrucao[0]=='L' and len(instrucao)==2: #Ler (L NomeFicheiro)
        return controller.ler(instrucao[1])

    else: return "Instrução inválida."

def main():
    while True:
        inserir = input()
        print (comando(inserir.split()))