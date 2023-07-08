import pygame
import random
import pygame_gui
from pygame_gui.elements import UIButton, UIHorizontalSlider, UILabel, UIDropDownMenu

# Определение начальных переменных
width = 1800
height = 900
particles = []
rules = []
rules_label_all = []
running = True
running_simulation = True
number_red = 100
number_green = 100
number_blue = 100
number_rule = 0
max_d = 500
resistance = 0.5
gravitation = 10
strength = 1

# Цвета
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Simulation NEW")
fpsClock = pygame.time.Clock()
ui_manager = pygame_gui.UIManager((width, height))

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

# Метод установки значений по умолчанию
def defaults():
    global number_red, number_green, number_blue, max_d, resistance, gravitation, strength
    number_red = 100
    number_green = 100
    number_blue = 100
    max_d = 500
    resistance = 0.5
    gravitation = 10
    strength = 1
    number_red_value_label.set_text(str(number_red))
    number_green_value_label.set_text(str(number_green))
    number_blue_value_label.set_text(str(number_blue))
    max_d_value_label.set_text(str(max_d))
    resistance_value_label.set_text(str(resistance))
    gravitation_value_label.set_text(str(gravitation))
    interaction_strength_value_label.set_text(str(strength))
    number_red_slider.set_current_value(number_red)
    number_green_slider.set_current_value(number_green)
    number_blue_slider.set_current_value(number_blue)
    max_d_slider.set_current_value(max_d)
    resistance_slider.set_current_value(resistance)
    gravitation_slider.set_current_value(gravitation)
    interaction_strength_slider.set_current_value(strength)

# Метод добавления базовых правил
def base_rules():
    rules.append((red_group, red_group, 2))
    rules_label_all.append(UILabel(relative_rect=pygame.Rect((10, 410), (300, 20)), text='Red attracted to Red with 2 force', manager=ui_manager))
    rules.append(((green_group, green_group, 2)))
    rules_label_all.append(UILabel(relative_rect=pygame.Rect((10, 440), (300, 20)), text='Green attracted to Green with 2 force', manager=ui_manager))
    rules.append(((blue_group, blue_group, -2)))
    rules_label_all.append(UILabel(relative_rect=pygame.Rect((10, 470), (300, 20)), text='Blue repelled from Blue with -2 force', manager=ui_manager))
    rules.append(((blue_group, red_group, 1)))
    rules_label_all.append(UILabel(relative_rect=pygame.Rect((10, 500), (300, 20)), text='Blue attracted to Red with 1 force', manager=ui_manager))
    rules.append(((blue_group, green_group, 1)))
    rules_label_all.append(UILabel(relative_rect=pygame.Rect((10, 530), (300, 20)), text='Blue attracted to Green with 1 force', manager=ui_manager))

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
    for a in particles1:
        fx = 0
        fy = 0
        for b in particles2:
            if a is not b:
                dx = a.x - b.x
                dy = a.y - b.y
                d_squared = dx ** 2 + dy ** 2
                min_d = a.weight + b.weight
                if min_d < d_squared < max_d ** 2:
                    F = (-gravitation / 10) * g * a.weight * b.weight / d_squared
                    fx += F * dx
                    fy += F * dy
        a.vx = (a.vx + fx) * (1 - resistance)
        a.vy = (a.vy + fy) * (1 - resistance)
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

# Методы увеличения яркости
def super_puper_bright_color(color):
    r, g, b = color
    r = min(255, r + 120)
    g = min(255, g + 120)
    b = min(255, b + 120)
    return (r, g, b)

def super_bright_color(color):
    r, g, b = color
    r = min(255, r + 100)
    g = min(255, g + 100)
    b = min(255, b + 100)
    return (r, g, b)

def bright_color(color):
    r, g, b = color
    r = min(255, r + 50)
    g = min(255, g + 50)
    b = min(255, b + 50)
    return (r, g, b)

# Метод рисования объекта
def draw_particles(particles):
    for particle in particles:
        b_color = bright_color(particle.color)
        sb_color = super_bright_color(particle.color)
        spb_color = super_puper_bright_color(particle.color)
        pygame.draw.circle(screen, particle.color, (particle.x, particle.y), particle.weight)
        pygame.draw.circle(screen, b_color, (particle.x, particle.y), particle.weight * 0.75)
        pygame.draw.circle(screen, sb_color, (particle.x, particle.y), particle.weight * 0.5)
        pygame.draw.circle(screen, spb_color, (particle.x, particle.y), particle.weight * 0.25)
        
# Ползунки
number_red_label = UILabel(relative_rect=pygame.Rect((10, 20), (110, 20)), text='Red Count:', manager=ui_manager)
number_red_slider = UIHorizontalSlider(relative_rect=pygame.Rect((130, 20), (200, 20)),
                                         start_value=100, value_range=(0, 200), manager=ui_manager)

number_green_label = UILabel(relative_rect=pygame.Rect((10, 50), (110, 20)), text='Green Count:', manager=ui_manager)
number_green_slider = UIHorizontalSlider(relative_rect=pygame.Rect((130, 50), (200, 20)),
                                        start_value=100, value_range=(0, 200), manager=ui_manager)

