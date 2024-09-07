import pygame
import random

# Inicjalizacja pygame
pygame.init()

# Wymiary okna gry
width = 600
height = 400

# Rozmiar węża i prędkość
snake_block = 10  # Każdy segment węża to 10x10 pikseli
head_size = 20  # Głowa węża będzie większa
eye_size = 4  # Rozmiar oczu węża
meat_block = 60  # Zwiększamy rozmiar mięsa do 60x60 pikseli
snake_speed = 7  # Utrzymujemy rozsądną prędkość

# Tworzenie okna gry
dis = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake Game')

# Zegar gry
clock = pygame.time.Clock()

# Czcionka do wiadomości
font_style = pygame.font.SysFont(None, 35)  # Czcionka do wyświetlania komunikatów

# Ładowanie obrazka mięsa
try:
    meat_img = pygame.image.load('meat.png')  # Załaduj obrazek mięsa
    meat_img = pygame.transform.scale(meat_img, (meat_block, meat_block))  # Dopasowanie do większych rozmiarów
    print("Obrazek mięsa załadowany pomyślnie.")
except pygame.error as e:
    print(f"Nie można załadować obrazka mięsa: {e}")
    meat_img = None


# Funkcja wyświetlania wiadomości w pełni widocznej na ekranie
def display_message(msg1, msg2, color):
    mesg1 = font_style.render(msg1, True, color)
    mesg2 = font_style.render(msg2, True, color)
    # Wyśrodkowanie pierwszej linii tekstu
    text_rect1 = mesg1.get_rect(center=(width / 2, height / 2 - 20))
    # Wyśrodkowanie drugiej linii tekstu
    text_rect2 = mesg2.get_rect(center=(width / 2, height / 2 + 20))
    # Wyświetlenie obu linii
    dis.blit(mesg1, text_rect1)
    dis.blit(mesg2, text_rect2)


# Funkcja rysująca głowę węża (prostokąt z zaokrąglonymi rogami i oczami)
def draw_snake_head(snake_list, direction):
    head_pos = snake_list[0]  # Głowa węża jest pierwszym segmentem

    # Przesunięcie głowy, aby była wyśrodkowana względem segmentów
    offset = (head_size - snake_block) // 2

    # Rysowanie głowy jako większy prostokąt z zaokrąglonymi rogami
    pygame.draw.rect(dis, (0, 0, 0),
                     [head_pos[0] - offset, head_pos[1] - offset, head_size, head_size],
                     border_radius=10)  # Zaokrąglone rogi

    # Ustawienie pozycji oczu w zależności od kierunku
    if direction == 'UP':
        eye_y_pos = head_pos[1] - offset + head_size // 4  # Oczy bliżej górnej krawędzi
        left_eye_x_pos = head_pos[0] - offset + head_size // 4
        right_eye_x_pos = head_pos[0] - offset + 3 * head_size // 4
    elif direction == 'DOWN':
        eye_y_pos = head_pos[1] - offset + 3 * head_size // 4  # Oczy bliżej dolnej krawędzi
        left_eye_x_pos = head_pos[0] - offset + head_size // 4
        right_eye_x_pos = head_pos[0] - offset + 3 * head_size // 4
    elif direction == 'LEFT':
        eye_y_pos = head_pos[1] - offset + head_size // 4  # Oczy bliżej lewej krawędzi
        left_eye_x_pos = head_pos[0] - offset + head_size // 4
        right_eye_x_pos = head_pos[0] - offset + head_size // 4
    elif direction == 'RIGHT':
        eye_y_pos = head_pos[1] - offset + head_size // 4  # Oczy bliżej prawej krawędzi
        left_eye_x_pos = head_pos[0] - offset + 3 * head_size // 4
        right_eye_x_pos = head_pos[0] - offset + 3 * head_size // 4

    # Rysowanie oczu (białe kółka)
    pygame.draw.circle(dis, (255, 255, 255), (left_eye_x_pos, eye_y_pos), eye_size)  # Lewe oko
    pygame.draw.circle(dis, (255, 255, 255), (right_eye_x_pos, eye_y_pos), eye_size)  # Prawe oko


