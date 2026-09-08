#importa função que sera utilizada nas escolhas na máquina
import random

# =========================
# CONSTANTES
# =========================

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


# =========================
# FUNÇÕES DE TABULEIRO / POSICIONAMENTO
# (compartilhadas entre jogador e máquina)
# =========================

def criar_mapa():
    """Cria um mapa vazio (lista de zeros) representando o tabuleiro 8x8."""
    return [VAZIO] * TAMANHO_MAPA


def coordenada_para_indice(linha, coluna):
    """Converte uma coordenada (linha, coluna) no índice equivalente da lista."""
    return linha * COLUNAS + coluna


def indice_para_coordenada(indice):
    """Converte um índice da lista de volta para (linha, coluna). Útil para prints/depuração."""
    return divmod(indice, COLUNAS)


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


# =========================
# POSICIONAMENTO - JOGADOR
# =========================

def ler_orientacao():
    """Lê e valida a orientação do barco (H = horizontal, V = vertical)."""
    orientacao = input("Orientação do barco (H = horizontal, V = vertical): ").strip().upper()
    return orientacao


def posicionamento_jogador():
    """Loop de posicionamento de barcos controlado pelo jogador via input()."""
    mapa = criar_mapa()
    quantidades = QUANTIDADE_INICIAL_BARCOS.copy()

    while barcos_restantes(quantidades):
        tipo_barco = int(input(f"Escolha o tamanho do barco {TAMANHOS_BARCOS}: "))

        if tipo_barco not in TAMANHOS_BARCOS:
            print("Tamanho inválido")
            continue

        if quantidades[tipo_barco] == 0:
            print("Esse barco já acabou")
            continue

        linha = int(input(f"Escolha a linha (0 a {LINHAS - 1}): "))
        coluna = int(input(f"Escolha a coluna (0 a {COLUNAS - 1}): "))
        orientacao = ler_orientacao()

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
        print(mapa)
        print("Agora tem")
        for tamanho, qtd in quantidades.items():
            print(qtd, f"barco(s) de tamanho {tamanho}")

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
            # se não há posição válida (em nenhuma orientação) para esse barco, desiste dele
            quantidades[tipo_barco] = 0

    return mapa


# =========================
# RODADAS DO JOGO
# =========================

def turno_jogador(mapa_maquina, mapa_escolhas):
    """
    Processa a jogada do jogador: escolhe uma linha/coluna no tabuleiro da
    máquina. O jogador só enxerga mapa_escolhas (o que já foi revelado),
    nunca mapa_maquina completo — assim ele não tem acesso à posição dos
    barcos que ainda não atirou.
    """
    while True:
        linha = int(input(f"Escolha a linha (0 a {LINHAS - 1}): "))
        coluna = int(input(f"Escolha a coluna (0 a {COLUNAS - 1}): "))

        if not (0 <= linha < LINHAS and 0 <= coluna < COLUNAS):
            print("Opção inválida")
            continue

        indice = coordenada_para_indice(linha, coluna)

        if mapa_maquina[indice] == ATINGIDO:
            print("Opção inválida")
            continue

        print(f"Jogador escolheu ({linha}, {coluna})")

        if mapa_maquina[indice] > 1:
            print("Acertou!")
            print("O tamanho do barco acertado é", mapa_maquina[indice])
        else:
            print("Errou!")

        mapa_escolhas[indice] = mapa_maquina[indice]
        mapa_maquina[indice] = ATINGIDO
        print(mapa_escolhas)
        break


def turno_maquina(mapa_jogador):
    """Processa a jogada da máquina: escolhe aleatoriamente uma célula não atingida."""
    while True:
        linha = random.randint(0, LINHAS - 1)
        coluna = random.randint(0, COLUNAS - 1)
        indice = coordenada_para_indice(linha, coluna)

        if mapa_jogador[indice] != ATINGIDO:
            print(f"Máquina escolheu ({linha}, {coluna})")

            if mapa_jogador[indice] > 1:
                print("Máquina acertou!")
            else:
                print("Máquina errou!")

            mapa_jogador[indice] = ATINGIDO
            print(mapa_jogador)
            break


def existem_barcos(mapa):
    """Checa se ainda existe algum barco não completamente afundado no mapa."""
    return any(x in TAMANHOS_BARCOS for x in mapa)


# =========================
# FLUXO PRINCIPAL
# =========================

def main():
    mapa_jogador = posicionamento_jogador()
    mapa_maquina = posicionamento_maquina()
    mapa_escolhas = criar_mapa()

    while existem_barcos(mapa_jogador) and existem_barcos(mapa_maquina):
        turno_jogador(mapa_maquina, mapa_escolhas)
        turno_maquina(mapa_jogador)

    if existem_barcos(mapa_jogador):
        print("Jogador venceu!")
    else:
        print("Máquina venceu!")

    print("Mapa do Jogador")
    print(mapa_jogador)
    print("Mapa da máquina")
    print(mapa_maquina)


if __name__ == "__main__":
    main()