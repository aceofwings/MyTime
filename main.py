import pygame
import time
import datetime
from routeinfo import Cache
from coordinates import deg2pix
pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
pygame.mouse.set_visible(False)

font = pygame.font.Font('Fixation.ttf', 60)

textColor = pygame.Color('#3237AA')
inactiveColor = pygame.Color('#5095AD')
busBGColor = pygame.Color('#2C6E84')

Buses = pygame.Surface((600 ,400))
BusRect = Buses.get_rect(center=(1500, 750))
Buses.set_alpha(200)
Buses.fill(busBGColor)

busText = font.render("Buses", 1, textColor)
textrect = busText.get_rect()
textrect.midtop = BusRect.midtop
textrect.y += 10

background = pygame.image.load("campus.png")


screen.blit(background, (0,0))
screen.blit(Buses, BusRect)
screen.blit(busText, textrect)

def redraw():
    screen.blit(background, (0,0))
    screen.blit(Buses, BusRect)
    screen.blit(busText, textrect)

    #pygame.draw.circle(screen,(255,0,0),deg2pix(t2x,t2y),10)
    #pygame.draw.circle(screen,(255,0,0),deg2pix(t3x,t3y),10)
def update_routes():
    Cache.update_stops()
    Cache.get_routes_of_interest()

def draw_route_texts():
    margin_left = 15
    start_pos = BusRect.topleft
    start_pos = (start_pos[0] + margin_left, start_pos[1] + 65 )
    renderings = []
    time_str = "None"
    for key,route in routes.items():
        routeColor = pygame.Color(route.color)
        if not route.active:
            routeColor = inactiveColor
            time_str = "OoS"
        elif route.route_stops[0].next_arrival_time is not None:
            timeDif = route.route_stops[0].next_arrival_time - time.time()
            time_str =  time.strftime("%M", time.gmtime(timeDif))
        elif route.active and route.route_stops[0].next_arrival_time is None :
            time_str = "No prediction"
        if route.active:
            pplat = route.bounds[0]
            pplon = route.bounds[1]
            pygame.draw.circle(screen,routeColor,deg2pix(pplat,pplon),20)
        route_name_graphic = font.render(route.alias + " - " + time_str , 1, routeColor)
        rect = route_name_graphic.get_rect()
        rect.topleft = start_pos
        screen.blit(route_name_graphic, rect)
        start_pos = (start_pos[0] , start_pos[1] + 60)

routes = Cache.get_routes_of_interest()
draw_route_texts()

done = False
while not done:
    update_routes()
    redraw()
    draw_route_texts()
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
pygame.quit()
