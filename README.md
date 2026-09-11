# batalha-naval
Atividade de Desing Profissional para botar em prática os conceitos aprendidos em GitHub com a professora Cassiana Fagundes Da Silva, o jogo de batalha naval foi feito em python usando a lógica de vetores durante o primeiro semestre do meu curso de Engenaria de Software na as aulas de Programação de Computadores com o professor Aryel Marlus Repula De Oliveira. O objetivo desse repositório é documentar o refinamento do código para botar em prática os principais conceitos aprendidos nas aulas de Desing Profissional.

# Organização do que sera feito
## 05/09/2026
Antes de eu começar a mexer no código, preciso identificar o que precisa ser melhorado e separar em tópicos e dentro desses tópicos separar em etapas. abaixo segue os tópicos e etapas que seguirei durante o desenvolvimento do código:
- Estrutura e organização do código
    - Transformar o script em funções (ex: posicionar_barco(), turno_jogador(), turno_maquina(), verificar_vencedor()) em vez de tudo solto no nível principal;
    - Eliminar duplicação: a lógica de "subtrai barco1_2/barco1_5/..." se repete várias vezes — trocar as variáveis soltas por um dicionário {2: qtd, 5: qtd, 8: qtd, 9: qtd};
    - Unificar a lógica de posicionamento de barco do jogador e da máquina numa única função parametrizada (elas fazem quase a mesma coisa);
    - Extrair "números mágicos" (65, [2,5,8,9], quantidades) para constantes no topo do arquivo;
    - Considerar criar classes Tabuleiro e Barco para reduzir uso de variáveis globais soltas;

- Jogabilidade (funcionalidade real do jogo)
    - Implementar um tabuleiro 2D de verdade (linha/coluna) em vez de índice linear — hoje um barco pode "vazar" de uma linha pra outra sem o jogador perceber;
    - Adicionar orientação de posicionamento (horizontal/vertical), já que batalha naval real permite as duas;
    - Impedir que o jogador veja o tabuleiro do adversário (hoje isso não é problema porque cada player só vê o seu próprio array, mas ao expandir pra interface gráfica, cuidar disso);

- Interface / usabilidade
    - Criar uma função de impressão do tabuleiro em formato de grade (ex: linhas e colunas com letras/números), em vez de print(mapa1) cru;
    - Reduzir prints repetitivos de listas inteiras a cada jogada (deixar mais "limpo" visualmente);
    - Mostrar o tabuleiro do adversário como o jogador o vê (com "?" nas células não reveladas) ao invés de mostrar mapa2 completo;

- Boas práticas gerais
    - Reduzir comentários excessivos linha a linha e manter só os que explicam decisões não óbvias;
    - Adicionar um if __name__ == "__main__": e mover a lógica principal para uma função main();
    - Adicionar testes simples ou pelo menos validações de estado (ex: garantir que a soma de barcos bate com o esperado antes de começar o jogo);

# Estrutura e organização do código
## 06/09/2026
- Transformar em funções
    - Todo o código que antes rodava direto no nível principal do script agora está dividido em funções: posicionamento_jogador(), posicionamento_maquina(), turno_jogador(), turno_maquina(), existem_barcos() e main(). Isso deixa o fluxo do jogo (em main()) fácil de ler de cima a baixo, e cada função pode ser testada ou reaproveitada isoladamente.

 - Eliminar duplicação com dicionário
    - As variáveis soltas barco1_2, barco1_5, barco1_8, barco1_9 (e o equivalente para a máquina) foram substituídas por um único dicionário: {2: qtd, 5: qtd, 8: qtd, 9: qtd}. Isso elimina os blocos repetidos de if tipo == 2: ... elif tipo == 5: ... que apareciam toda vez que era preciso subtrair ou checar a quantidade de um barco.

- Unificar lógica de posicionamento
    - Jogador e máquina compartilham agora as mesmas funções de baixo nível: cabe_no_mapa(), posicao_livre() e posicionar_barco(). Antes essa lógica estava duplicada (uma cópia pro jogador, outra pra máquina, quase idênticas). Agora só existe uma versão de cada regra — se um bug de posicionamento for corrigido, corrige em um lugar só e vale pros dois.

- Constantes no topo
    - TAMANHO_MAPA, TAMANHOS_BARCOS e QUANTIDADE_INICIAL_BARCOS ficam declarados no início do arquivo, em vez de números como 65 e listas [2,5,8,9] espalhados pelo código. Facilita mudar as regras do jogo (ex: mapa maior, outros tamanhos de barco) sem precisar caçar cada ocorrência.

- Sobre classes (Tabuleiro, Barco)
    - Deixei esse ponto de lado por enquanto — ele muda mais a "forma" do código (orientado a objetos) do que a organização em si, e faz mais sentido introduzir junto com o tabuleiro 2D real (item do tópico "Jogabilidade").

