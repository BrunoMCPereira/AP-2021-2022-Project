import json
from os import path

import model


def _cpu():
    """Garante que o jogador automatico CPU existe na lista de jogadores."""
    if not _existe_jogador("CPU"):
        model.jogadores.append(_novo_jogador("CPU"))


def _novo_jogador(nome):
    """Cria a estrutura inicial de estatisticas para um jogador."""
    return {
        "Jogador": nome,
        "Jogos": 0,
        "Vitorias": 0,
        "Empates": 0,
        "Derrotas": 0,
    }


def _existe_jogador(nome):
    """Indica se um jogador ja esta registado."""
    for jogador in model.jogadores:
        if jogador["Jogador"] == nome:
            return True
    return False


def _obter_jogador(nome):
    """Procura e devolve o dicionario de um jogador registado."""
    for jogador in model.jogadores:
        if jogador["Jogador"] == nome:
            return jogador
    return None


def _lado_do_jogador(nome):
    """Devolve o lado do tabuleiro ocupado pelo jogador: A, B ou None."""
    if model.jogo.get("JogadorA") == nome:
        return "A"
    if model.jogo.get("JogadorB") == nome:
        return "B"
    return None


def _oponente(lado):
    """Devolve o lado adversario ao lado recebido."""
    if lado == "A":
        return "B"
    return "A"


def _casa(lado, pos):
    """Gera a chave usada para representar uma casa do tabuleiro."""
    return lado + str(pos)


def _poco(lado):
    """Gera a chave usada para representar o poco de um jogador."""
    return lado + "7"


def _casas(lado):
    """Devolve as seis casas normais de um lado do tabuleiro."""
    return [_casa(lado, pos) for pos in range(1, 7)]


def _linha_vazia(lado):
    """Verifica se uma das filas do tabuleiro ficou sem sementes."""
    for casa in _casas(lado):
        if model.jogo[casa] != 0:
            return False
    return True


def _somar_linha_ao_poco(lado):
    """Move todas as sementes de uma fila para o respetivo poco."""
    total = 0
    for casa in _casas(lado):
        total += model.jogo[casa]
        model.jogo[casa] = 0
    model.jogo[_poco(lado)] += total


def _sequencia(lado):
    """Calcula a ordem de distribuicao das sementes para uma jogada."""
    outro = _oponente(lado)
    return _casas(lado) + [_poco(lado)] + _casas(outro)


def _trocar_vez(lado):
    """Passa a vez para o jogador adversario."""
    outro = _oponente(lado)
    model.jogo["Vez"] = model.jogo["Jogador" + outro]


def _mensagem_fim():
    """Monta a mensagem apresentada quando o jogo termina."""
    return (
        "Jogo terminado.\n"
        + model.jogo["JogadorA"]
        + " "
        + str(model.jogo["A7"])
        + "\n"
        + model.jogo["JogadorB"]
        + " "
        + str(model.jogo["B7"])
    )


def _registar_resultado():
    """Atualiza vitorias, derrotas ou empates quando o jogo acaba."""
    pontos_a = model.jogo["A7"]
    pontos_b = model.jogo["B7"]

    if pontos_a > pontos_b:
        _adicionar_vitoria(model.jogo["JogadorA"])
        _adicionar_derrota(model.jogo["JogadorB"])
    elif pontos_b > pontos_a:
        _adicionar_vitoria(model.jogo["JogadorB"])
        _adicionar_derrota(model.jogo["JogadorA"])
    else:
        _adicionar_empate(model.jogo["JogadorA"])
        _adicionar_empate(model.jogo["JogadorB"])


def _adicionar_vitoria(nome):
    """Soma um jogo e uma vitoria ao jogador indicado."""
    jogador = _obter_jogador(nome)
    if jogador is not None:
        jogador["Jogos"] += 1
        jogador["Vitorias"] += 1


def _adicionar_derrota(nome):
    """Soma um jogo e uma derrota ao jogador indicado."""
    jogador = _obter_jogador(nome)
    if jogador is not None:
        jogador["Jogos"] += 1
        jogador["Derrotas"] += 1


def _adicionar_empate(nome):
    """Soma um jogo e um empate ao jogador indicado."""
    jogador = _obter_jogador(nome)
    if jogador is not None:
        jogador["Jogos"] += 1
        jogador["Empates"] += 1


def _terminar_se_necessario():
    """Fecha o jogo se uma das filas estiver vazia apos uma jogada."""
    if not _linha_vazia("A") and not _linha_vazia("B"):
        return None

    if _linha_vazia("A"):
        _somar_linha_ao_poco("B")
    if _linha_vazia("B"):
        _somar_linha_ao_poco("A")

    mensagem = _mensagem_fim()
    _registar_resultado()
    model.jogo = {}
    return mensagem


