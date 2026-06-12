import os
import sys

import controller


def _limpar_ecra():
    """Limpa o terminal para redesenhar menus e tabuleiro."""
    os.system("cls" if os.name == "nt" else "clear")


def _pausa():
    """Espera pelo utilizador antes de voltar ao menu anterior."""
    input("\nPrima Enter para continuar...")


def _ler_texto(mensagem):
    """Le um valor de texto introduzido pelo utilizador."""
    return input(mensagem).strip()


def _mostrar_menu_principal():
    """Mostra o menu inicial da aplicacao."""
    _limpar_ecra()
    print("========================================")
    print("              MANCALA")
    print("========================================")
    print("1 - Novo jogo")
    print("2 - Continuar jogo gravado")
    print("3 - Registar jogador")
    print("4 - Jogadores registados")
    print("0 - Sair")
    print("========================================")


def _mostrar_menu_novo_jogo():
    """Mostra o submenu onde se escolhe o tipo de jogo."""
    _limpar_ecra()
    print("========================================")
    print("             NOVO JOGO")
    print("========================================")
    print("1 - Jogador contra jogador")
    print("2 - Jogador contra CPU")
    print("0 - Voltar")
    print("========================================")


def _mostrar_jogadores():
    """Apresenta a tabela de jogadores registados."""
    _limpar_ecra()
    print("========================================")
    print("        JOGADORES REGISTADOS")
    print("========================================")
    print(controller.listar())


def _registar_jogador_menu():
    """Regista um jogador a partir do menu principal."""
    _limpar_ecra()
    print("========================================")
    print("          REGISTAR JOGADOR")
    print("========================================")
    nome = _ler_texto("Nome do jogador: ")
    if nome == "":
        print("\nNome invalido.")
    else:
        print("\n" + controller.registar(nome))
    _pausa()


def _jogos_gravados():
    """Lista ficheiros que parecem ter sido gravados pelo jogo."""
    jogos = []
    for nome_ficheiro in os.listdir("."):
        if not nome_ficheiro.endswith(".txt"):
            continue
        try:
            with open(nome_ficheiro, "r", encoding="utf-8") as ficheiro:
                conteudo = ficheiro.read()
        except OSError:
            continue
        if '"jogadores"' in conteudo and '"jogo"' in conteudo:
            jogos.append(nome_ficheiro[:-4])
    return sorted(jogos)


def _continuar_jogo_gravado():
    """Mostra os jogos gravados e carrega o jogo escolhido."""
    while True:
        _limpar_ecra()
        print("========================================")
        print("          JOGOS GRAVADOS")
        print("========================================")

        jogos = _jogos_gravados()
        if jogos:
            for indice, nome in enumerate(jogos, 1):
                print(str(indice) + " - " + nome)
        else:
            print("Nao existem jogos gravados.")

        print("0 - Voltar")
        print("========================================")

        escolha = _ler_texto("Escolha o jogo a continuar: ")
        if escolha == "0":
            return

        if escolha.isdigit():
            indice = int(escolha)
            if 1 <= indice <= len(jogos):
                resultado = controller.ler(jogos[indice - 1])
                print("\n" + resultado)
                _pausa()
                if controller.jogo_em_curso():
                    _ecra_jogo()
                return

        print("\nOpcao invalida.")
        _pausa()


def _selecionar_ou_registar_jogador(titulo, excluir=None):
    """Permite escolher um jogador existente ou registar um novo."""
    if excluir is None:
        excluir = []

    while True:
        _limpar_ecra()
        print("========================================")
        print(titulo)
        print("========================================")

        jogadores = []
        for nome in controller.nomes_jogadores(excluir_cpu=True):
            if nome not in excluir:
                jogadores.append(nome)

        if jogadores:
            for indice, nome in enumerate(jogadores, 1):
                print(str(indice) + " - " + nome)
        else:
            print("Ainda nao existem jogadores humanos disponiveis.")

        print("N - Registar novo jogador")
        print("0 - Cancelar")
        print("========================================")

        escolha = _ler_texto("Escolha: ")
        if escolha == "0":
            return None

        if escolha.upper() == "N":
            nome = _ler_texto("Nome do novo jogador: ")
            if nome == "":
                print("\nNome invalido.")
                _pausa()
                continue
            resultado = controller.registar(nome)
            print("\n" + resultado)
            if resultado == "Jogador registado com sucesso.":
                _pausa()
                return nome
            _pausa()
            continue

        if escolha.isdigit():
            indice = int(escolha)
            if 1 <= indice <= len(jogadores):
                return jogadores[indice - 1]

        print("\nOpcao invalida.")
        _pausa()


