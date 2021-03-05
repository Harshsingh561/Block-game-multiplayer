import pygame
import socket
import threading

s = socket.socket()
host = 'DESKTOP-RDTFRVP'
s.connect((host, 9999))
print("Connected")
pygame.init()
screen_width = 500
screen_height = 600
display_window = pygame.display.set_mode((screen_width, screen_height))
exit = True
velocity_init = 10
red = (255, 0, 0)
class t:
        def __init__(self):
                self.pos_x = 20
                self.pos_y = 70
                self.clock = pygame.time.Clock()
                self.pos2_x = 60
                self.pos2_y = 90
                self.velocity_x = 0
                self.velocity_x2 = 0
                self.velocity_y2 = 0
                self.velocity_y = 0
        def func(self):
                while True:
                        msg = s.recv(1024).decode()
                        if 'x' in msg:
                                msg=msg.replace('x', '')
                                self.velocity_x2 = int(msg)
                                self.velocity_y2=0
                        elif 'y' in msg:
                                msg=msg.replace('y', '')
                                self.velocity_y2=int(msg)
                                self.velocity_x2 = 0
                        self.pos_x+=self.velocity_x2
                        self.pos_y+=self.velocity_y2
                        pygame.display.update()
                        self.clock.tick(40)

cl = t()
while exit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                cl.velocity_x = velocity_init
                cl.velocity_y = 0
            elif event.key == pygame.K_LEFT:
                cl.velocity_x = -velocity_init
                cl.velocity_y = 0
            elif event.key == pygame.K_DOWN:
                cl.velocity_y = velocity_init
                cl.velocity_x = 0
            elif event.key == pygame.K_UP:
                cl.velocity_y = -velocity_init
                cl.velocity_x = 0
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                cl.velocity_x = 0
                cl.velocity_y = 0
            elif event.key == pygame.K_LEFT:
                cl.velocity_x = 0
                cl.velocity_y = 0
            elif event.key == pygame.K_DOWN:
                cl.velocity_y = 0
                cl.velocity_x = 0
            elif event.key == pygame.K_UP:
                cl.velocity_y = 0
                cl.velocity_x = 0
    cl.pos2_x += cl.velocity_x
    cl.pos2_y += cl.velocity_y
    s.send(f'x{cl.velocity_x}'.encode())
    s.send(f'y{cl.velocity_y}'.encode())
    display_window.fill((0, 0, 0))
    pygame.draw.rect(display_window, red, [cl.pos_x, cl.pos_y, 45, 45])
    pygame.draw.rect(display_window, red, [cl.pos2_x, cl.pos2_y, 45, 45])
    thr = threading.Thread(target=cl.func)
    thr.start()
    pygame.display.update()
    cl.clock.tick(40)