number_blue_label = UILabel(relative_rect=pygame.Rect((10, 80), (110, 20)), text='Blue Count:', manager=ui_manager)
number_blue_slider = UIHorizontalSlider(relative_rect=pygame.Rect((130, 80), (200, 20)),
                                        start_value=100, value_range=(0, 200), manager=ui_manager)

max_d_label = UILabel(relative_rect=pygame.Rect((10, 110), (110, 20)), text='Max Distance:', manager=ui_manager)
max_d_slider = UIHorizontalSlider(relative_rect=pygame.Rect((130, 110), (200, 20)),
                                  start_value=500, value_range=(0, 1000), manager=ui_manager)

resistance_label = UILabel(relative_rect=pygame.Rect((10, 140), (110, 20)), text='Resistance:', manager=ui_manager)
resistance_slider = UIHorizontalSlider(relative_rect=pygame.Rect((130, 140), (200, 20)),
                                           start_value=0.5, value_range=(0, 1), manager=ui_manager)

gravitation_label = UILabel(relative_rect=pygame.Rect((10, 170), (110, 20)), text='Gravitation:', manager=ui_manager)
gravitation_slider = UIHorizontalSlider(relative_rect=pygame.Rect((130, 170), (200, 20)),
                                           start_value=10, value_range=(0, 100), manager=ui_manager)

rules_label = UILabel(relative_rect=pygame.Rect((10, 380), (50, 20)), text='Rules:', manager=ui_manager)

# Отображение значений ползунков
number_red_value_label = UILabel(relative_rect=pygame.Rect((340, 20), (40, 20)), text=str(number_red), manager=ui_manager)
number_green_value_label = UILabel(relative_rect=pygame.Rect((340, 50), (40, 20)), text=str(number_green), manager=ui_manager)
number_blue_value_label = UILabel(relative_rect=pygame.Rect((340, 80), (40, 20)), text=str(number_blue), manager=ui_manager)
max_d_value_label = UILabel(relative_rect=pygame.Rect((340, 110), (40, 20)), text=str(max_d), manager=ui_manager)
resistance_value_label = UILabel(relative_rect=pygame.Rect((340, 140), (40, 20)), text=str((resistance)), manager=ui_manager)
gravitation_value_label = UILabel(relative_rect=pygame.Rect((340, 170), (40, 20)), text=str(gravitation), manager=ui_manager)

# Кнопки 
defaults_button = UIButton(relative_rect=pygame.Rect((10, 200), (100, 30)), text='Defaults', manager=ui_manager)
start_button = UIButton(relative_rect=pygame.Rect((10, 240), (100, 30)), text='Start', manager=ui_manager)
stop_button = UIButton(relative_rect=pygame.Rect((120, 240), (100, 30)), text='Stop', manager=ui_manager)
restart_button = UIButton(relative_rect=pygame.Rect((10, 280), (100, 30)), text='Restart', manager=ui_manager)
exit_button = UIButton(relative_rect=pygame.Rect((120, 280), (100, 30)), text='Exit', manager=ui_manager)
add_button = UIButton(relative_rect=pygame.Rect((60, 380), (100, 30)), text='Add', manager=ui_manager)
delete_all_button = UIButton(relative_rect=pygame.Rect((170, 380), (110, 30)), text='Delete All', manager=ui_manager)
add_basic_button = UIButton(relative_rect=pygame.Rect((290, 380), (100, 30)), text='Add Basic', manager=ui_manager)
show_gui_button = UIButton(relative_rect=pygame.Rect((10, 850), (130, 30)), text='Show/Hide GUI', manager=ui_manager)
start_button.disable()
add_basic_button.disable()

# Меню выбора первых и вторых взаимодействующих частиц
menu_options = ['Red', 'Green', 'Blue']
interaction_label = UILabel(relative_rect=pygame.Rect((10, 320), (170, 20)), text='Interaction Settings:', manager=ui_manager)
interaction_dropdown_1 = UIDropDownMenu(menu_options, 'Red', pygame.Rect((180, 320), (100, 20)), manager=ui_manager)
interaction_dropdown_2 = UIDropDownMenu(menu_options, 'Green', pygame.Rect((290, 320), (100, 20)), manager=ui_manager)

# Ползунок для выбора силы взаимодействия
interaction_strength_label = UILabel(relative_rect=pygame.Rect((10, 350), (170, 20)), text='Interaction Strength:', manager=ui_manager)
interaction_strength_slider = UIHorizontalSlider(relative_rect=pygame.Rect((180, 350), (200, 20)),
                                                 start_value=1, value_range=(-10, 10), manager=ui_manager)
interaction_strength_value_label = UILabel(relative_rect=pygame.Rect((350, 350), (80, 20)), text='1', manager=ui_manager)

# Создаем группы частиц
red_group = create_particles(number_red, red)
green_group = create_particles(number_green, green)
blue_group = create_particles(number_blue, blue)

# Первоначальная настройка
defaults()
base_rules()