def _selecionar_nivel_cpu():
    """Pergunta qual o nivel de dificuldade do CPU."""
    while True:
        _limpar_ecra()
        print("========================================")
        print("             NIVEL DO CPU")
        print("========================================")
        print("1 - Normal")
        print("2 - Avancado")
        print("0 - Cancelar")
        print("========================================")

        escolha = _ler_texto("Escolha: ")
        if escolha == "1":
            return "Normal"
        if escolha == "2":
            return "Avançado"
        if escolha == "0":
            return None

        print("\nOpcao invalida.")
        _pausa()


def _novo_jogo_humano():
    """Cria um jogo entre dois jogadores humanos."""
    jogador_a = _selecionar_ou_registar_jogador("JOGADOR A")
    if jogador_a is None:
        return

    jogador_b = _selecionar_ou_registar_jogador("JOGADOR B", excluir=[jogador_a])
    if jogador_b is None:
        return

    resultado = controller.iniciar(jogador_a, jogador_b)
    print("\n" + resultado)
    if resultado == "Jogo iniciado com sucesso.":
        _pausa()
        _ecra_jogo()
    else:
        _pausa()


def _novo_jogo_cpu():
    """Cria um jogo entre um jogador humano e o CPU."""
    jogador = _selecionar_ou_registar_jogador("JOGADOR HUMANO")
    if jogador is None:
        return

    nivel = _selecionar_nivel_cpu()
    if nivel is None:
        return

    resultado = controller.iniciar_auto(jogador, nivel)
    print("\n" + resultado)
    if resultado == "Jogo automático de nível " + nivel + " iniciado com sucesso.":
        _pausa()
        _ecra_jogo()
    else:
        _pausa()


def _menu_novo_jogo():
    """Controla o submenu de escolha do tipo de jogo."""
    if controller.jogo_em_curso():
        print("\nJa existe um jogo em curso.")
        _pausa()
        return

    while True:
        _mostrar_menu_novo_jogo()
        escolha = _ler_texto("Escolha: ")
        if escolha == "1":
            _novo_jogo_humano()
            return
        if escolha == "2":
            _novo_jogo_cpu()
            return
        if escolha == "0":
            return

        print("\nOpcao invalida.")
        _pausa()


def _valor(tabuleiro, chave):
    """Obtem um valor do tabuleiro para facilitar o desenho."""
    return str(tabuleiro.get(chave, 0)).rjust(2)


def _desenhar_tabuleiro():
    """Desenha uma representacao visual do tabuleiro no terminal."""
    tabuleiro = controller.dados_tabuleiro()
    if tabuleiro == {}:
        print("Nao existe jogo em curso.")
        return

    jogador_a = tabuleiro["JogadorA"]
    jogador_b = tabuleiro["JogadorB"]
    vez = tabuleiro.get("Vez")

    print("========================================")
    print("              TABULEIRO")
    print("========================================")
    print("Vez: " + str(vez))
    print()
    print("          " + jogador_b)
    print("       6    5    4    3    2    1")
    print("    +----+----+----+----+----+----+")
    print(
        "    | "
        + _valor(tabuleiro, "B6")
        + " | "
        + _valor(tabuleiro, "B5")
        + " | "
        + _valor(tabuleiro, "B4")
        + " | "
        + _valor(tabuleiro, "B3")
        + " | "
        + _valor(tabuleiro, "B2")
        + " | "
        + _valor(tabuleiro, "B1")
        + " |"
    )
    print("+---+----+----+----+----+----+----+---+")
    print(
        "| "
        + _valor(tabuleiro, "B7")
        + " |                         | "
        + _valor(tabuleiro, "A7")
        + " |"
    )
    print("+---+----+----+----+----+----+----+---+")
    print(
        "    | "
        + _valor(tabuleiro, "A1")
        + " | "
        + _valor(tabuleiro, "A2")
        + " | "
        + _valor(tabuleiro, "A3")
        + " | "
        + _valor(tabuleiro, "A4")
        + " | "
        + _valor(tabuleiro, "A5")
        + " | "
        + _valor(tabuleiro, "A6")
        + " |"
    )
    print("    +----+----+----+----+----+----+")
    print("       1    2    3    4    5    6")
    print("          " + jogador_a)
    print()
    print("Pocos: " + jogador_b + "=" + str(tabuleiro["B7"]) + " | " + jogador_a + "=" + str(tabuleiro["A7"]))
    print("========================================")


