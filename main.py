import pygame
import time
import datetime
from routeinfo import Cache
pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
pygame.mouse.set_visible(False)

font = pygame.font.Font('Fixation.ttf', 60)

textColor = pygame.Color('#3237AA')
highlightColor = pygame.Color('#E5471A')
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
def update_routes():
    #Cache.update_stops()
    Cache.get_routes_of_interest()

def draw_route_texts():
    margin_left = 15
    start_pos = BusRect.topleft
    start_pos = (start_pos[0] + margin_left, start_pos[1] + 65 )
    renderings = []
    time_str = "None"
    for key,route in Cache.get_routes_of_interest().items():
        routeColor = pygame.Color("#" + route.color)
        if not route.active:
            routeColor = highlightColor
            time_str = "OoS"
        elif route.route_stops[0].next_arrival_time is not None:
            timeDif = route.route_stops[0].next_arrival_time - time.time()
            routeColor = textColor
            time_str =  time.strftime("%M", time.gmtime(timeDif))
        elif route.active and route.route_stops[0].next_arrival_time is None :
            print( route.route_stops[0])
            time_str = "No prediction"

        route_name_graphic = font.render(route.alias + " - " + time_str , 1, routeColor)
        rect = route_name_graphic.get_rect()
        rect.topleft = start_pos
        screen.blit(route_name_graphic, rect)
        start_pos = (start_pos[0] , start_pos[1] + 60)


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