def _jogar_lado(lado, pos):
    """Executa uma jogada completa para um dos lados do tabuleiro."""
    casa_inicial = _casa(lado, pos)
    sementes = model.jogo[casa_inicial]
    model.jogo[casa_inicial] = 0

    percurso = _sequencia(lado)
    indice = percurso.index(casa_inicial)
    ultima = casa_inicial

    while sementes > 0:
        indice = (indice + 1) % len(percurso)
        ultima = percurso[indice]
        model.jogo[ultima] += 1
        sementes -= 1

    outro = _oponente(lado)
    if ultima in _casas(lado) and model.jogo[ultima] == 1:
        pos_ultima = int(ultima[1])
        casa_oposta = _casa(outro, 7 - pos_ultima)
        if model.jogo[casa_oposta] > 0:
            capturadas = model.jogo[casa_oposta] + model.jogo[ultima]
            model.jogo[casa_oposta] = 0
            model.jogo[ultima] = 0
            model.jogo[_poco(lado)] += capturadas

    fim = _terminar_se_necessario()
    if fim is not None:
        return fim

    if ultima == _poco(lado):
        return "O jogador " + model.jogo["Jogador" + lado] + " tem direito a outra jogada."

    _trocar_vez(lado)
    return None


def _criar_jogo(jogador_a, jogador_b, nivel=None):
    """Inicializa um novo tabuleiro com quatro sementes por casa."""
    model.jogo = {
        "JogadorA": jogador_a,
        "A1": 4,
        "A2": 4,
        "A3": 4,
        "A4": 4,
        "A5": 4,
        "A6": 4,
        "A7": 0,
        "JogadorB": jogador_b,
        "B1": 4,
        "B2": 4,
        "B3": 4,
        "B4": 4,
        "B5": 4,
        "B6": 4,
        "B7": 0,
        "Vez": jogador_a,
    }
    if nivel is not None:
        model.jogo["Nivel"] = nivel


def jogo_em_curso():
    """Indica se existe um jogo ativo neste momento."""
    return model.jogo != {}


def nomes_jogadores(excluir_cpu=False):
    """Devolve os nomes dos jogadores registados."""
    nomes = []
    for jogador in model.jogadores:
        if excluir_cpu and jogador["Jogador"] == "CPU":
            continue
        nomes.append(jogador["Jogador"])
    return nomes


def jogador_da_vez():
    """Devolve o nome do jogador que deve jogar agora."""
    if model.jogo == {}:
        return None
    return model.jogo.get("Vez")


def jogo_contra_cpu():
    """Indica se o jogo ativo e contra o CPU."""
    return model.jogo != {} and model.jogo.get("JogadorB") == "CPU"


def dados_tabuleiro():
    """Devolve uma copia simples dos dados necessarios para desenhar o tabuleiro."""
    if model.jogo == {}:
        return {}
    return dict(model.jogo)


def registar(player):
    """Regista um novo jogador humano."""
    if _existe_jogador(player):
        return "Jogador existente."
    if len(model.jogadores) == 0:
        _cpu()
    model.jogadores.append(_novo_jogador(player))
    return "Jogador registado com sucesso."


def listar():
    """Lista jogadores ordenados por vitorias e depois por nome."""
    _cpu()
    jogadores = sorted(model.jogadores, key=lambda jogador: (-jogador["Vitorias"], jogador["Jogador"]))
    linhas = []
    for jogador in jogadores:
        linhas.append(
            jogador["Jogador"]
            + " "
            + str(jogador["Jogos"])
            + " "
            + str(jogador["Vitorias"])
            + " "
            + str(jogador["Empates"])
            + " "
            + str(jogador["Derrotas"])
        )
    model.jogadores = jogadores
    return "\n".join(linhas)


def iniciar(jogador_a, jogador_b):
    """Inicia um jogo entre dois jogadores registados."""
    if model.jogo != {}:
        return "Existe um jogo em curso."
    if not _existe_jogador(jogador_a) or not _existe_jogador(jogador_b) or jogador_a == jogador_b:
        return "Jogador inexistente."

    _criar_jogo(jogador_a, jogador_b)
    return "Jogo iniciado com sucesso."


def iniciar_auto(jogador, nivel):
    """Inicia um jogo entre um jogador humano e o CPU."""
    if model.jogo != {}:
        return "Existe um jogo em curso."
    if not _existe_jogador(jogador):
        return "Jogador inexistente."

    _cpu()
    _criar_jogo(jogador, "CPU", nivel)
    return "Jogo automático de nível " + nivel + " iniciado com sucesso."


def detalhes():
    """Mostra o estado atual do tabuleiro no formato do enunciado."""
    if model.jogo == {}:
        return "Não existe jogo em curso."

    linha_a = model.jogo["JogadorA"]
    for pos in range(1, 7):
        linha_a += " [" + str(model.jogo[_casa("A", pos)]) + "]"
    linha_a += " (" + str(model.jogo["A7"]) + ")"

    linha_b = model.jogo["JogadorB"]
    for pos in range(1, 7):
        linha_b += " [" + str(model.jogo[_casa("B", pos)]) + "]"
    linha_b += " (" + str(model.jogo["B7"]) + ")"

    return linha_a + "\n" + linha_b


