import pygame
from routeinfo import Cache
pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
pygame.mouse.set_visible(False)

done = False

bgColor =  pygame.Color('#f4c330')

inactiveColor = pygame.Color('#BEB7A4')

textColor = pygame.Color('#0C0B0A')

font = pygame.font.Font('Yonky.ttf', 60)

rendering = font.render("Buses", 1, textColor)

routes = Cache.get_routes_of_interest()

BusesRect = pygame.draw.rect(screen, (0,0,0), (1200,150,600 ,400), 3)

textrect = rendering.get_rect()
textrect.midtop = BusesRect.midtop
textrect.y -= 70
#= screen.get_rect().centery


bg = pygame.image.load("campus.png")
screen.blit(bg, (0,0))
screen.blit(rendering, textrect)

def draw():
    pygame.draw.rect(screen, (0,0,0), (1200,150,600 ,400), 3)

def update_routes():
    Cache.update_stops()
def draw_route_texts():
    margin_left = 20
    start_pos = BusesRect.topleft
    start_pos = (start_pos[0] + margin_left, start_pos[1] + 30 )
    renderings = []
    for key,route in routes.items():

        routeColor = pygame.Color("#" + route.color)
        if not route.active:
            routeColor = inactiveColor

        route_name_graphic = font.render(route.alias + " - " , 1, routeColor)
        rect = route_name_graphic.get_rect()
        rect.topleft = start_pos
        screen.blit(route_name_graphic, rect)
        start_pos = (start_pos[0] , start_pos[1] + 60)





draw_route_texts()

while not done:
    update_routes()
    draw()
    draw_route_texts()
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
pygame.quit()
#
# pygame.display.set_caption('font example')
# size = [640, 480]
# screen = pygame.display.set_mode(size)
#
# clock = pygame.time.Clock()
#
# basicfont = pygame.font.SysFont(None, 48)
# text = basicfont.render('Hello World!', True, (255, 0, 0), (255, 255, 255))
# textrect = text.get_rect()
# textrect.centerx = screen.get_rect().centerx
# textrect.centery = screen.get_rect().centery
#
# screen.fill((255, 255, 255))
# screen.blit(text, textrect)
#
# pygame.display.update()
#
# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()
#
#     clock.tick(20)