# Основной цикл программы
while running:
    time_delta = fpsClock.tick(60) / 1000.0
    
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                if event.ui_element == number_red_slider:
                    number_red = int(event.value)
                    number_red_value_label.set_text(str(number_red))
                elif event.ui_element == number_green_slider:
                    number_green = int(event.value)
                    number_green_value_label.set_text(str(number_green))
                elif event.ui_element == number_blue_slider:
                    number_blue = int(event.value)
                    number_blue_value_label.set_text(str(number_blue))
                elif event.ui_element == max_d_slider:
                    max_d = int(event.value)
                    max_d_value_label.set_text(str(max_d))
                elif event.ui_element == resistance_slider:
                    resistance = event.value
                    resistance_value_label.set_text(str(resistance))
                elif event.ui_element == gravitation_slider:
                    gravitation = event.value
                    gravitation_value_label.set_text(str(gravitation))
                elif event.ui_element == interaction_strength_slider:
                    strength = int(event.value)
                    interaction_strength_value_label.set_text(str(strength))
            elif event.user_type== pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == exit_button:
                    running = False
                elif event.ui_element == start_button:
                    running_simulation = True
                    stop_button.enable()
                    start_button.disable()
                elif event.ui_element == stop_button:
                    running_simulation = False
                    stop_button.disable()
                    start_button.enable()
                elif event.ui_element == restart_button:
                    particles = []
                    red_group.clear()
                    red_group.extend(create_particles(number_red, red))
                    green_group.clear()
                    green_group.extend(create_particles(number_green, green))
                    blue_group.clear()
                    blue_group.extend(create_particles(number_blue, blue))
                elif event.ui_element == defaults_button:
                    defaults()
                elif event.ui_element == add_button:
                    delete_all_button.enable()
                    add_basic_button.disable()
                    # Получение выбранных типов частиц для взаимодействия
                    interaction_particle_1 = interaction_dropdown_1.selected_option
                    interaction_particle_2 = interaction_dropdown_2.selected_option
                    if strength != 0:
                        # Обработка правил взаимодействия между частицами
                        if interaction_particle_1 == 'Red':
                            if interaction_particle_2 == 'Red':
                                rules.append((red_group, red_group, strength))
                            elif interaction_particle_2 == 'Green':
                                rules.append((red_group, green_group, strength))
                            elif interaction_particle_2 == 'Blue':
                                rules.append((red_group, blue_group, strength))
                        elif interaction_particle_1 == 'Green':
                            if interaction_particle_2 == 'Red':
                                rules.append((green_group, red_group, strength))
                            elif interaction_particle_2 == 'Green':
                                rules.append((green_group, green_group, strength))
                            elif interaction_particle_2 == 'Blue':
                                rules.append((green_group, blue_group, strength))
                        elif interaction_particle_1 == 'Blue':
                            if interaction_particle_2 == 'Red':
                                rules.append((blue_group, red_group, strength))
                            elif interaction_particle_2 == 'Green':
                                rules.append((blue_group, green_group, strength))
                            elif interaction_particle_2 == 'Blue':
                                rules.append((blue_group, blue_group, strength))
                    if strength > 0:
                        number_rule += 1
                        text_rule = f'{interaction_particle_1} attracted to {interaction_particle_2} with {strength} force'
                        rules_label_all.append(UILabel(relative_rect=pygame.Rect((10, 380 + 30 * number_rule), (300, 20)), text=text_rule, manager=ui_manager))
                    if strength < 0:
                        number_rule += 1
                        text_rule = f'{interaction_particle_1} repelled from {interaction_particle_2} with {strength} force'
                        rules_label_all.append(UILabel(relative_rect=pygame.Rect((10, 380 + 30 * number_rule), (300, 20)), text=text_rule, manager=ui_manager))
                elif event.ui_element == delete_all_button:
                    delete_all_button.disable()
                    add_basic_button.enable()
                    number_rule = 0
                    rules.clear()
                    for i in range(len(rules_label_all)):
                        rules_label_all[i].kill()
                elif event.ui_element == add_basic_button:
                    delete_all_button.enable()
                    add_basic_button.disable()
                    base_rules()

        ui_manager.process_events(event)

    # Очистка экрана
    screen.fill(black)

    # Обработка частиц, если симуляция запущена
    if running_simulation:
        for i in range(len(rules)):
            rule(rules[i][0], rules[i][1], rules[i][2])
        
    # Отрисовка частиц
    draw_particles(particles)

    if show_gui_button.is_enabled and show_gui_button.pressed:
            # Получение текущей видимости элементов интерфейса
            current_visibility = not exit_button.visible
            # Изменение видимости всех элементов, кроме show_gui_button
            for element in ui_manager.get_sprite_group():
                if element != show_gui_button:
                    element.visible = current_visibility

    # Обновление элементов интерфейса
    ui_manager.update(time_delta)

    # Отрисовка элементов интерфейса
    ui_manager.draw_ui(screen)

    # Обновление экрана
    pygame.display.flip()

# Завершение работы Pygame
pygame.quit()