def _posicao_valida(lado, pos):
    """Confirma se a casa escolhida existe e tem sementes."""
    return 1 <= pos <= 6 and model.jogo[_casa(lado, pos)] > 0


def _escolha_cpu_normal():
    """Escolhe a jogada do CPU no nivel Normal."""
    for pos in range(6, 0, -1):
        if model.jogo[_casa("B", pos)] > 0:
            return pos
    return None


def _simular_jogada(lado, pos):
    """Simula uma jogada e restaura o estado original do jogo."""
    guardado = dict(model.jogo)
    resultado = _jogar_lado(lado, pos)
    simulado = dict(model.jogo)
    model.jogo = guardado
    return resultado, simulado


def _escolha_cpu_avancado():
    """Escolhe a jogada do CPU no nivel Avancado."""
    for pos in range(6, 0, -1):
        if model.jogo[_casa("B", pos)] == 0:
            continue
        antes = model.jogo["B7"]
        _, simulado = _simular_jogada("B", pos)
        if simulado.get("B7", 0) > antes + 1:
            return pos

    for pos in range(6, 0, -1):
        if model.jogo[_casa("B", pos)] == 0:
            continue
        resultado, _ = _simular_jogada("B", pos)
        if resultado == "O jogador CPU tem direito a outra jogada.":
            return pos

    for pos in range(1, 7):
        if model.jogo[_casa("B", pos)] > 0:
            return pos
    return None


def _jogar_cpu():
    """Executa as jogadas automaticas do CPU quando for a sua vez."""
    while model.jogo != {} and model.jogo.get("JogadorB") == "CPU" and model.jogo.get("Vez") == "CPU":
        if model.jogo.get("Nivel") == "Avançado":
            pos = _escolha_cpu_avancado()
        else:
            pos = _escolha_cpu_normal()

        if pos is None:
            return _terminar_se_necessario()

        resultado = _jogar_lado("B", pos)
        if resultado is not None and resultado != "O jogador CPU tem direito a outra jogada.":
            return resultado
    return None


def jogada(jogador, pos):
    """Valida e executa uma jogada pedida pelo utilizador."""
    if model.jogo == {}:
        return "Não existe jogo em curso."
    if not _existe_jogador(jogador):
        return "Jogador inexistente."

    lado = _lado_do_jogador(jogador)
    if lado is None:
        return "Jogador não participa no jogo em curso."

    pos = int(pos)
    if not _posicao_valida(lado, pos):
        return "Jogada inválida."

    resultado = _jogar_lado(lado, pos)
    if model.jogo != {} and model.jogo.get("JogadorB") == "CPU" and model.jogo.get("Vez") == "CPU":
        resultado_cpu = _jogar_cpu()
        if resultado_cpu is not None:
            resultado = resultado_cpu

    if resultado is not None:
        return resultado
    return "Jogada efetuada com sucesso."


def desistir(instrucao):
    """Termina o jogo por desistência de um ou dois jogadores."""
    if model.jogo == {}:
        return "Não existe jogo em curso."

    nomes = instrucao[1:]
    for nome in nomes:
        if not _existe_jogador(nome):
            return "Jogador inexistente."
    for nome in nomes:
        if _lado_do_jogador(nome) is None:
            return "Jogador não participa no jogo em curso."

    if len(nomes) == 1:
        desistente = nomes[0]
        vencedor = model.jogo["JogadorB"]
        if desistente == vencedor:
            vencedor = model.jogo["JogadorA"]
        _adicionar_derrota(desistente)
        _adicionar_vitoria(vencedor)
    else:
        _adicionar_derrota(nomes[0])
        if nomes[1] != nomes[0]:
            _adicionar_derrota(nomes[1])

    model.jogo = {}
    return "Jogo terminado com sucesso."


def gravar(nome_ficheiro):
    """Guarda jogadores e jogo atual num ficheiro JSON."""
    dados = {
        "jogadores": model.jogadores,
        "jogo": model.jogo,
    }
    with open(nome_ficheiro + ".txt", "w", encoding="utf-8") as ficheiro:
        json.dump(dados, ficheiro, ensure_ascii=False)
    return "Jogo gravado com sucesso."


def ler(nome_ficheiro):
    """Carrega jogadores e jogo atual a partir de um ficheiro JSON."""
    if not path.isfile(nome_ficheiro + ".txt"):
        return "Ficheiro inexistente."

    with open(nome_ficheiro + ".txt", "r", encoding="utf-8") as ficheiro:
        dados = json.load(ficheiro)

    model.jogadores = dados.get("jogadores", [])
    model.jogo = dados.get("jogo", {})
    return "Jogo lido com sucesso."