# Jogabilidade (funcionalidade real do jogo)
## 08/09/2026
- Tabuleiro 2D de verdade (linha/coluna)
    - O mapa deixou de ser uma lista linear de índice único e virou um tabuleiro real de 10x10 (100 células), acessado por (linha, coluna). Criei coordenada_para_indice() e indice_para_coordenada() pra converter entre a coordenada 2D e a posição interna na lista. Isso resolve o problema do original, onde um barco podia começar no fim de uma linha e continuar na linha de baixo sem o jogador perceber — agora cabe_no_mapa() verifica limites reais de linha e coluna.

- Correção de erro:
    - Corrigi um bug ao testar: com tabuleiro 8x8 (minha ideia inicial), o barco de tamanho 9 nunca cabia em nenhuma linha/coluna, e o jogo simplesmente desistia dele silenciosamente. Aumentei para 10x10 (tamanho padrão do batalha naval) e confirmei com um teste automatizado que agora as 44 células de barco (2×2 + 3×5 + 2×8 + 1×9) são sempre posicionadas corretamente.

- Orientação horizontal/vertical
    - Adicionei HORIZONTAL/VERTICAL e a função indices_do_barco(), que calcula as células ocupadas crescendo em coluna (H) ou em linha (V). O jogador agora escolhe linha, coluna e orientação (H/V) ao posicionar um barco, e a máquina testa as duas orientações em posicoes_validas_para_barco() antes de escolher aleatoriamente — isso também aumenta as chances dela conseguir posicionar todos os barcos.

- Jogador não ver o tabuleiro do adversário
    - Isso já estava estruturalmente correto (cada um só manipula seu próprio array), mas deixei isso explícito em comentário na função turno_jogador(): o jogador só recebe acesso a mapa_escolhas (o que já foi revelado por tentativas anteriores), nunca ao mapa_maquina completo com os barcos ainda escondidos.

# Interface/usabilidade
## 09/09/2026

- Tabuleiro em formato de grade
    - Criei imprimir_tabuleiro(), que desenha o mapa como uma grade real, com colunas em letras (A, B, C...) e linhas numeradas (1, 2, 3...), no estilo clássico de batalha naval — em vez do antigo print(mapa) cru, que jogava a lista Python inteira na tela ([0, 0, 8, 8, 0, 5, ...]). Como consequência, também troquei a forma de escolher posição: agora o jogador informa linha + letra da coluna (ex: linha 3, coluna "F"), igual ao jogo de tabuleiro físico, em vez de um índice numérico abstrato de 0 a 99.

- Reduzir prints repetitivos
    - Antes, cada tiro imprimia a lista completa do mapa de novo. Agora as mensagens de tiro só mostram texto direto (ex: Jogador atirou em F3: Acertou!), e o tabuleiro em grade só é redesenhado uma vez por rodada completa (depois da jogada do jogador e da máquina), não a cada mensagem — bem menos poluição visual no terminal.

- Ocultar barcos não revelados do oponente
    - Esse foi o ponto mais delicado. O código original, ao marcar uma célula atingida, sobrescrevia o valor com 1 (ATINGIDO) tanto em acerto quanto em erro — perdendo a informação de qual dos dois havia sido. Para resolver isso corretamente, adicionei dois arrays de histórico (historico_tiros_dados e historico_tiros_recebidos) que guardam o valor da célula no exato momento do tiro, antes de ser sobrescrita. Com isso, simbolos_mapa_oponente() consegue mostrar:

    - ? em toda célula ainda não atingida (o jogador realmente não sabe o que tem lá)
    - X só nas células onde já acertou um barco
    - O só nas células onde já errou

# Boas práticas gerais
## 11/09/2026

- Reduzir comentários excessivos
    - Esse item já estava praticamente resolvido pelas reestruturações anteriores — o código não tem mais um comentário por linha como o original (#seleção do local, #checa se é possivel posicionar, etc.). Só removi um resquício trivial (#importa função que sera utilizada nas escolhas na máquina em cima de import random, que não agregava nada).

- main() + if __name__ == "__main__":
    - Também já estava feito desde a reestruturação em funções. Confirmando: o fluxo principal do jogo vive todo dentro de main(), e só executa quando o arquivo é rodado diretamente.

- Validações e testes simples — o trabalho principal desta etapa:
    - Criei validar_configuracao(), que roda automaticamente no início de main() e verifica, antes do jogo começar, se a configuração é jogável: se o maior barco cabe no tabuleiro, se a soma de células dos barcos não excede o tabuleiro, e se TAMANHOS_BARCOS e QUANTIDADE_INICIAL_BARCOS estão sincronizados.

    - Testei essa validação de propósito com uma configuração quebrada (tabuleiro 8x8 com barco de tamanho 9 — o mesmo bug real que apareceu numa etapa anterior) e ela pegou o problema corretamente, em vez de deixar o jogo simplesmente "esquecer" de posicionar aquele barco silenciosamente.