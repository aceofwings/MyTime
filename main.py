import pygame
import endpoints
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)

done = False

bgColor =  pygame.Color('#f4c330')

font = pygame.font.Font('Fixation.ttf', 40)

rendering = font.render("Love", 1, (255,255,0),(255,0,0))

textrect = rendering.get_rect()
textrect.centerx = screen.get_rect().centerx
textrect.centery = screen.get_rect().centery

screen.fill(bgColor)
screen.blit(rendering, textrect)


routes = endpoints.get_routes_of_interest()

while not done:
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
