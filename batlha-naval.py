#importa função que sera utilizada nas escolhas na máquina 
import random

#lista que sera usada como mapa
mapa1 = [0]*65
mapa2 = [0]*65
mapa_escolhas = [0]*65

#quantidades de barcos

#barcos do jogador
barco1_2 = 2
barco1_5 = 3
barco1_8 = 2
barco1_9 = 1

#barcos da máquina
barco2_2 = 2
barco2_5 = 3
barco2_8 = 2
barco2_9 = 1

#posicionamento de barcos jogador

#consição para continuar o looping de posicionamento
while barco1_2 > 0 or barco1_5 > 0 or barco1_8 > 0 or barco1_9 > 0:
    #seleção do tamanho do barco
    tipo_barco1 = int(input("Escolha o tamanho do barco (2,5,8,9): "))
    #checa se foi escolhido um dos tamanhos disponiveis
    if tipo_barco1 not in [2,5,8,9]:
        print("Tamanho inválido")
    #checa se o tamaho do barco escolhido esta disponivel
    elif tipo_barco1 == 2 and barco1_2 == 0:
        print("Esse barco já acabou")
    elif tipo_barco1 == 5 and barco1_5 == 0:
        print("Esse barco já acabou")
    elif tipo_barco1 == 8 and barco1_8 == 0:
        print("Esse barco já acabou")
    elif tipo_barco1 == 9 and barco1_9 == 0:
        print("Esse barco já acabou")
    else:
        #posicionamento do barco

        #escolha do local
        local = int(input("Escolha a posição do barco: "))
        #checa se é possivel posicionar o barco selecionado
        if local < 0 or local > 64 or local + tipo_barco1 > 65:
            print("Não cabe no mapa")
        else:
            #checa se ja tem um barco na posição selecionada
            livre = True
            for i in range(tipo_barco1):
                if mapa1[local + i] != 0:
                    livre = False
                    break
            
            #checa se o espaço selecionando esta livre
            if livre:
                #posiciona o barco
                for i in range(tipo_barco1):
                    mapa1[local + i] = tipo_barco1

                #subitrai a quantidade de barcos dependendo de qual foi selecionado
                if tipo_barco1 == 2:
                    barco1_2 -= 1
                elif tipo_barco1 == 5:
                    barco1_5 -= 1
                elif tipo_barco1 == 8:
                    barco1_8 -= 1
                elif tipo_barco1 == 9:
                    barco1_9 -= 1

                #informa confirmação do posicionamento
                print("Barco colocado!")
                print(mapa1)

                #informa quantidade de barcos
                print("Agora tem")
                print(barco1_2, "barco(s) de tamanho 2")
                print(barco1_5, "barco(s) de tamanho 5")
                print(barco1_8, "barco(s) de tamanho 8")
                print(barco1_9, "barco de tamanho 9")
            #exibe esta mensagem se o espaço ja esta ocupado
            else:
                print("Espaço ocupado")

#posicionamento de barcos máquina

#consição para continuar o looping de posicionamento
while barco2_2 > 0 or barco2_5 > 0 or barco2_8 > 0 or barco2_9 > 0:
    #máquina escolhe aleatóriamento o tamanho do barco
    tipo_barco2 = random.choice([2,5,8,9])
    #checa se o tamaho do barco escolhido esta disponivel
    if tipo_barco2 == 2 and barco2_2 == 0:
        continue
    elif tipo_barco2 == 5 and barco2_5 == 0:
        continue
    elif tipo_barco2 == 8 and barco2_8 == 0:
        continue
    elif tipo_barco2 == 9 and barco2_9 == 0:
        continue
    #sitema para evitar looping infinito

    #liste que armazena todas as posições onde cabe o barco
    posicoes_validas = []

    #testa todas as posições do mapa
    for pos in range(65):
        #checa se o barco cabe no mapa
        if pos + tipo_barco2 <= 65:
            livre = True
            #checa se ja tem um barco na posição selecionada
            for i in range(tipo_barco2):
                if mapa2[pos + i] != 0:
                    livre = False
                    break
            #salva posição

            #posicionamento do barco

            #checa se a posição esta livre
            if livre:
                posicoes_validas.append(pos)
    #checa se foi possivel encontrar uma posição valida
    if len(posicoes_validas) > 0:
        #escolhe aleatóriamente uma das posições válidas
        local2 = random.choice(posicoes_validas)
        #posiciona o barco
        for i in range(tipo_barco2):
            mapa2[local2 + i] = tipo_barco2
        
        #subitrai a quantidade de barcos dependendo de qual foi selecionado
        if tipo_barco2 == 2:
            barco2_2 -= 1
        elif tipo_barco2 == 5:
            barco2_5 -= 1
        elif tipo_barco2 == 8:
            barco2_8 -= 1
        elif tipo_barco2 == 9:
            barco2_9 -= 1
    #se nenhuma posição valida foi encontrada zera a quantidade de barcos que foi selecionado
    else:
        if tipo_barco2 == 2:
            barco2_2 = 0
        elif tipo_barco2 == 5:
            barco2_5 = 0
        elif tipo_barco2 == 8:
            barco2_8 = 0
        elif tipo_barco2 == 9:
            barco2_9 = 0

#condições para o looping de rodadas
while any(x  in [2, 5, 8, 9] for x in mapa1) and any (x in [2, 5, 8, 9] for x in mapa2):
    
    #turno do jogador
    while True:
        #determina escolha
        escolha1 = int(input("Escolha um número de 0 a 64: "))
        #checa se a escolha enta dentro do mapa ou se ela ja foi escolhida
        if escolha1 < 0 or escolha1 > 64 or mapa2[escolha1] == 1:
            print("Opção inválida")
        else:
            #exibe local escolhido
            print(f"Jogador escolheu {escolha1}")
            #exibe acerto ou erro e o tamanho do barco acertado
            if mapa2[escolha1] > 1:
                print("Acertou!")
                print("O tamanho do barco acertado é", mapa2[escolha1])
            else:
                print("Errou!")
                mapa2[escolha1] = 1
            #marca posição escolhida
            mapa_escolhas[escolha1] = mapa2[escolha1]
            mapa2[escolha1] = 1
            print(mapa_escolhas)
            break

    #turno da máquina
    while True:
        #determina aleatóriamente a escolha
        escolha2 = random.randint(0, 64)
        #checa se a escolha ja foi escolhida
        if mapa1[escolha2] != 1:
            #exibe escolha da máquina
            print(f"Máquina escolheu {escolha2}")
            #exibe acerto ou erro
            if mapa1[escolha2] > 1:
                print("Máquina acertou!")
            else:
                print("Máquina errou!")
            #marca posição escolhida
            mapa1[escolha2] = 1
            print(mapa1)
            break

#verifica o vencedor
if any( x in [2, 5, 8, 9] for x in mapa1):
    print("Jogador venceu!")
else:
    print("Máquina venceu!")

#exibe mapa
print("Mapa do Jogador")
print(mapa1)
print("Mapa da máquina")
print(mapa2)