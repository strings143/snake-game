import cv2
import numpy as np
import pygame

import random, math, os
import string


pygame.init()

# 視窗設定
screen_width = 700
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()  # 時間控制int

# 變數
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 193, 112)
PINK = (255, 140, 250)
GREEN_BLUE = (79, 156, 156)
GREY = (150, 150, 150)
GREY2 = (130, 130, 130)
DARK_YELLOW = (228, 128, 16)
ORANGE=(219, 69, 0)
GROWN=(168, 56, 0)
YELLOW_FOOD=(238, 238, 47)

FPS = 10
score = 0

# 蛇設定 (頭、身體還會在主畫面設定初始化)
snake_size = 18
snake_speed = 20
snake_body = [(80, 100), (60, 100), (40, 100)]  # 蛇身體
snake_head = snake_body[0]  # 蛇頭
snake_len = len(snake_body)

# 顏色設定
snake_color = ORANGE
food_color = YELLOW_FOOD
score_color = BLACK

#ball位置
pos_x=0
pos_y=0

#蛇位置
temp_x=[0]*100
temp_y=[0]*100
count=0
old_x=0
old_y=0
new_x=0
new_y=0
direction = 1

def findR(img):
    hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

    lower=np.array([22,127,98])
    upper=np.array([38,210,255])
    mask=cv2.inRange(hsv,lower,upper)
    finalimg=cv2.bitwise_and(img,img,mask=mask)
    temp=findC(mask)
    return temp
def findC(img):
    controus,_=cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for cnt in controus:
        cv2.drawContours(oriImg,cnt,-1,(0,0,255),2)
        if cv2.contourArea(cnt)>500:
            vert=cv2.approxPolyDP(cnt,cv2.arcLength(cnt,True)*0.02,True)
            #print(len(vert))
            corners=len(vert)
            #（x，y）是矩阵的左上点坐标,（x+w，y+h）是矩阵的右下点坐标
            x,y,w,h=cv2.boundingRect(vert)
            #print('x', x, 'y', y)
            cv2.rectangle(oriImg,(x,y),(x+w,y+h),(0,255,0),4)

            return x,y
# 食物物件
class Food():
    def __init__(self, x, y):
        self.img = pygame.Surface((20, 20))
        self.img.fill(food_color)
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        screen.blit(self.img, self.rect)


