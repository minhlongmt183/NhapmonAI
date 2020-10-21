import pygame
import time




def draw_screen(screen, color):
    pygame.draw.rect(screen, color, (100,50,50,50))
    pygame.draw.rect(screen, color, (100,200,50,50))
    pygame.draw.rect(screen, color, (200,50,50,50))
    pygame.draw.rect(screen, color, (200,200,50,50))
    pygame.draw.rect(screen, color, (300,50,150,50))
    pygame.draw.rect(screen, color, (300,200,150,50))

def draw_text(screen, mins_plus_text, secs_plus_text, mins_minus_text,
        secs_minus_text, start_text, reset_text, tmins, tsecs, tcolon):
    screen.blit(mins_plus_text, (124, 70))
    screen.blit(secs_minus_text, (124, 220))
    screen.blit(mins_minus_text, (226, 70))
    screen.blit(secs_minus_text, (226, 220))
    screen.blit(start_text, (370, 70))
    screen.blit(reset_text, (370, 220))

    screen.blit(tmins, (110, 125))
    screen.blit(tcolon, (170, 125))
    screen.blit(tsecs, (210, 125))

def update_time(mins, secs, number_font):
    tmins   =   number_font.render(str(mins), False, (197, 228, 109))
    tsecs   =   number_font.render(str(secs), False, (197, 228, 109))

    return  tmins, tsecs

def isClick(x, y, pos_x, pos_y, w, h):
    if (x < pos_x) or (x > pos_x + w):
        return False
    elif (y < pos_y) or (y > pos_y + h):
        return False

    return True



def main():
    # time
    secs    = 0
    mins    = 0

    # color
    GREY    = (128,128,128)
    WHITE   = (253, 253, 255)

    # state
    running = True


    pygame.init()
    screen = pygame.display.set_mode((500, 600))
        # create a text file
    pygame.font.init()
    text_font       =   pygame.font.SysFont('Comic San MS', 40)
    number_font     =   pygame.font.SysFont('Comic San MS', 80)

    mins_plus_text  =   text_font.render("+", False, (0, 0, 0))
    secs_plus_text  =   text_font.render("+", False, (0, 0, 0))
    mins_minus_text =   text_font.render("-", False, (0,0, 0))
    secs_minus_text =   text_font.render("-", False, (0,0, 0))
    start_text      =   text_font.render("Start", False, (0, 0, 0))
    reset_text      =   text_font.render("Reset", False, (0, 0, 0))

    tmins   =   number_font.render("0", False, (197, 228, 109))
    tsecs   =   number_font.render("0", False, (197, 228, 109))
    tcolon  =   number_font.render(":", False, (197, 228, 109))


    start_btn       = False
    mins_plus_btn   = False
    secs_plus_btn   = False
    
    mins = 0
    secs = 0

    while running:
        screen.fill(GREY)

        # Get mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()

        draw_screen(screen, WHITE)



        if (start_btn):
            if (mins == 0 and secs == 0):
                start_btn = False
            elif secs == 0:
                mins = mins - 1
                secs = 59
            else:
                secs = secs - 1
        elif secs_plus_btn:
            if (mins == 59 and secs == 59):
                pass
            elif secs == 59:
                mins = mins + 1
                secs = 0
            else:
                secs = secs + 1
            
            secs_plus_btn = False

        elif mins_plus_btn:
            if (mins == 59):
                pass
            else:
                mins = mins + 1
            mins_plus_btn = False

        tmins, tsecs = update_time(mins, secs, number_font)
        draw_text(screen, mins_plus_text, secs_plus_text, mins_minus_text, 
                secs_minus_text, start_text, reset_text, tmins, tsecs, tcolon)
        if start_btn:
            time.sleep(1)
        

            # time.sleep(1000)




        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1 and start_btn == False: 
                    if  isClick(mouse_x, mouse_y, 300,50,150,50):
                        print("start click")
                        start_btn = True
                        break
                    if  isClick(mouse_x, mouse_y, 100,50,50,50):
                        mins_plus_btn = True 

            if event.type == pygame.QUIT:
                print("exit")
                running = False    

        pygame.display.flip()

    pygame.quit()





if __name__ == '__main__':
    main()