Invvaders by RICK RIBEIRO
Descrição

"Invvaders" é um jogo 2D estilo "arcade shooter", onde o jogador controla uma nave espacial para defender-se contra ondas de inimigos. O objetivo do jogador é derrotar todos os inimigos enquanto evita seus ataques e sobrevive o máximo possível. Ao final, o jogador enfrentará o Game Over se sua saúde ou vidas chegarem a zero.

Requisitos

    Python 3.7+
    Pygame 2.0.0+
    8-BIT WONDER.ttf (Disponível na pasta 'assets')
    
    

Instalação

    Certifique-se de ter o Python instalado em seu sistema.
    Instale o Pygame executando o comando no terminal de comando:
    pip install pygame
    

Como Jogar

    Abra a pasta que você baixou desse diretório em uma IDE configurada para Python e
    execute o arquivo principal 'main.py' para iniciar o jogo:

    Na tela de menu, você terá as opções:
        COMECAR: Começa o jogo.
        SAIR: Sai do jogo.

    Durante o jogo:
        Use as teclas W, A, S, D para movimentar a nave.
        Pressione Espaço para disparar contra os inimigos.

    O jogo aumenta de dificuldade conforme as ondas de inimigos avançam.

    Quando a vida do jogador ou o número de vidas for zero, uma imagem de Game Over será exibida.

Recursos

    Nave do Jogador: Controlada pelo jogador com teclas WASD.
    Inimigos: Aparecem em ondas, cada um com diferentes velocidades e projéteis.
    Sistema de Vidas: O jogador começa com 5 vidas. Quando um inimigo ou projétil atinge o jogador, ele perde saúde e, eventualmente, uma vida.
    Disparo Alternado: A nave do jogador atira projéteis de diferentes posições (alternando o offset).
    Animações de Inimigos: Cada inimigo tem animações e sprites variados ao ser atingido.
    Sistema de Game Over: Quando todas as vidas acabam, uma imagem de Game Over é exibida no centro da tela.

Estrutura do Projeto
invvaders/
│
├── assets/                  # Arquivos de imagem, som e fontes usados no jogo
│   ├── Main_Ship_Full_Health.png
│   ├── MainShip_Weapons_Auto_Cannon_1.png
│   ├── Player_beam.png
│   ├── GAME_OVER.png
│   └── 8-BIT WONDER.ttf
│
├── main.py                  # Arquivo principal do jogo
├── README.md                # Instruções e informações sobre o projeto

Personalização

Você pode modificar ou adicionar novos recursos facilmente:

    Sprites: Substitua as imagens na pasta assets/ para dar um novo visual ao jogo.
    Dificuldade: Alterando variáveis como enemy_velocity, wave_length, e weapon_shoot_velocity, você pode ajustar a dificuldade do jogo.
    Sons: Para adicionar sons, você pode usar o pygame.mixer e carregar arquivos .wav ou .mp3 na pasta assets/.

Licença

Este projeto foi criado por Rick Ribeiro e é distribuído sob a licença MIT.
Créditos

    Programação: Rick Ribeiro
    Arte:
    https://grafxkid.itch.io/mini-pixel-pack-3#google_vignette
    https://foozlecc.itch.io/void-main-ship
    https://ansimuz.itch.io/space-background
    
    Sons:
    https://youtu.be/G2nmOULeOBQ?si=4Tn_7HbHrHmIUt3C
    https://www.youtube.com/watch?v=l3TQbgPme5Q
    
    Fonte: 8-BIT WONDER.ttf