def _ecra_jogo():
    """Mostra o tabuleiro e permite jogar ate o jogo terminar ou voltar ao menu."""
    mensagem = ""

    while controller.jogo_em_curso():
        _limpar_ecra()
        _desenhar_tabuleiro()
        if mensagem != "":
            print("\n" + mensagem)

        jogador = controller.jogador_da_vez()
        print()
        print("1-6 - Jogar casa")
        print("G   - Gravar jogo")
        print("D   - Desistir")
        print("M   - Voltar ao menu principal")
        escolha = _ler_texto("Escolha de " + str(jogador) + ": ")

        if escolha.upper() == "M":
            return

        if escolha.upper() == "G":
            ficheiro = _ler_texto("Nome do ficheiro: ")
            mensagem = controller.gravar(ficheiro)
            continue

        if escolha.upper() == "D":
            mensagem = controller.desistir(["D", jogador])
            _limpar_ecra()
            print(mensagem)
            _pausa()
            return

        if escolha.isdigit() and 1 <= int(escolha) <= 6:
            mensagem = controller.jogada(jogador, escolha)
            if not controller.jogo_em_curso():
                _limpar_ecra()
                print(mensagem)
                _pausa()
                return
            continue

        mensagem = "Opcao invalida."


def _menu_principal_interativo():
    """Controla o menu principal usado quando o programa corre no terminal."""
    while True:
        _mostrar_menu_principal()
        escolha = _ler_texto("Escolha: ")

        if escolha == "1":
            _menu_novo_jogo()
        elif escolha == "2":
            _continuar_jogo_gravado()
        elif escolha == "3":
            _registar_jogador_menu()
        elif escolha == "4":
            _mostrar_jogadores()
            _pausa()
        elif escolha == "0":
            return
        else:
            print("\nOpcao invalida.")
            _pausa()


def comando(instrucao):
    """Recebe uma instrucao textual e chama a funcao correspondente."""
    if instrucao[0] == "RJ" and len(instrucao) == 2:
        return controller.registar(instrucao[1])

    elif instrucao[0] == "LJ" and len(instrucao) == 1:
        return controller.listar()

    elif instrucao[0] == "IJ" and len(instrucao) == 3:
        return controller.iniciar(instrucao[1], instrucao[2])

    elif instrucao[0] == "IJA" and len(instrucao) == 3:
        return controller.iniciar_auto(instrucao[1], instrucao[2])

    elif instrucao[0] == "DJ" and len(instrucao) == 1:
        return controller.detalhes()

    elif instrucao[0] == "J" and len(instrucao) == 3:
        return controller.jogada(instrucao[1], instrucao[2])

    elif instrucao[0] == "D" and len(instrucao) > 1 and len(instrucao) <= 3:
        return controller.desistir(instrucao)

    elif instrucao[0] == "G" and len(instrucao) == 2:
        return controller.gravar(instrucao[1])

    elif instrucao[0] == "L" and len(instrucao) == 2:
        return controller.ler(instrucao[1])

    else:
        return "Instrução inválida."


def main():
    """Arranca o programa em modo menu ou em modo comandos redirecionados."""
    if sys.stdin.isatty():
        _menu_principal_interativo()
        return

    while True:
        inserir = input()
        if inserir == "":
            break
        print(comando(inserir.split()))
