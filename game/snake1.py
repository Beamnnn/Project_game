import pygame
import random
import math
import sys

#Dimensions ขนาดความสูงและความกว้าง
WIDTH = 800
HEIGHT = 600

#Colors สี
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
white = (255,255,255)
black = (0,0,0)
#music and sound เพลงในการเล่นเกม 
pygame.mixer.init()
pygame.mixer.music.load("music.mp3")
pygame.mixer.music.play(-1)

#Snake square Dimensions ขนาดของหมีน้อย
snake_d = 40

#Food square Dimensions ขนาดของลุงตู่ 
food_d = 40

#Maximum distance to successfully eat food ระยะทางสูงสุดในการกินอาหารสำเร็จ
edible_dist = 40

#Collison with self distance ของกับระยะห่างของน้องหมี
collision_dist = edible_dist
lastscore=[]
with open("score.csv" ,"r")as f :
    for i in f:
        lastscore.append(int(i))

def round40(x):#เป็นฟังก์ที่ไว้รันเกม
    return 40* round(x/40)

def print_food(win,food,foodx,foody):#แลนดอม
    win.blit(food,(foodx,foody))

def check_if_eaten(win,x,y,foodx,foody): #ตรวจค่าของ
    dist = calc_dist(x,y,foodx,foody)
    if dist <= 20:
        return True
    else:
        return False

def check_if_collided(snake_list):#ตรวจว่าระยะห่างการโดนมีมากขนาดไหน
    for i in range(2,len(snake_list)):
        dist = calc_dist(snake_list[0][0],snake_list[0][1],snake_list[i][0],snake_list[i][1])
        if dist == 0:
            return True
    return False

def calc_dist(x1,y1,x2,y2): #ฟังก์ชั่นเกี่ยวกับสูตรคณิต
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def produce_food(snake_list,rectx,recty): 
    f = True
    while True:
        foodx = round40(random.randrange(0,WIDTH - food_d))
        foody = round40(random.randrange(0,HEIGHT - food_d))
        for x in snake_list:
            if calc_dist(x[0],x[1],foodx,foody) < collision_dist or (x[0] in range(2*rectx+1) and x[1] in range(2*recty+1)):
                f = False
                break
        if f:
            break
    return foodx, foody 
#คำนวณและตรวจสอบรอบสุดท้ายก่อนปริ้นซ์ค่าออกมา
def add_body(snake_list,moving):
    if moving is 'left':
        snake_list.append((snake_list[-1][0]+snake_d,snake_list[-1][1]))
    if moving is 'right':
        snake_list.append((snake_list[-1][0]-snake_d,snake_list[-1][1]))
    if moving is 'down':
        snake_list.append((snake_list[-1][0],snake_list[-1][1]-snake_d))
    if moving is 'up':
        snake_list.append((snake_list[-1][0],snake_list[-1][1]+snake_d))


def move_body(snake_list): #การเคลื่อนไหวของน้องหมีน้อย
    for i in range(len(snake_list)-1,0,-1):
        x = snake_list[i-1][0]
        y = snake_list[i-1][1]
        snake_list[i] = (x,y)

def print_body(win,body,snake_head,snake_list):
    for i in range(len(snake_list)-1,0,-1):
        win.blit(body,(snake_list[i][0],snake_list[i][1]))
    win.blit(snake_head,(snake_list[0][0],snake_list[0][1]))
#เช็คสัดส่วน
    
