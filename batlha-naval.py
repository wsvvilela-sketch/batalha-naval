#importa função que sera utilizada nas escolhas na máquina
import random

# =========================
# CONSTANTES
# =========================
# O mapa é um tabuleiro 2D de verdade: 10 linhas x 10 colunas = 100
# células (tamanho padrão de batalha naval).
LINHAS = 10
COLUNAS = 10
TAMANHO_MAPA = LINHAS * COLUNAS

TAMANHOS_BARCOS = [2, 5, 8, 9]
QUANTIDADE_INICIAL_BARCOS = {2: 2, 5: 3, 8: 2, 9: 1}

VAZIO = 0
ATINGIDO = 1

HORIZONTAL = "H"
VERTICAL = "V"
ORIENTACOES_VALIDAS = [HORIZONTAL, VERTICAL]

# Símbolos usados na exibição do tabuleiro em grade
SIMBOLO_AGUA = "."          # célula ainda não atingida (mapa próprio)
SIMBOLO_DESCONHECIDO = "?"  # célula ainda não atingida no mapa do oponente (oculta)
SIMBOLO_BARCO = "#"         # barco próprio, ainda não atingido
SIMBOLO_ACERTO = "X"        # célula atingida que tinha barco
SIMBOLO_ERRO = "O"          # célula atingida que estava vazia


# =========================
# FUNÇÕES DE TABULEIRO / POSICIONAMENTO
# (compartilhadas entre jogador e máquina)
# =========================

def criar_mapa():
    """Cria um mapa vazio (lista de zeros) representando o tabuleiro 10x10."""
    return [VAZIO] * TAMANHO_MAPA


def coordenada_para_indice(linha, coluna):
    """Converte uma coordenada (linha, coluna) no índice equivalente da lista."""
    return linha * COLUNAS + coluna


def cabe_no_mapa(linha, coluna, tamanho_barco, orientacao):
    """
    Checa se um barco cabe no tabuleiro a partir de (linha, coluna),
    respeitando a orientação (horizontal cresce em coluna, vertical cresce em linha).
    """
    if not (0 <= linha < LINHAS and 0 <= coluna < COLUNAS):
        return False

    if orientacao == HORIZONTAL:
        return coluna + tamanho_barco <= COLUNAS
    elif orientacao == VERTICAL:
        return linha + tamanho_barco <= LINHAS

    return False


def indices_do_barco(linha, coluna, tamanho_barco, orientacao):
    """Retorna a lista de índices que o barco ocuparia, dado o ponto inicial e orientação."""
    indices = []
    for i in range(tamanho_barco):
        if orientacao == HORIZONTAL:
            indices.append(coordenada_para_indice(linha, coluna + i))
        else:  # VERTICAL
            indices.append(coordenada_para_indice(linha + i, coluna))
    return indices


def posicao_livre(mapa, indices):
    """Checa se todas as células que o barco ocuparia estão livres."""
    return all(mapa[i] == VAZIO for i in indices)


def posicionar_barco(mapa, indices, tamanho_barco):
    """Marca no mapa as células ocupadas pelo barco."""
    for i in indices:
        mapa[i] = tamanho_barco


def barcos_restantes(quantidades):
    """Retorna True se ainda houver algum barco para posicionar."""
    return any(qtd > 0 for qtd in quantidades.values())


def existem_barcos(mapa):
    """Checa se ainda existe algum barco não completamente afundado no mapa."""
    return any(x in TAMANHOS_BARCOS for x in mapa)


# =========================
# EXIBIÇÃO DO TABULEIRO EM GRADE
# =========================
# Antes, cada jogada terminava com um print(mapa) cru (a lista Python
# inteira, ex: [0, 0, 8, 8, 0, 5, ...]), difícil de ler e sem noção de
# linha/coluna. Agora o tabuleiro é desenhado como uma grade com colunas
# A, B, C... e linhas numeradas, parecido com batalha naval de tabuleiro
# físico.

def letra_coluna(coluna):
    """Converte o índice da coluna (0, 1, 2...) para letra (A, B, C...)."""
    return chr(ord("A") + coluna)


def imprimir_tabuleiro(titulo, simbolos):
    """Desenha um tabuleiro a partir de uma lista de símbolos (um por célula)."""
    print(f"\n{titulo}")
    cabecalho = "    " + " ".join(letra_coluna(c) for c in range(COLUNAS))
    print(cabecalho)
    for linha in range(LINHAS):
        inicio = linha * COLUNAS
        fim = inicio + COLUNAS
        celulas = " ".join(simbolos[inicio:fim])
        # right-align no número da linha para colunas de dois dígitos alinharem certo
        print(f"{linha + 1:>2}  {celulas}")


