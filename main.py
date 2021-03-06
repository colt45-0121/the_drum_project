import pygame
from pygame import mixer
pygame.init()

WIDTH = 1280
HEIGHT = 800

black = (0, 0, 0)
white = (255, 255, 255)
gray = (128, 128, 128)
dark_gray = (64, 64, 64)
green = (0, 255, 0)
gold = (255, 175, 55)
blue = (0, 255, 255)

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('DRUM')
label_font = pygame.font.Font('freesansbold.ttf', 30)
medium_font = pygame.font.Font('freesansbold.ttf', 20)
max_font = pygame.font.Font('freesansbold.ttf', 40)

fps = 60
timer = pygame.time.Clock()
beats = 8
instruments = 6
clicked = [[-1 for _ in range(beats)]for _ in range(instruments)]
active_list = [1 for _ in range(instruments)]
bpm = 240
playing = True
active_length = 0
active_beat = 1
beat_changed = True

hi_hat = mixer.Sound('beats/hi hat.WAV')
snare = mixer.Sound('beats/snare.WAV')
kick = mixer.Sound('beats/kick.WAV')
crash = mixer.Sound('beats/crash.WAV')
clap = mixer.Sound('beats/clap.WAV')
floor_tom = mixer.Sound('beats//tom.WAV')
pygame.mixer.set_num_channels(instruments*3)


def play_notes():
    for i in range(len(clicked)):
        if clicked[i][active_beat] == 1 and active_list[i] == 1:
            if i == 0:
                hi_hat.play()
            if i == 1:
                snare.play()
            if i == 2:
                kick.play()
            if i == 3:
                crash.play()
            if i == 4:
                clap.play()
            if i == 5:
                floor_tom.play()


