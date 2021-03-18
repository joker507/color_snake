import cv2
import numpy as np
from random import randint
from random import choice
import time


# 游戏变量

# 每个单元格的宽度
CELL_SIZE = 8
#每一行有多少个单元格
BOARD_SIZE = 80
#速度
SPEED = 5
#小蛇没吃掉一个苹果后，小蛇增长的速度
GROWTH = 2

#判断苹果是否被吃
eaten = True
#判断是否退出游戏
quit = False
#变量增长
grow = 0

#储存小蛇
snake = []
#得分
core = 0
last_core = 0 #上一次得分



class Head:
    '''头部'''
    def __init__(self,direction,x,y):
        #蛇头的运动方向
        self.direction = direction
        self.x = x
        self.y = y
    
    def move(self):
        #移动
        if self.direction == 0:
            self.x += 1 #右
        elif self.direction == 1:
            self.y += 1 #下
        elif self.direction == 2:
            self.x -= 1 #左
        elif self.direction == 3:
            self.y -= 1 #上


class SnakePart:
    '''身体'''
    def __init__(self,front,x,y):
        #front： 蛇身小块移动的下一个位置点
        self.front = front
        self.x = x
        self.y = y

    #移动函数，当前小块的下一个位置为当前小块的前一个小块当前的位置
    def move(self):
        self.x = self.front.x
        self.y = self.front.y
    



# 构建窗口并获取焦点
def win_focus():
    cv2.namedWindow('Snake Game',cv2.WINDOW_AUTOSIZE)
    board = np.zeros([BOARD_SIZE * CELL_SIZE,BOARD_SIZE * CELL_SIZE,3])
    cv2.imshow("Snake Game",board)
    cv2.setWindowProperty("Snake Game",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_AUTOSIZE)
    cv2.waitKey(2000)
    cv2.setWindowProperty("Snake Game",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_AUTOSIZE)

#展示游戏：
def display():
    #创建黑色背景板
    board = np.zeros([BOARD_SIZE,BOARD_SIZE,3]) 
    #画蛇身绿色
    for part in snake:
        board[part.y, part.x] = [randint(0,255),randint(0,255),randint(0,255)]
    #画苹果红色
    board[appley,applex] = [randint(0,255),randint(0,255),randint(0,255)]
    #刷新背景版，返回键盘信息
    cv2.imshow("Snake Game",np.uint8(board.repeat(CELL_SIZE,0).repeat(CELL_SIZE,1)))
    key = cv2.waitKey(int(1000/SPEED))

    return key


def start():
    SPEED = 5
    snake = []
    GROWTH = 2
    eaten = True
    quit = False
    grow = 0
    core = 0
    head = Head(0,int((BOARD_SIZE - 1)/2),int((BOARD_SIZE - 1)/2))
    snake.append(head) #初始化蛇只有蛇头
    cv2.waitKey(0)
    return head,snake

def end():
    global last_core
    global core
    global SPEED
    end_img = np.zeros([300,600,3]) + 255
    end_img = cv2.putText(end_img, 'game continue: blank space', (100, 200), cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,0,0),2)
    end_img = cv2.putText(end_img, 'game over: Esc ', (100, 220), cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,0,0),2)
    end_img = cv2.putText(end_img, 'core:'+str(core), (100, 100), cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)
    end_img = cv2.putText(end_img, 'lastcore:'+str(last_core), (100, 150), cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)
    cv2.imshow("Game end",end_img)
    
    end_key = cv2.waitKey()

    while (end_key != ord(' ')) and (end_key != 27):
        end_key = cv2.waitKey()
    cv2.destroyAllWindows()
    last_core = core
    core = 0
    SPEED = 5
    return end_key

def pause():
    #暂停
    while True:
        if cv2.waitKey(0) == ord(' '):
            break

if __name__ == '__main__':

    head,snake = start()
    # input()
    while not quit:            
        # game loop
        
        #生成苹果 并判断有无吃到
        if eaten:
            #将二维地图——》一维序列 #地图的索引值
            s = list(range(0,BOARD_SIZE ** 2))
            #将序列中被小蛇占有的指踢掉 #删除蛇占有的索引值
            for part in snake:
                s.remove(part.x * BOARD_SIZE + part.y)
            #随机生成apple 的地址
            a = choice(s)
            applex = int(a/BOARD_SIZE)
            appley = a % (BOARD_SIZE-20) 

            eaten = False #此时状态是没有吃到

        #刷新屏幕
        key = display()

        #根据按键信息控制小蛇
        if key == 8 or key == 27:
            break
        elif key == ord('d') and head.direction != 2: #防止自己撞自己
            head.direction = 0
        elif key == ord('s') and head.direction != 3:
            head.direction = 1
        elif key == ord('a') and head.direction != 0:
            head.direction = 2
        elif key == ord('w') and head.direction != 1:
            head.direction = 3
        elif key == ord(' '):
            pause()

        # 移动蛇尾和蛇头，蛇头由上面方向给定
        for part in snake[::-1]: #列表反转后取出，先取出蛇尾
            part.move()
        
        #小蛇吃到苹果后要长身体
        if grow > 0:
            #在蛇后面添加上新的蛇身块
            snake.append(SnakePart(snake[-1],subx,suby))
            grow -= 1


                    #当蛇头碰到苹果
        if applex == head.x and appley == head.y:
            subx = snake[-1].x
            suby = snake[-1].y
            eaten = True #吃到了
            grow += GROWTH #增长长度
            SPEED += 2 # 速度 + 2
            core += 1 #得分 +1

        #游戏失败判断
        if head.x < 0 or head.x > BOARD_SIZE-1 or head.y < 0 or head.y > BOARD_SIZE-1:
            end_key = end()
            if not end_key == ord(' '):
                quit = True
            else:
                head,snake = start()

        #碰撞蛇身
        for part in snake[1::]: #去掉蛇头
            if head.x == part.x and head.y == part.y:
                end_key = end()
                if not end_key == ord(' '):
                    quit = True
                else:
                    head,snake = start()
                break
            
        if quit:
            break 

