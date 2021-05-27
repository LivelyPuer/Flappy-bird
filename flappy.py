import pygame, sys, random
import datetime as dt
import asyncio
import webbrowser

fails = ["FAIL", "LOL", "HA-HA", "NOOB", "KILL"]

import sys
import os


def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 900))
    screen.blit(floor_surface, (floor_x_pos + 576, 900))


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(700, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(700, random_pipe_pos - 300))
    return bottom_pipe, top_pipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= speed_game
    visible_pipes = [pipe for pipe in pipes if pipe.right > -50]
    return visible_pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


def check_collision(pipes):
    global can_score, screenshot
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            can_score = True

            return False

    if bird_rect.top <= -100 or bird_rect.bottom >= 900:
        death_sound.play()
        can_score = True
        return False

    return True


def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
    return new_bird


def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
    return new_bird, new_bird_rect


def score_display(game_state):
    if game_state == 'main_game':
        str_score = str(int(score))
        nums = list()
        for num in str_score:
            nums.append(pygame.image.load(resource_path(f'sprites/{num}.png')).convert_alpha())
        if len(str_score) == 1:
            num1_rect = nums[0].get_rect(center=(288, 100))
            screen.blit(nums[0], num1_rect)
        elif len(str_score) == 2:
            num1_rect = nums[0].get_rect(center=(276, 100))
            num2_rect = nums[1].get_rect(center=(300, 100))
            screen.blit(nums[0], num1_rect)
            screen.blit(nums[1], num2_rect)
        elif len(str_score) == 3:
            num1_rect = nums[0].get_rect(center=(264, 100))
            num2_rect = nums[1].get_rect(center=(288, 100))
            num3_rect = nums[2].get_rect(center=(312, 100))
            screen.blit(nums[0], num1_rect)
            screen.blit(nums[1], num2_rect)
            screen.blit(nums[2], num3_rect)
        # score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        # score_rect = score_surface.get_rect(center=(288, 100))
        # screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        str_score = str(int(score))
        nums = list()
        for num in str_score:
            nums.append(pygame.image.load(resource_path(f'sprites/{num}.png')).convert_alpha())
        if len(str_score) == 1:
            num1_rect = nums[0].get_rect(center=(288, 100))
            screen.blit(nums[0], num1_rect)
        elif len(str_score) == 2:
            num1_rect = nums[0].get_rect(center=(276, 100))
            num2_rect = nums[1].get_rect(center=(300, 100))
            screen.blit(nums[0], num1_rect)
            screen.blit(nums[1], num2_rect)
        elif len(str_score) == 3:
            num1_rect = nums[0].get_rect(center=(264, 100))
            num2_rect = nums[1].get_rect(center=(288, 100))
            num3_rect = nums[2].get_rect(center=(312, 100))
            screen.blit(nums[0], num1_rect)
            screen.blit(nums[1], num2_rect)
            screen.blit(nums[2], num3_rect)

        high_score_surface = game_font.render(f'High score: {int(high_score)}', True,
                                              (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(288, 950))
        screen.blit(high_score_surface, high_score_rect)
        if not first_run:
            frame_surface = pygame.image.load(
                resource_path('sprites/pipe-frame.png')).convert_alpha()
            frame_rect = frame_surface.get_rect(center=(100, 790))
            frame_rect = pygame.Rect(frame_rect[0] - 20, frame_rect[1] - 30, frame_rect[2],
                                     frame_rect[3])
            frame_surface = pygame.transform.rotozoom(frame_surface, 20, 1)

            screenshot_surface = pygame.image.load(
                resource_path('data/screenshot.png')).convert_alpha()
            screenshot_rect = screenshot_surface.get_rect(center=(100, 770))
            screenshot_surface = pygame.transform.rotozoom(screenshot_surface, 20, 1)
            screen.blit(screenshot_surface, screenshot_rect)
            screen.blit(frame_surface, frame_rect)

            fail_font = pygame.font.Font(resource_path('04B_19.ttf'), fail_size_font)
            fail_surface = fail_font.render(fail_word, True,
                                            (0, 0, 0))
            fail_rect = high_score_surface.get_rect(center=(150, 720))
            fail_surface = pygame.transform.rotate(fail_surface, 20)
            screen.blit(fail_surface, fail_rect)
            # screen.blit(share_surface, share_rect)
            # screen.blit(share_text_black_surface, share_text_black_rect)
            # screen.blit(share_text_surface, share_text_rect)
            # screen.blit(facebook_surface, facebook_rect)
            # screen.blit(twitter_surface, twitter_rect)

    if game_state == 'end':
        screen.blit(game_over, game_over_end_rect)

        derect_surface = game_font.render(f'Directed by:', True, (0, 0, 0))
        derect_rect = derect_surface.get_rect(center=(288, 600))
        screen.blit(derect_surface, derect_rect)

        author_surface = game_font.render(f'LivelyPuer', True, (0, 0, 0))
        author_rect = author_surface.get_rect(center=(288, 650))
        screen.blit(author_surface, author_rect)


def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score


def pipe_score_check():
    global score, can_score, bg_surface, pipe_surface, now_speed, speed_game, speed_ground

    if pipe_list:
        for pipe in pipe_list:
            if 95 < pipe.centerx < 105 and can_score and score < 999:
                score += add_score
                if score in [20, 100, 200, 300, 600]:
                    speed_game += 1
                    speed_ground = speed_game
                    now_speed = game_speed_dict[speed_game]
                    pygame.time.set_timer(SPAWNPIPE, now_speed)

                score_sound.play()
                can_score = False
            if pipe.centerx < 0:
                can_score = True


def random_skin():
    global num_skin
    num_skin = random.randrange(1, 4)
    global bird_downflap, bird_midflap, bird_upflap, bird_frames
    bird_downflap = pygame.transform.scale2x(
        pygame.image.load(
            resource_path(f'sprites/{dict_skin[num_skin]}-downflap.png')).convert_alpha())
    bird_midflap = pygame.transform.scale2x(
        pygame.image.load(
            resource_path(f'sprites/{dict_skin[num_skin]}-midflap.png')).convert_alpha())
    bird_upflap = pygame.transform.scale2x(
        pygame.image.load(
            resource_path(f'sprites/{dict_skin[num_skin]}-upflap.png')).convert_alpha())
    bird_frames = [bird_downflap, bird_midflap, bird_upflap]


def night_to_day():
    global bg_surface, pipe_surface
    if now_count % 2 != 0:
        bg_surface = pygame.image.load(resource_path('sprites/background-night.png')).convert()
        pipe_surface = pygame.image.load(resource_path('sprites/pipe-red.png'))
    else:
        bg_surface = pygame.image.load(resource_path('sprites/background-day.png')).convert()
        pipe_surface = pygame.image.load(resource_path('sprites/pipe-green.png'))
    bg_surface = pygame.transform.scale2x(bg_surface)
    pipe_surface = pygame.transform.scale2x(pipe_surface)


async def make_screenshot():
    full_screen = screen.copy()
    cropped = pygame.Surface((200, 200))
    cropped.blit(full_screen, (0, 0), pygame.Rect((bird_rect[0] - 50, bird_rect[1] - 100, 200, 200)))
    pygame.image.save(cropped, "data/screenshot.png")


def bird_skin_died():
    global bird_surface, bird_rect
    bird_surface = pygame.transform.scale2x(
        pygame.image.load(resource_path(f'sprites/{dict_skin[num_skin]}-died.png')).convert_alpha())

    bird_rect = bird_surface.get_rect(center=(100, bird_rect.centery))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    pygame.init()
    pygame.display.set_caption('Flappy Bird by LivelyPuer')
    programIcon = pygame.image.load(resource_path('favicon.ico'))
    pygame.display.set_icon(programIcon)
    screen = pygame.display.set_mode((576, 1024))
    clock = pygame.time.Clock()
    game_font = pygame.font.Font(resource_path('04B_19.ttf'), 40)
    share_font = pygame.font.Font(resource_path("04B_19.TTF"), 60)

    # Game Variables
    game_speed_dict = {
        4: 900,
        5: 800,
        6: 700,
        7: 600,
        8: 600,
        9: 600,
    }
    old_speed = 4
    now_speed = game_speed_dict[old_speed]
    speed_game = old_speed
    speed_ground = old_speed

    speeds = [3000, 2000, 1500, 1000, 800, 700, 600]
    jump_impulse = 8
    gravity = 0.25
    bird_movement = 0
    game_active = False
    first_run = True
    fail_word = random.choice(fails)
    file = open(resource_path('data/score.txt'), 'r', encoding='utf-8')
    num = file.read()
    if num.isdigit():
        high_score = int(num)
    else:
        high_score = 0

    score = 0
    add_score = 1
    now_count = 0
    can_score = True
    num_skin = 1
    dict_skin = {
        1: 'yellowbird',
        2: 'bluebird',
        3: 'redbird',
    }
    night_to_day()

    floor_surface = pygame.image.load(resource_path('sprites/base.png')).convert()
    floor_surface = pygame.transform.scale2x(floor_surface)
    floor_x_pos = 0

    bird_downflap = pygame.transform.scale2x(
        pygame.image.load(resource_path('sprites/yellowbird-downflap.png')).convert_alpha())
    bird_midflap = pygame.transform.scale2x(
        pygame.image.load(resource_path('sprites/yellowbird-midflap.png')).convert_alpha())
    bird_upflap = pygame.transform.scale2x(
        pygame.image.load(resource_path('sprites/yellowbird-upflap.png')).convert_alpha())
    bird_frames = list()
    random_skin()
    bird_index = 0
    bird_surface = bird_frames[bird_index]
    bird_rect = bird_surface.get_rect(center=(100, 512))

    game_over = pygame.transform.scale2x(
        pygame.image.load(resource_path('sprites/gameover.png')).convert_alpha())
    game_over_end_rect = game_over.get_rect(center=(288, 412))

    share_text_pos = (400, 692)
    share_text_surface = share_font.render("Share:", True, (255, 255, 255))
    share_text_rect = share_text_surface.get_rect(center=share_text_pos)

    share_text_black_surface = share_font.render("Share:", True, (0, 0, 0))
    share_text_black_rect = share_text_black_surface.get_rect(
        center=tuple(map(lambda x: x + 5, share_text_pos)))
    #
    # share_surface = pygame.image.load('sprites/share.png').convert_alpha()
    # share_rect = share_surface.get_rect(center=(300, 760))
    #
    # facebook_surface = pygame.image.load('sprites/facebook.png').convert_alpha()
    # facebook_rect = facebook_surface.get_rect(center=(400, 760))
    #
    # twitter_surface = pygame.image.load('sprites/twitter.png').convert_alpha()
    # twitter_rect = twitter_surface.get_rect(center=(500, 760))

    BIRDFLAP = pygame.USEREVENT + 1
    pygame.time.set_timer(BIRDFLAP, 200)

    pipe_list = []
    SPAWNPIPE = pygame.USEREVENT
    pygame.time.set_timer(SPAWNPIPE, now_speed)
    pipe_height = [400, 500, 600, 700, 800]

    game_over_surface = pygame.transform.scale2x(
        pygame.image.load(resource_path('sprites/message.png')).convert_alpha())
    game_over_rect = game_over_surface.get_rect(center=(288, 412))

    pipe_frame_surface = pygame.image.load(resource_path('sprites/pipe-frame.png')).convert_alpha()
    pipe_frame_rect = pipe_frame_surface.get_rect(center=(288, 512))

    flap_sound = pygame.mixer.Sound(resource_path('audio/wing.wav'))
    death_sound = pygame.mixer.Sound(resource_path('audio/hit.wav'))
    score_sound = pygame.mixer.Sound(resource_path('audio/point.wav'))
    ending = pygame.mixer.Sound(resource_path('audio/ending.mp3'))
    play_end = False
    score_sound_countdown = 100

    SCOREEVENT = pygame.USEREVENT + 2
    pygame.time.set_timer(SCOREEVENT, 100)

    FAILFICKER = pygame.USEREVENT + 3
    pygame.time.set_timer(FAILFICKER, 30)
    big = True
    min_fail_size = 40
    max_fail_size = 60
    fail_size_font = 40

    NIGHTTIMER = pygame.USEREVENT + 4
    pygame.time.set_timer(NIGHTTIMER, 24000)

    screenshot = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                file.close()
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if first_run:
                        first_run = False
                        game_active = True
                    elif game_active:
                        bird_movement = 0
                        bird_movement -= jump_impulse
                        flap_sound.play()
                    elif not game_active:
                        random_skin()
                        speed_game = old_speed
                        ending.stop()
                        play_end = False
                        game_active = True
                        pipe_list.clear()
                        bird_rect.center = (100, 512)
                        bird_movement = 0
                        score = 0

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    screenshot = True
                if event.key == pygame.K_SPACE and first_run:
                    first_run = False
                    game_active = True
                elif event.key == pygame.K_SPACE and game_active:
                    bird_movement = 0
                    bird_movement -= jump_impulse
                    flap_sound.play()
                elif event.key == pygame.K_SPACE and not game_active:
                    random_skin()
                    ending.stop()
                    play_end = False
                    speed_game = old_speed
                    game_active = True
                    pipe_list.clear()
                    bird_rect.center = (100, 512)
                    bird_movement = 0
                    score = 0

            if event.type == SPAWNPIPE and game_active:
                pipe_list.extend(create_pipe())

            if event.type == BIRDFLAP:
                if game_active:
                    if bird_index < 2:
                        bird_index += 1
                    else:
                        bird_index = 0

                    bird_surface, bird_rect = bird_animation()
            if event.type == FAILFICKER:
                if fail_size_font > max_fail_size:
                    big = False
                elif fail_size_font < min_fail_size:
                    big = True
                if big:
                    fail_size_font += 2
                else:
                    fail_size_font -= 2
            if event.type == NIGHTTIMER and game_active:
                now_count += 1
                night_to_day()

        if score >= 999:
            screen.blit(game_over, game_over.get_rect())
        screen.blit(bg_surface, (0, 0))
        if first_run:
            screen.blit(game_over_surface, game_over_rect)
            score_display('game_over')
            draw_floor()
        elif game_active:
            bird_movement += gravity
            bird_rect.centery += bird_movement
            game_active = check_collision(pipe_list)
            if not game_active:
                fail_word = random.choice(fails)
                bird_skin_died()
                speed_game = old_speed
                speed_ground = old_speed
                now_speed = game_speed_dict[old_speed]
                pygame.time.set_timer(SPAWNPIPE, now_speed)
                screenshot = True
            rotated_bird = rotate_bird(bird_surface)
            screen.blit(rotated_bird, bird_rect)
            if score >= 999:
                if not play_end:
                    ending.play()
                    play_end = True
                speed_game = 0
            pipe_list = move_pipes(pipe_list)
            draw_pipes(pipe_list)

            pipe_score_check()

            score_display('main_game')
            if score >= 999:
                score_display('end')
            # Floor
            floor_x_pos -= speed_ground
            draw_floor()
            if floor_x_pos <= -576:
                floor_x_pos = 0
        else:
            high_score = update_score(score, high_score)
            file = open(resource_path('data/score.txt'), 'w')
            file.write(str(high_score))
            file.close()
            if bird_rect.bottom < 870:
                bird_movement += gravity
                bird_rect.centery += bird_movement
            else:
                bird_rect.center = (100, 870)
            draw_pipes(pipe_list)
            rotated_bird = rotate_bird(bird_surface)
            screen.blit(rotated_bird, bird_rect)
            draw_floor()

            score_display('game_over')
            screen.blit(game_over_surface, game_over_rect)
        if screenshot:
            loop.run_until_complete(make_screenshot())
            screenshot = False
        pygame.display.update()
        clock.tick(120)