# 顯示文字函數
def text_draw(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

#蛇移動
def move_snake(o_x,o_y,n_x,n_y,z):
    if n_x < o_x and (z != 2) and (n_x-o_x)<-20: # 往右
        z=1
        #print("right")
    elif n_x > o_x and (z != 1) and (n_x-o_x)>20: # 往左
        z=2
        #print("left")
    elif n_y < o_y and (z != 4) and (n_y-o_y)<-20: # 往上
        z=3
        #print("up")
    elif n_y > o_y and (z != 3)and (n_y-o_y)>20 :  # 往下
        z=4
        #print("down")
    else:
        z=z
    return z
# 遊戲字形設定
score_font = pygame.font.SysFont('Bauhaus 93', 40)  # 分數字形
title_font = pygame.font.SysFont('Bauhaus 93', 70)  # title 字形
rules_font = pygame.font.SysFont('Bauhaus 93', 25)  # rule 字形
start_font = pygame.font.SysFont('Bauhaus 93', 35)  # start 字形
die_font = pygame.font.SysFont('Bauhaus 93', 55)  # start 字形
c_font = pygame.font.SysFont('Bauhaus 93', 25)  # 繼續字形
rank_font = pygame.font.SysFont('Bauhaus 93', 45)
new_record_font = pygame.font.SysFont('Bauhaus 93', 30)

# 遊戲主畫面內容設定
title = 'Greedy Snake'
rules = '[WASD] to control the Snake!'
start = 'PRESS [SPACE] TO START'
Fake_snake = [(520, 222), (500, 222), (480, 222), (460, 222)]

# 死亡顯示畫面設定
die = 'YOU ARE DEAD!!'
score_text = 'YOUR SCROE: '
Continue = 'PRESS [SPACE] TO CONTINUE'
END='PRESS [Q] TO END'
# 遊戲迴圈前置設定
running = True
direction = 1  # 預設往右移動
food_check = False  # 確認是否有食物
menu = 0  # 畫面

save = False  # 使否已儲存分數
new_record = 99  # 進到榜單的名次
new_high = False  # 是否破紀錄

cap =cv2.VideoCapture(0)

while (running):
    clock.tick(FPS)
    screen.fill(YELLOW)
    # 参数ret的值为True或False，代表有没有读到图片,参数是frame，是当前截取一帧的图片
    ret, frame = cap.read()
    if ret:
        oriImg = frame.copy()
        pos = findR(frame)
        if pos != None:
            pos_x, pos_y = pos
            # print("x=", pos_x, "y=", pos_y)
        oriImg = cv2.flip(oriImg, 1)
        cv2.imshow('Opencv', oriImg)
        if cv2.waitKey(10) == ord('q'):
            pygame.quit()
    # 取得事件===================================
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_SPACE) and (menu != 1):
                direction = 1
                menu += 1
            if (event.key == pygame.K_SPACE) and (menu == -1):
                running = True
            if (event.key ==  ord('q')):
                pygame.quit()
    # 顯示主菜單=================================
    if menu == 0:
        text_draw(title, title_font, GROWN, 140, screen_height / 4)  # 印出標題
        #text_draw(rules, rules_font, GREY, 200, 360)  # 印出規則
        text_draw(start, start_font,DARK_YELLOW , 170, (screen_height / 3) * 2)  # 印出開始
        for i in range(len(Fake_snake)):  # 印出假蛇
            pygame.draw.rect(screen, snake_color,
                                pygame.Rect(Fake_snake[i][0], Fake_snake[i][1], snake_size, snake_size))

        # 初始化遊戲
        snake_body = [(80, 100), (60, 100), (40, 100)]  # 蛇身體
        snake_head = snake_body[0]  # 蛇頭
        #direction = 4
        food_check = False
        save = False
        score = 0
        new_record = 99
        new_high = False
        # 開始遊戲===================================
    elif menu == 1:
        # 生成食物
        if food_check == False:
            x = random.randrange(0, screen_width - 20)
            y = random.randrange(0, screen_height - 20)
            food = Food(x, y)
            food_check = True
        # 蛇移動和自我碰撞-----------------------------------------------------------------------
        temp_x[count]=pos_x
        temp_y[count]=pos_y
        if count == 0:
            old_x = temp_x[count]
            old_y = temp_y[count]
            #print("old_x=", old_x, "old_y=", old_y)
        else:
            new_x = temp_x[count]
            new_y = temp_y[count]
            direction=move_snake(old_x,old_y,new_x,new_y,direction)
            #print("new_x=", new_x, "new_y", new_y)
        #print(count, "=", temp_x[count])
        count=count+1
        if count>1:
            count=0
        # 蛇移動


        if direction == 1:
            snake_head = (snake_head[0] + snake_speed, snake_head[1])
        elif direction == 2:
            snake_head = (snake_head[0] - snake_speed, snake_head[1])
        elif direction == 3:
            snake_head = (snake_head[0], snake_head[1] - snake_speed)
        elif direction == 4:
            snake_head = (snake_head[0], snake_head[1] + snake_speed)
        # 與自己身體碰撞
        head_rect = pygame.Rect(snake_head[0], snake_head[1], snake_size, snake_size)  # 蛇頭 Rect設定
        for body in snake_body:
            body_rect = pygame.Rect(body[0], body[1], snake_size, snake_size)  # 蛇身 Rect設定
            if pygame.Rect.colliderect(head_rect, body_rect):  # 碰撞產生
                menu = -1
        # 加蛇頭、去蛇尾
        snake_body.insert(0, snake_head)
        snake_body.pop(len(snake_body) - 1)
        # 碰撞--------------------------------------------------------------------------------

        # 與食物碰撞
        if pygame.Rect.colliderect(head_rect, food.rect):
            if direction == 1:
                snake_head = (snake_head[0] + snake_speed, snake_head[1])
            if direction == 2:
                snake_head = (snake_head[0] - snake_speed, snake_head[1])
            if direction == 3:
                snake_head = (snake_head[0], snake_head[1] - snake_speed)
            if direction == 4:
                snake_head = (snake_head[0], snake_head[1] + snake_speed)
            snake_body.insert(0, snake_head)  # 增加蛇長度
            score += 10  # 分數增加
            del food  # 刪除食物
            food_check = False
        # 與邊界碰撞
        if snake_head[0] + (snake_size) >= screen_width or snake_head[0] <= 0:
            menu = -1
        if snake_head[1] + (snake_size) >= screen_height or snake_head[1] <= 0:
            menu = -1

        # 螢幕顯示-----------------------------------------------------------------------------
        if food_check == True:  # 如果食物存在
            food.update()  # 顯示食物
        snake_len = len(snake_body)  # 蛇長度更新
        for i in range(snake_len):  # 顯示蛇
            pygame.draw.rect(screen, snake_color,
                             pygame.Rect(snake_body[i][0], snake_body[i][1], snake_size, snake_size))
        text_draw(str(score), score_font, score_color, 15, 10)  # 分數顯示
        # 顯示分數畫面===============================
    elif menu == -1:

        # 顯示畫面
        for i in range(snake_len):  # 顯示蛇死亡狀態
            pygame.draw.rect(screen, snake_color,pygame.Rect(snake_body[i][0], snake_body[i][1], snake_size, snake_size))
        text_draw(die, die_font, RED, 150, 50)  # 顯示[死亡]字樣
        text_draw(score_text, score_font, GREEN_BLUE, 150, 110)  # 顯示[分數標題]字樣
        text_draw(str(score), score_font, GREEN_BLUE, 430, 110)  # 顯示[分數]字樣
        text_draw(Continue, c_font, BLACK, 190, 480)  # 顯示[繼續]字樣
        text_draw(END, c_font, BLACK, 250, 510)  # 顯示結束按鍵
        running=True


    # 螢幕更新==================================
    pygame.display.update()

print(score)
pygame.quit()