def game():

    #Initialization การเริ่มต้นของเกม
    pygame.init()
    win = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption('หมีน้อยจะกินบักตู่นะจ๊ะ')
    game_running = True

    #Loading Background Image อัพโหลดพื้นหลัง
    bg_img = pygame.image.load('img/bg.png')

    #Loading Food อัพโหลดอาหาร ตู่ 
    food = pygame.image.load('img/too.png')
    
    #Loading Snake Head, initially looking up อัพโหลดหัวงูเงยที่หน้าขึ้น
    head_img = pygame.image.load('img/up.png')

    #Loading Snake Body กำลังโหลดร่างกายน้องหมี
    body = pygame.image.load('img/oh.png') #สีตอนกิน //ร่างกาย
    
    #Initial snake length ความยาวหมีน้อยเริ่มต้น
    s_length = 1

    #start point จุดเริ่มต้น ขนาดของค่า
    x = WIDTH/2
    y = HEIGHT/2

    #Chage in dimension เช็คมิติของงู
    change_d = snake_d

    #change in x and y, initially moving upwards 
    x_change = 0
    y_change = -change_d
    moving = 'up'

    #Initialization of speed การเริ่มต้นของความเร็ว
    clock = pygame.time.Clock()

    #Initialization of list for handling snake body เริ่มต้นรายการรับมือน้องหมีน้อย
    snake_list = []
    snake_list.append((x,y))

    #Game over display เกมโอเวอร์ดิสเพลย์ หน้าเกม
    font_c = pygame.font.Font('freesansbold.ttf', 40)
    message_c = ' Game Over! Your score was: '
    text_c = font_c.render(message_c, True, white, black)
    textRect_c = text_c.get_rect()
    messagex = WIDTH/2
    messagey = HEIGHT/4
    textRect_c.center = (messagex, messagey)
    ##    คะแนนครั้งที่แล้ว
    font_l = pygame.font.Font('freesansbold.ttf',40)
    last_score = ' lastScore: '
    text_l = font_l.render(last_score, True, white, black)
    textRect_l = text_l.get_rect()
    lscore_rectx = WIDTH/2
    lscore_recty = HEIGHT/4+50
    textRect_l.center = (lscore_rectx,lscore_recty)
    replay_quit_img = pygame.image.load('img/y.png')

    #Live score display การแสดงคะแนนสด หน้าตาเกม
    font = pygame.font.Font('freesansbold.ttf',15)
    score_template = ' Score: '
    text = font.render(score_template, True, black, white)
    textRect = text.get_rect()
    score_rectx = 40
    score_recty = 15
    textRect.center = (score_rectx,score_recty)
    

    

    #Initialization การเริ่มต้นของการเริ่มเกม
    score = 0

    #Speed ความเร็ว
    speed = 10


    #Initial food coordinates พิกัดอาหารเบื้องต้น
    foodx,foody = produce_food(snake_list,score_rectx,score_recty)

    game_over = False
    eaten = False
    play_again = False
    break_out = False

    #Mouse coordinates initialized พิกัดของเมาส์เริ่มต้น
    mouse = (0,0)

    #Game loop ห่วงเกม
    while game_running:

        #Event Loop วนรอบกิจกรรม
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
                break
            
            if not game_over:

                #Keypress Conditions เงื่อนไขของคีย์
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        head_img = pygame.image.load('img/left.png') ##หัวงูหันซ้าย
                        x_change = -change_d
                        y_change = 0
                        moving = 'left'
                    if event.key == pygame.K_RIGHT:
                        head_img = pygame.image.load('img/right.png') #หัวงูหัวขวา
                        x_change = change_d
                        y_change = 0
                        moving = 'right'
                    if event.key == pygame.K_DOWN:
                        head_img = pygame.image.load('img/ori.png') #หัวงูหันลง
                        y_change = change_d
                        x_change = 0
                        moving = 'down'
                    if event.key == pygame.K_UP:
                        head_img = pygame.image.load('img/up.png') #หัวงูหันขึ้น
                        y_change = -change_d
                        x_change = 0
                        moving = 'up'
            
            else: #จุดเมาส์คลิกเกมโอเว่อ
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if mouse[0] in range(208,350) and mouse[1] in range(475,540):
                        break_out = True
                        play_again = True 
                        break
                    elif mouse[0] in range(454,605) and mouse[1] in range(475,540):
                        break_out = True
                        play_again = False
                        break
        if break_out:
            break

        if not game_over:
            
            #Updating Change in coordinates กำลังอัพเดทการเปลี่ยนแปลงพิกัด
            x += x_change
            y += y_change

            #Checking bounds เช็คขอบเขต
            if x>= WIDTH - snake_d:
                x = WIDTH - snake_d
            if x<= 0:
                x = 0
            if y>= HEIGHT - snake_d:
                y = HEIGHT - snake_d
            if y<= 0 :
                y = 0

            snake_xy = (x,y)
            if len(snake_list) > 0:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
                snake_list[0] = snake_xy
            else: 
                snake_list.append(snake_xy)

            #Check if snake has eaten food #เช็คว่างูกินอาหารหรือเปล่า
            eaten = check_if_eaten(win,x,y,foodx,foody)
                                        
            #Background Image ภาพพื้นหลัง
            win.blit(bg_img,(0,0))

            #Print new food if snake eats it  พิมพ์อาหารใหม่ถ้างูกิน
            if eaten:
                foodx,foody = produce_food(snake_list,score_rectx, score_recty)
                global i
                i = random.randrange(0,10)
                print_food(win,food,foodx,foody)
                s_length += 1
                
                #Update score เพิ่มหรือลดคะแนน
                score += 1

                #Adding Body เสริมร่างกาย
                add_body(snake_list,moving)

                #Increasing Speed เพิ่มความเร็ว
                #speed += 1

            else:
                print_food(win,food,foodx,foody)
            
            if check_if_collided(snake_list):
                game_over = True

            #Moving snake 
            move_body(snake_list)

            #Printing Snake
            print_body(win,body,head_img,snake_list)

            #Display Live Score สีฟอนต์เกมเริ่ม
            text = font.render(score_template + str(score) + ' ', True, black, white)
            win.blit(text,textRect)
 
        #If game is over  สีฟอนต์เกมจบ
        else:
            win.fill(black)
            text_c = font_c.render(message_c + str(score) + ' ', True, white, black)
            text_l = font_l.render(last_score + str(lastscore[0]) + ' ', True, white, black)
            with open("score.csv",'w') as f:
                f.write(str(score))

            #Display final score
            win.blit(text_c,textRect_c)
            win.blit(text_l,textRect_l)
            #Display Play or Quit 
            win.blit(replay_quit_img, (WIDTH/5,2*HEIGHT/3))

            #Mouse coordinates
            mouse = pygame.mouse.get_pos()
            
        #Updating display with specified time
        pygame.display.update()
        clock.tick(speed)
    
    if play_again: #รันเกมอีกที
        game()
    pygame.quit()
    sys.exit(0)

def main():
    game()

if __name__ == '__main__' :
    main()
