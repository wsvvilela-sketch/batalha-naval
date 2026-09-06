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