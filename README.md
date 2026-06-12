# Mancala

Projeto em Python que implementa uma versao de terminal do jogo Mancala.

O programa permite jogar entre dois jogadores humanos ou contra um jogador automatico (`CPU`). A interface principal e feita por menus no terminal e apresenta um tabuleiro visual atualizado a cada jogada.

## Funcionalidades

- Registo de jogadores.
- Listagem de jogadores e estatisticas.
- Novo jogo entre dois jogadores humanos.
- Novo jogo contra CPU.
- Dois niveis de CPU: `Normal` e `Avancado`.
- Tabuleiro desenhado no terminal.
- Jogadas feitas diretamente no ecra do jogo, escolhendo casas de `1` a `6`.
- Gravacao de jogos durante uma partida.
- Listagem de jogos gravados para continuar mais tarde.
- Modo por comandos mantido para testes de input/output.

## Regras do jogo

O tabuleiro tem duas filas de seis casas. Cada casa comeca com quatro sementes.

Em cada jogada, o jogador escolhe uma casa da sua fila. As sementes dessa casa sao distribuidas uma a uma pelas casas seguintes, pelo proprio poco e pela fila adversaria, sem colocar sementes no poco do adversario.

Regras especiais:

- Se a ultima semente cair no proprio poco, o jogador tem direito a outra jogada.
- Se a ultima semente cair numa casa vazia da propria fila, o jogador captura essa semente e as sementes da casa oposta do adversario.
- O jogo termina quando uma das filas fica sem sementes.
- As sementes restantes da outra fila sao colocadas no poco correspondente.
- Vence quem tiver mais sementes no poco.

## Como executar

Abrir um terminal na pasta do projeto:

```powershell
cd C:\Github\mancala
```

Executar:

```powershell
python program.py
```

No VS Code, abre a pasta `C:\Github\mancala`, confirma que tens um Python Interpreter selecionado e corre o comando acima no terminal integrado.

## Menu principal

Ao iniciar o programa no terminal, aparece o menu:

```text
1 - Novo jogo
2 - Continuar jogo gravado
3 - Registar jogador
4 - Jogadores registados
0 - Sair
```

### Novo jogo

Permite escolher:

- Jogador contra jogador.
- Jogador contra CPU.

Durante a criacao do jogo, o programa mostra os jogadores registados e permite selecionar um deles ou registar um novo.

No jogo contra CPU, tambem e pedido o nivel:

- `Normal`
- `Avancado`

### Durante o jogo

O terminal mostra o tabuleiro e as opcoes:

```text
1-6 - Jogar casa
G   - Gravar jogo
D   - Desistir
M   - Voltar ao menu principal
```

A opcao `G` grava o jogo atual num ficheiro `.txt`. Os jogos gravados ficam disponiveis no menu `Continuar jogo gravado`.

## Estrutura do projeto

```text
mancala
|-- program.py        # Ponto de entrada do programa
|-- cli.py            # Menus, interface de terminal e modo por comandos
|-- controller.py     # Logica do jogo, jogadores, CPU e gravacao/leitura
|-- model.py          # Estado global do jogo e dos jogadores
|-- iotests/          # Testes publicos de input/output
|-- figures/          # Imagens do enunciado original
|-- REPORT.md         # Relatorio do projeto
```

## Modo por comandos

Apesar da interface por menus, o programa continua a aceitar comandos quando recebe input redirecionado. Isto permite executar os testes existentes.

Exemplo:

```powershell
python program.py < iotests\1.in
```

Tambem e possivel guardar a saida:

```powershell
python program.py < iotests\1.in > 1.mine.out
```

## Comandos suportados no modo de testes

```text
RJ NomeJogador
LJ
IJ NomeJogadorA NomeJogadorB
IJA NomeJogador Nivel
DJ
J NomeJogador Posicao
D NomeJogador
D NomeJogador NomeJogador
G NomeFicheiro
L NomeFicheiro
```

## Requisitos

- Python 3
- Nao sao usadas bibliotecas externas.

## Estado atual dos testes

Os testes publicos de input/output continuam disponiveis na pasta `iotests`.

No estado atual:

- `iotests\1` passa.
- `iotests\2` passa.
- `iotests\6` passa.
- `iotests\3`, `iotests\4` e `iotests\5` ainda diferem em sequencias ligadas ao CPU e a jogadas consideradas invalidas pela implementacao atual.

## Autores

Ver `REPORT.md`.