def draw_grid(clicks, beat, active):
    left_box = pygame.draw.rect(screen, gray, [0, 0, 200, HEIGHT-200], 10)
    bottom_box = pygame.draw.rect(
        screen, gray, [0, HEIGHT-210, WIDTH, 200], 10)
    boxes = []
    colors = [gray, white, gray]

    hi_hat_text = label_font.render('Hi-Hat', True, colors[active[0]])
    screen.blit(hi_hat_text, (15, 40))
    snare_text = label_font.render('Snare', True, colors[active[1]])
    screen.blit(snare_text, (15, 140))
    kick_text = label_font.render('Bass-Drum', True, colors[active[2]])
    screen.blit(kick_text, (15, 240))
    crash_text = label_font.render('Crash', True, colors[active[3]])
    screen.blit(crash_text, (15, 340))
    clap_text = label_font.render('Clap', True, colors[active[4]])
    screen.blit(clap_text, (15, 440))
    floor_text = label_font.render('Floor-Tom', True, colors[active[5]])
    screen.blit(floor_text, (15, 540))
    for i in range(5):
        pygame.draw.line(screen, gray, (0, i*100+100), (190, i*100+100), 10)
    for i in range(beats):
        for j in range(instruments):
            if clicks[j][i] == -1:
                color = gray
            else:
                if active[j] == 1:
                    color = green
                else:
                    color = dark_gray
            rect = pygame.draw.rect(screen, color, [(
                i*(WIDTH-200)//beats)+200, (j*100), ((WIDTH-200)//beats), ((HEIGHT-200)//instruments)], 0, 10)
            pygame.draw.rect(screen, gold, [
                             (i*(WIDTH-200)//beats)+200, (j*100), ((WIDTH-200)//beats), ((HEIGHT-200)//instruments)], 10, 10)
            boxes.append((rect, (i, j)))
        pygame.draw.rect(screen, blue, [
                         beat*((WIDTH-200)//beats)+200, 0, ((WIDTH-200)//beats), instruments*100], 10, 10)
    return boxes


run = True
while run:
    timer.tick(fps)
    screen.fill(black)

    boxes = draw_grid(clicked, active_beat, active_list)

    play_pause = pygame.draw.rect(
        screen, gray, [50, HEIGHT-150, 200, 100], 0, 10)
    play_text = label_font.render('Play/Pause', True, white)
    screen.blit(play_text, (70, HEIGHT-130))
    if playing:
        play_text2 = medium_font.render('Playing', True, dark_gray)
    else:
        play_text2 = medium_font.render('Paused', True, dark_gray)
    screen.blit(play_text2, (70, HEIGHT-95))

    # bpm
    bpm_rect = pygame.draw.rect(
        screen, gray, [300, HEIGHT-150, 200, 100], 10, 10)
    bpm_text = medium_font.render('Beats Per Minute', True, white)
    screen.blit(bpm_text, (315, HEIGHT-130))
    bpm_text2 = label_font.render(str(bpm), True, white)
    screen.blit(bpm_text2, (370, HEIGHT-100))
    bpm_add_rect = pygame.draw.rect(
        screen, gray, [510, HEIGHT-150, 48, 48], 0, 10)
    bpm_sub_rect = pygame.draw.rect(
        screen, gray, [510, HEIGHT-100, 48, 48], 0, 10)
    add_text = label_font.render('+', True, white)
    sub_text = label_font.render('-', True, white)
    screen.blit(add_text, (525, HEIGHT-140))
    screen.blit(sub_text, (530, HEIGHT-90))
    # beats
    beats_rect = pygame.draw.rect(
        screen, gray, [600, HEIGHT-150, 200, 100], 10, 10)
    beats_text = medium_font.render('Beats In Loop', True, white)
    screen.blit(beats_text, (630, HEIGHT-130))
    beats_text2 = label_font.render(str(beats), True, white)
    screen.blit(beats_text2, (690, HEIGHT-100))
    beats_add_rect = pygame.draw.rect(
        screen, gray, [810, HEIGHT-150, 48, 48], 0, 10)
    beats_sub_rect = pygame.draw.rect(
        screen, gray, [810, HEIGHT-100, 48, 48], 0, 10)
    add_text2 = label_font.render('+', True, white)
    sub_text2 = label_font.render('-', True, white)
    screen.blit(add_text2, (825, HEIGHT-140))
    screen.blit(sub_text2, (830, HEIGHT-90))
    # instrument
    instrument_rects = []
    for i in range(instruments):
        rect = pygame.rect.Rect((0, i*100), (200, 100))
        instrument_rects.append(rect)
    # clear board
    clear_button = pygame.draw.rect(
        screen, gray, [950, HEIGHT-150, 250, 100], 0, 10)
    clear_text = max_font.render('CLEAR ALL', True, white)
    screen.blit(clear_text, (960, HEIGHT-115))

    if beat_changed:
        play_notes()
        beat_changed = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(boxes)):
                if boxes[i][0].collidepoint(event.pos):
                    coords = boxes[i][1]
                    clicked[coords[1]][coords[0]] *= -1
        if event.type == pygame.MOUSEBUTTONUP:
            if play_pause.collidepoint(event.pos):
                if playing:
                    playing = False
                else:
                    playing = True
            if bpm_add_rect.collidepoint(event.pos):
                bpm += 10
            elif bpm_sub_rect.collidepoint(event.pos):
                bpm -= 10
            if beats_add_rect.collidepoint(event.pos):
                beats += 1
                for i in range(len(clicked)):
                    clicked[i].append(-1)
            elif beats_sub_rect.collidepoint(event.pos):
                beats -= 1
                for i in range(len(clicked)):
                    clicked[i].pop(-1)
            for i in range(len(instrument_rects)):
                if instrument_rects[i].collidepoint(event.pos):
                    active_list[i] *= -1
            if clear_button.collidepoint(event.pos):
                clicked = [[-1 for _ in range(beats)]
                           for _ in range(instruments)]

    beat_length = 3600//bpm
    if playing:
        if active_length < beat_length:
            active_length += 1
        else:
            active_length = 0
            if active_beat < beats-1:
                active_beat += 1
                beat_changed = True
            else:
                active_beat = 0
                beat_changed = True

    pygame.display.flip()
pygame.quit()