def simbolos_posicionamento(mapa):
    """Símbolos do tabuleiro durante a fase de posicionamento (sem tiros ainda)."""
    return [SIMBOLO_BARCO if mapa[i] in TAMANHOS_BARCOS else SIMBOLO_AGUA for i in range(TAMANHO_MAPA)]


def simbolos_mapa_proprio(mapa, historico_tiros_recebidos):
    """
    Símbolos do tabuleiro do próprio jogador durante a partida: mostra os
    barcos, e onde a máquina já acertou ou errou.
    'historico_tiros_recebidos[i]' guarda o valor da célula ANTES de ser
    atingida (necessário porque, ao ser atingida, a célula é sobrescrita
    com ATINGIDO e perderia essa informação).
    """
    simbolos = []
    for i in range(TAMANHO_MAPA):
        if mapa[i] == ATINGIDO:
            if historico_tiros_recebidos[i] in TAMANHOS_BARCOS:
                simbolos.append(SIMBOLO_ACERTO)
            else:
                simbolos.append(SIMBOLO_ERRO)
        elif mapa[i] in TAMANHOS_BARCOS:
            simbolos.append(SIMBOLO_BARCO)
        else:
            simbolos.append(SIMBOLO_AGUA)
    return simbolos


def simbolos_mapa_oponente(mapa, historico_tiros_dados):
    """
    Símbolos do tabuleiro do oponente, como o jogador o vê: células ainda
    não atingidas aparecem como '?' (o jogador NÃO sabe se há barco ali),
    e só as células já atingidas revelam acerto ou erro.
    """
    simbolos = []
    for i in range(TAMANHO_MAPA):
        if mapa[i] == ATINGIDO:
            if historico_tiros_dados[i] in TAMANHOS_BARCOS:
                simbolos.append(SIMBOLO_ACERTO)
            else:
                simbolos.append(SIMBOLO_ERRO)
        else:
            simbolos.append(SIMBOLO_DESCONHECIDO)
    return simbolos


# =========================
# POSICIONAMENTO - JOGADOR
# =========================

def ler_orientacao():
    """Lê e valida a orientação do barco (H = horizontal, V = vertical)."""
    return input("Orientação do barco (H = horizontal, V = vertical): ").strip().upper()


def posicionamento_jogador():
    """Loop de posicionamento de barcos controlado pelo jogador via input()."""
    mapa = criar_mapa()
    quantidades = QUANTIDADE_INICIAL_BARCOS.copy()

    print("=== Posicionamento dos seus barcos ===")

    while barcos_restantes(quantidades):
        pendentes = ", ".join(f"{tam}x{qtd}" for tam, qtd in quantidades.items() if qtd > 0)
        print(f"Barcos restantes: {pendentes}")

        tipo_barco = int(input(f"Escolha o tamanho do barco {TAMANHOS_BARCOS}: "))

        if tipo_barco not in TAMANHOS_BARCOS:
            print("Tamanho inválido")
            continue

        if quantidades[tipo_barco] == 0:
            print("Esse barco já acabou")
            continue

        linha = int(input(f"Escolha a linha (1 a {LINHAS}): ")) - 1
        coluna_letra = input(f"Escolha a coluna (A a {letra_coluna(COLUNAS - 1)}): ").strip().upper()
        orientacao = ler_orientacao()

        if not coluna_letra or not ("A" <= coluna_letra <= letra_coluna(COLUNAS - 1)):
            print("Coluna inválida")
            continue

        coluna = ord(coluna_letra) - ord("A")

        if orientacao not in ORIENTACOES_VALIDAS:
            print("Orientação inválida (use H ou V)")
            continue

        if not cabe_no_mapa(linha, coluna, tipo_barco, orientacao):
            print("Não cabe no mapa")
            continue

        indices = indices_do_barco(linha, coluna, tipo_barco, orientacao)

        if not posicao_livre(mapa, indices):
            print("Espaço ocupado")
            continue

        posicionar_barco(mapa, indices, tipo_barco)
        quantidades[tipo_barco] -= 1

        print("Barco colocado!")
        imprimir_tabuleiro("Seu tabuleiro", simbolos_posicionamento(mapa))

    return mapa


# =========================
# POSICIONAMENTO - MÁQUINA
# =========================

