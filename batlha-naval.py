#importa função que sera utilizada nas escolhas na máquina
import random

# =========================
# CONSTANTES
# =========================
# Antes eram "números mágicos" espalhados pelo código (65, [2,5,8,9], etc.)
# Agora ficam centralizados aqui: se precisar mudar o tamanho do mapa ou os
# tipos de barco, muda-se em um único lugar.
TAMANHO_MAPA = 65
TAMANHOS_BARCOS = [2, 5, 8, 9]
QUANTIDADE_INICIAL_BARCOS = {2: 2, 5: 3, 8: 2, 9: 1}

VAZIO = 0
ATINGIDO = 1


# =========================
# FUNÇÕES DE TABULEIRO / POSICIONAMENTO
# (compartilhadas entre jogador e máquina)
# =========================

def criar_mapa():
    """Cria um mapa vazio (lista de zeros) do tamanho definido em TAMANHO_MAPA."""
    return [VAZIO] * TAMANHO_MAPA


def cabe_no_mapa(local, tamanho_barco):
    """Checa se um barco de determinado tamanho cabe no mapa a partir de 'local'."""
    return 0 <= local <= TAMANHO_MAPA - 1 and local + tamanho_barco <= TAMANHO_MAPA


def posicao_livre(mapa, local, tamanho_barco):
    """Checa se todas as células que o barco ocuparia estão livres."""
    for i in range(tamanho_barco):
        if mapa[local + i] != VAZIO:
            return False
    return True


def posicionar_barco(mapa, local, tamanho_barco):
    """Marca no mapa as células ocupadas pelo barco."""
    for i in range(tamanho_barco):
        mapa[local + i] = tamanho_barco


def barcos_restantes(quantidades):
    """Retorna True se ainda houver algum barco para posicionar."""
    return any(qtd > 0 for qtd in quantidades.values())


# =========================
# POSICIONAMENTO - JOGADOR
# =========================

def posicionamento_jogador():
    """Loop de posicionamento de barcos controlado pelo jogador via input()."""
    mapa = criar_mapa()
    # copy() evita alterar a constante QUANTIDADE_INICIAL_BARCOS
    quantidades = QUANTIDADE_INICIAL_BARCOS.copy()

    while barcos_restantes(quantidades):
        tipo_barco = int(input(f"Escolha o tamanho do barco {TAMANHOS_BARCOS}: "))

        if tipo_barco not in TAMANHOS_BARCOS:
            print("Tamanho inválido")
            continue

        if quantidades[tipo_barco] == 0:
            print("Esse barco já acabou")
            continue

        local = int(input("Escolha a posição do barco: "))

        if not cabe_no_mapa(local, tipo_barco):
            print("Não cabe no mapa")
            continue

        if not posicao_livre(mapa, local, tipo_barco):
            print("Espaço ocupado")
            continue

        posicionar_barco(mapa, local, tipo_barco)
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
    """Retorna todas as posições onde o barco cabe e está livre."""
    validas = []
    for pos in range(TAMANHO_MAPA):
        if cabe_no_mapa(pos, tamanho_barco) and posicao_livre(mapa, pos, tamanho_barco):
            validas.append(pos)
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
            local = random.choice(validas)
            posicionar_barco(mapa, local, tipo_barco)
            quantidades[tipo_barco] -= 1
        else:
            # se não há posição válida para esse tipo de barco, desiste dele
            quantidades[tipo_barco] = 0

    return mapa


# =========================
# RODADAS DO JOGO
# =========================

def turno_jogador(mapa_maquina, mapa_escolhas):
    """Processa a jogada do jogador: escolhe uma posição no mapa da máquina."""
    while True:
        escolha = int(input("Escolha um número de 0 a 64: "))

        if escolha < 0 or escolha > TAMANHO_MAPA - 1 or mapa_maquina[escolha] == ATINGIDO:
            print("Opção inválida")
            continue

        print(f"Jogador escolheu {escolha}")

        if mapa_maquina[escolha] > 1:
            print("Acertou!")
            print("O tamanho do barco acertado é", mapa_maquina[escolha])
        else:
            print("Errou!")

        mapa_escolhas[escolha] = mapa_maquina[escolha]
        mapa_maquina[escolha] = ATINGIDO
        print(mapa_escolhas)
        break


def turno_maquina(mapa_jogador):
    """Processa a jogada da máquina: escolhe aleatoriamente uma posição não atingida."""
    while True:
        escolha = random.randint(0, TAMANHO_MAPA - 1)

        if mapa_jogador[escolha] != ATINGIDO:
            print(f"Máquina escolheu {escolha}")

            if mapa_jogador[escolha] > 1:
                print("Máquina acertou!")
            else:
                print("Máquina errou!")

            mapa_jogador[escolha] = ATINGIDO
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