# Funkcja rysująca węża
def our_snake(snake_block, snake_list, direction):
    # Rysowanie głowy węża (większej, prostokątnej z zaokrąglonymi rogami i oczami)
    draw_snake_head(snake_list, direction)

    # Rysowanie reszty ciała jako prostokąty
    for segment in snake_list[1:]:
        pygame.draw.rect(dis, (0, 0, 0), [segment[0], segment[1], snake_block, snake_block])  # Czarne ciało


# Funkcja rysująca "mięso"
def draw_meat(foodx, foody):
    if meat_img:
        dis.blit(meat_img, (foodx, foody))  # Rysowanie obrazka mięsa na pozycji
    else:
        pygame.draw.rect(dis, (255, 0, 0), [foodx, foody, meat_block, meat_block])


# Funkcja głównej pętli gry
def gameLoop():
    global x1_change, y1_change

    game_over = False
    game_close = False

    # Początkowe położenie węża
    x1 = width // 2
    y1 = height // 2

    # Zmiany położenia węża
    x1_change = 0
    y1_change = 0
    direction = 'RIGHT'  # Początkowy kierunek poruszania się węża

    # Lista do przechowywania segmentów węża
    snake_List = [[x1, y1], [x1 - snake_block, y1], [x1 - 2 * snake_block, y1]]  # Wąż ma 3 segmenty na starcie
    Length_of_snake = 3

    # Początkowe położenie "mięsa"
    foodx = round(random.randrange(0, width - meat_block) / 10.0) * 10.0
    foody = round(random.randrange(0, height - meat_block) / 10.0) * 10.0

    print("Gra rozpoczęta. Pozycja węża:", snake_List)  # Debug

    first_move = True  # Flaga wskazująca, że pierwszy ruch jeszcze się nie odbył

    while not game_over:

        while game_close == True:
            dis.fill((0, 255, 0))  # Zielone tło
            display_message("IF YOU WANT TO END PRESS Z", "OR IF YOU WANT TO START PRESS C", (213, 50, 80))  # Podzielony komunikat
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_z:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                first_move = False  # Pierwszy ruch się rozpoczął
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -snake_block
                    y1_change = 0
                    direction = 'LEFT'
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = snake_block
                    y1_change = 0
                    direction = 'RIGHT'
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -snake_block
                    x1_change = 0
                    direction = 'UP'
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = snake_block
                    x1_change = 0
                    direction = 'DOWN'

        # Sprawdzenie, czy wąż uderza w krawędź
        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            print(f"Kolizja z krawędzią: pozycja węża x={x1}, y={y1}")  # Debug
            game_close = True

        # Aktualizacja pozycji węża
        x1 += x1_change
        y1 += y1_change
        dis.fill((0, 255, 0))  # Tło gry

        # Rysowanie "mięsa"
        draw_meat(foodx, foody)

        # Aktualizacja węża
        snake_Head = [x1, y1]  # Głowa na początku listy
        snake_List.insert(0, snake_Head)

        # Utrzymanie długości węża
        if len(snake_List) > Length_of_snake:
            del snake_List[-1]

        # Sprawdzenie kolizji z własnym ciałem tylko po pierwszym ruchu
        if not first_move:  # Sprawdzaj kolizję dopiero po pierwszym ruchu
            for segment in snake_List[1:]:
                if segment == snake_List[0]:  # Sprawdzanie kolizji z głową
                    print("Kolizja z ciałem węża.")  # Debug
                    game_close = True

        # Rysowanie węża (z głową prowadzącą i ciałem podążającym za nią)
        our_snake(snake_block, snake_List, direction)

        # Aktualizacja ekranu
        pygame.display.update()

        # Sprawdzenie, czy wąż zjadł "mięso" (dokładna kolizja z głową węża)
        if x1 < foodx + meat_block and x1 + snake_block > foodx and y1 < foody + meat_block and y1 + snake_block > foody:
            print("Wąż zjadł mięso")  # Debug
            foodx = round(random.randrange(0, width - meat_block) / 10.0) * 10.0
            foody = round(random.randrange(0, height - meat_block) / 10.0) * 10.0
            Length_of_snake += 1  # Wąż się wydłuża

        clock.tick(snake_speed)  # Tempo gry

    pygame.quit()
    quit()


# Uruchomienie gry
gameLoop()






