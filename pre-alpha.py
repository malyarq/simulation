import pygame
import random

# Определение начальных переменных
width = 1800
height = 900
particles = []
max_d = 1000
particle_speed = 0.5
running = True
number_minus = 100
number_plus = 100
number_zero = 100

# Цвета
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Simulation MAIN")
fpsClock = pygame.time.Clock()
fpsClock.tick(360)

# Метод рисования объекта
def draw_particles(particles):
    for particle in particles:
        pygame.draw.circle(screen, particle.color, (particle.x, particle.y), particle.weight)

# Класс частиц
class Particle:
    def __init__(self, x, y, color, weight):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.color = color
        self.weight = weight

# Методы рандомных значений x, y и weight
def random_x():
    return random.randint(0, width)

def random_y():
    return random.randint(0, height)

def random_weight():
    return random.randint(6, 12)

# Метод создания группы частиц
def create_particles(number, color):
    group = []
    for _ in range(number):
        particle = Particle(random_x(), random_y(), color, random_weight())
        group.append(particle)
        particles.append(particle)
    return group

# Метод для работы физики между частицами
def rule(particles1, particles2, g):
    for i in range(len(particles1)):
        fx = 0
        fy = 0
        a = particles1[i]
        for j in range(len(particles2)):
            if i != j:
                b = particles2[j]
                dx = a.x - b.x
                dy = a.y - b.y
                d = (dx ** 2 + dy ** 2) ** 0.5
                min_d = a.weight + b.weight
                if min_d < d < max_d:
                    F = (-1 * g * a.weight * b.weight) / (d ** 2)
                    fx += (F * dx)
                    fy += (F * dy)
        a.vx = (a.vx + fx) * particle_speed
        a.vy = (a.vy + fy) * particle_speed
        a.x += a.vx
        a.y += a.vy
        if a.x <= 0:
            a.vx *= -1
            a.x = 1
        if a.x >= width:
            a.vx *= -1
            a.x = width - 1
        if a.y <= 0:
            a.vy *= -1
            a.y = 1
        if a.y >= height:
            a.vy *= -1
            a.y = height - 1

# Создаем группы частиц
minus = create_particles(number_minus, red)
plus = create_particles(number_plus, green)
zero = create_particles(number_zero, blue)

# Основной цикл программы
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Очистка экрана
    screen.fill(black)
    '''
    Обработка частиц
    Правила взаимодействия: rule(группа1, группа2, сила)
    Положительная сила = притяжение; Отрицательная сила = отталкивание
    '''
    rule(minus, minus, 2)
    rule(plus, plus, 2)
    rule(zero, zero, -2)
    rule(zero, minus, 1)
    rule(zero, plus, 1)
    
    # Отрисовка частиц
    draw_particles(particles)

    # Обновление экрана
    pygame.display.flip()

# Завершение работы Pygame
pygame.quit()