def posicoes_validas_para_barco(mapa, tamanho_barco):
    """
    Retorna todas as combinações válidas (lista de índices) onde o barco
    cabe e está livre, considerando as duas orientações possíveis.
    """
    validas = []
    for linha in range(LINHAS):
        for coluna in range(COLUNAS):
            for orientacao in ORIENTACOES_VALIDAS:
                if cabe_no_mapa(linha, coluna, tamanho_barco, orientacao):
                    indices = indices_do_barco(linha, coluna, tamanho_barco, orientacao)
                    if posicao_livre(mapa, indices):
                        validas.append(indices)
    return validas


def posicionamento_maquina():
    """Loop de posicionamento de barcos controlado aleatoriamente pela máquina."""
    mapa = criar_mapa()
    quantidades = QUANTIDADE_INICIAL_BARCOS.copy()

    while barcos_restantes(quantidades):
        tipo_barco = random.choice(TAMANHOS_BARCOS)

        if quantidades[tipo_barco] == 0:
            continue

        validas = posicoes_validas_para_barco(mapa, tipo_barco)

        if len(validas) > 0:
            indices = random.choice(validas)
            posicionar_barco(mapa, indices, tipo_barco)
            quantidades[tipo_barco] -= 1
        else:
            quantidades[tipo_barco] = 0

    return mapa


# =========================
# RODADAS DO JOGO
# =========================

def turno_jogador(mapa_maquina, historico_tiros_dados):
    """
    Processa a jogada do jogador: escolhe uma linha/coluna no tabuleiro da
    máquina. 'historico_tiros_dados' guarda o valor original da célula no
    momento do tiro, usado só para exibição (ver simbolos_mapa_oponente).
    """
    while True:
        linha = int(input(f"Escolha a linha (1 a {LINHAS}): ")) - 1
        coluna_letra = input(f"Escolha a coluna (A a {letra_coluna(COLUNAS - 1)}): ").strip().upper()
        coluna = ord(coluna_letra) - ord("A") if coluna_letra else -1

        if not (0 <= linha < LINHAS and 0 <= coluna < COLUNAS):
            print("Opção inválida")
            continue

        indice = coordenada_para_indice(linha, coluna)

        if mapa_maquina[indice] == ATINGIDO:
            print("Você já atirou aí")
            continue

        if mapa_maquina[indice] > 1:
            print(f"Jogador atirou em {letra_coluna(coluna)}{linha + 1}: Acertou!")
        else:
            print(f"Jogador atirou em {letra_coluna(coluna)}{linha + 1}: Errou!")

        historico_tiros_dados[indice] = mapa_maquina[indice]
        mapa_maquina[indice] = ATINGIDO
        break


def turno_maquina(mapa_jogador, historico_tiros_recebidos):
    """
    Processa a jogada da máquina: escolhe aleatoriamente uma célula não
    atingida. 'historico_tiros_recebidos' guarda o valor original da
    célula no momento do tiro, usado só para exibição (simbolos_mapa_proprio).
    """
    while True:
        linha = random.randint(0, LINHAS - 1)
        coluna = random.randint(0, COLUNAS - 1)
        indice = coordenada_para_indice(linha, coluna)

        if mapa_jogador[indice] != ATINGIDO:
            if mapa_jogador[indice] > 1:
                print(f"Máquina atirou em {letra_coluna(coluna)}{linha + 1}: Acertou!")
            else:
                print(f"Máquina atirou em {letra_coluna(coluna)}{linha + 1}: Errou!")

            historico_tiros_recebidos[indice] = mapa_jogador[indice]
            mapa_jogador[indice] = ATINGIDO
            break


# =========================
# FLUXO PRINCIPAL
# =========================

def main():
    mapa_jogador = posicionamento_jogador()
    mapa_maquina = posicionamento_maquina()

    # históricos usados só para exibição (ver comentário nas funções de turno)
    historico_tiros_dados = criar_mapa()       # tiros do jogador no mapa da máquina
    historico_tiros_recebidos = criar_mapa()   # tiros da máquina no mapa do jogador

    print("\n=== Início da partida ===")

    while existem_barcos(mapa_jogador) and existem_barcos(mapa_maquina):
        turno_jogador(mapa_maquina, historico_tiros_dados)
        turno_maquina(mapa_jogador, historico_tiros_recebidos)

        # o tabuleiro só é redesenhado uma vez por rodada (não a cada
        # mensagem de acerto/erro), reduzindo a poluição visual
        imprimir_tabuleiro("Seu tabuleiro", simbolos_mapa_proprio(mapa_jogador, historico_tiros_recebidos))
        imprimir_tabuleiro("Tabuleiro da máquina", simbolos_mapa_oponente(mapa_maquina, historico_tiros_dados))

    print()
    if existem_barcos(mapa_jogador):
        print("Jogador venceu!")
    else:
        print("Máquina venceu!")


if __name__ == "__main__":
    main()