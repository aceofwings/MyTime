import pygame
import time
import datetime
from routeinfo import Cache
from coordinates import deg2pix
pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((1920,1080))#, pygame.FULLSCREEN)
pygame.mouse.set_visible(False)

font = pygame.font.Font('Hack.ttf', 60)

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
    Cache.update_vehicle_locations()

def draw_route_texts():
    margin_left = 15
    start_pos = BusRect.topleft
    start_pos = (start_pos[0] + margin_left, start_pos[1] + 65 )
    renderings = []
    time_str = "None"
    bounds = Cache.update_vehicle_locations()
    for key,route in Cache.get_routes_of_interest().items():
        if not route.active:
            routeColor = highlightColor
            time_str = "OoS"
        elif route.route_stops[-1].next_arrival_time is not None: #The next stop time estimation time exists
            timeDif = route.route_stops[0].next_arrival_time - time.time()
            routeColor = textColor
            time_str =  time.strftime("%M", time.gmtime(timeDif))
            routeColor = pygame.Color("#" + route.color)
            pygame.draw.circle(screen,routeColor,deg2pix(bounds[key][0],bounds[key][1]),20)#Decimal to pixel coordinate
        elif route.active and route.route_stops[0].next_arrival_time is None :
            time_str = "Error"
            routeColor = pygame.Color("#8c0202")

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
