import pygame
import pygame_gui
import string
from random import choice
import re
import sys
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from os import system

#---------------------------------------------------------------
#---------------------------------------------------------------
#The important stuff
#---------------------------------------------------------------
#---------------------------------------------------------------
pygame.init()

BLUE=(38, 63, 106)

pygame.display.set_caption('Whatsapp Spam Bot')
icon = pygame.image.load('images/icon.png')
pygame.display.set_icon(icon)

screen = pygame.display.set_mode((1000,800))
scan_screen = pygame.display.set_mode((1000,800))
attack_screen = pygame.display.set_mode((1000,800))


manager = pygame_gui.UIManager((1000,800))


clock = pygame.time.Clock()

#---------------------------------------------------------------
#---------------------------------------------------------------
#Settings
#---------------------------------------------------------------
#---------------------------------------------------------------

GREY = (48,48,48)
DARK_BLUE = (48, 48, 68)
LIGHT_GREY = (68,68,68)

bannerImg = pygame.image.load('images/banner.png')
guide_Img = pygame.image.load('images/scan_guide.png')
U_font = pygame.font.Font('fonts/Ubuntu-L.ttf', 38)
MiniU_font = pygame.font.Font('fonts/Ubuntu-L.ttf', 28)

frames = 0

alphabet = list(string.ascii_letters)
numbers = ['0','1','2','3','4','5','6','7','8','9']
numbers2 = ['-','0','1','2','3','4','5','6','7','8','9']

contacts = []

random_message = ['My pet kangaroo just died of cancer', 'My mom just died LMAO', 'Im an a fart who has nothing to do in his free time']
#---------------------------------------------------------------
#---------------------------------------------------------------
#Widgets
#---------------------------------------------------------------
#---------------------------------------------------------------


#---------------------------------------------------------------
#---------------------------------------------------------------
#functions
#---------------------------------------------------------------
#---------------------------------------------------------------

def banner():
    screen.blit(bannerImg, (80,0))


def make_text_input(name: str, cords: tuple, size: tuple):
    name = pygame_gui.elements.ui_text_entry_line.UITextEntryLine(relative_rect=pygame.Rect(cords, size),
                                                                    manager=manager)
def generate_random_message():
    new_msg = choice(random_message)

    if message_box.get_text() == new_msg:
        generate_random_message()
    else:
        message_box.set_text(str(new_msg))


def outlines():
    #big rectangle + outline 
    pygame.draw.rect(screen, LIGHT_GREY, (15,125,970,410))
    pygame.draw.rect(screen, GREY, (20,130,960,400))

    #smaller Rectangle + outline in bottom left corner
    pygame.draw.rect(screen, LIGHT_GREY, (15, 545, 460, 248))
    pygame.draw.rect(screen, (GREY), (20,550,450,238))

    #smaller Rectangle + outline in bottom right/middle-ish
    pygame.draw.rect(screen, LIGHT_GREY, (482, 545, 300, 248))
    pygame.draw.rect(screen, (GREY), (487,550,290,238))

    #contacts section
    contacts_title = U_font.render('Targets', True, (220,220,220))
    screen.blit(contacts_title, (420,130))

    contact_1 = MiniU_font.render('Contact 1:', True, (220,220,220))
    screen.blit(contact_1, (30,210))

    contact_2 = MiniU_font.render('Contact 2:', True, (220,220,220))
    screen.blit(contact_2, (600,210))

    contact_3 = MiniU_font.render('Contact 3:', True, (220,220,220))
    screen.blit(contact_3, (30,300))

    contact_4 = MiniU_font.render('Contact 4:', True, (220,220,220))
    screen.blit(contact_4, (600,300))

    contact_5 = MiniU_font.render('Contact 5:', True, (220,220,220))
    screen.blit(contact_5, (30,390))

    contact_6 = MiniU_font.render('Contact 6:', True, (220,220,220))
    screen.blit(contact_6, (600,390))

    contact_7 = MiniU_font.render('Contact 7:', True, (220,220,220))
    screen.blit(contact_7, (30,480))

    contact_8 = MiniU_font.render('Contact 8:', True, (220,220,220))
    screen.blit(contact_8, (600,480))

    #message section
    message_text = U_font.render('Message', True, (220,220,220))
    screen.blit(message_text, (170,550))

    #number of times + timeout section
    times_text = MiniU_font.render('Number Of Msgs', True, (220,220,220))
    screen.blit(times_text, (525,560))

    timeout_text = MiniU_font.render('Timeout (Optional)', True, (220,220,220))
    screen.blit(timeout_text, (515,670))

    """
    c1 = contact1.get_text()
    c2 = contact2.get_text()
    c3 = contact3.get_text()
    c4 = contact4.get_text()
    c5 = contact5.get_text()
    c6 = contact6.get_text()
    c7 = contact7.get_text()
    c8 = contact8.get_text()
    """

def filter_all():
    #filters contacts
    global contacts
    global c1
    global c2
    global c3
    global c4
    global c5
    global c6
    global c7
    global c8

    contacts.append(c1)
    contacts.append(c2)
    contacts.append(c3)
    contacts.append(c4)
    contacts.append(c5)
    contacts.append(c6)
    contacts.append(c7)
    contacts.append(c8)
    

    while '' in contacts:
        contacts.remove('')


def launch_chrome():
    global driver
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--user-data-dir=C:\\Users\\Samuel Soo\\AppData\\Local\\Google\\Chrome\\User Data\\Default')
        options.add_argument('--profile-directory=Default')

        driver = webdriver.Chrome(executable_path='driver/chromedriver', options=options)
        driver.get('https://web.whatsapp.com')
    except selenium.common.exceptions.WebDriverException as e:
        pygame_gui.windows.ui_message_window.UIMessageWindow(rect=(400,400,200,200),
                                                            manager=manager,
                                                            window_title='ERROR',
                                                            html_text='The Following Error Occured: ' + str(e))


def scan_menu():
    global frames
    global MiniU_font
    global driver

    #kill all widgets in main menu
    contact1.kill()
    contact2.kill()
    contact3.kill()
    contact4.kill()
    contact5.kill()
    contact6.kill()
    contact7.kill()
    contact8.kill()
    message_box.kill()
    timeout_in_secs.kill()
    number_of_msgs.kill()
    message_preview_button.kill()
    random_message_button.kill()
    attack_button.kill()
    reset_button.kill()
    info_button.kill()
    settings_button.kill()

    try:
        info_window.kill()
        settings_window.kill()
    except:
        pass


    #widgets
    back_button = pygame_gui.elements.ui_button.UIButton(relative_rect=pygame.Rect(20,710,150,70),
                                            manager=manager,
                                            text='<-- GO BACK')

    forward_button = pygame_gui.elements.ui_button.UIButton(relative_rect=pygame.Rect(830,710,150,70),
                                                        manager=manager,
                                                        text='FORWARD -->')

    chrome_button = pygame_gui.elements.ui_button.UIButton(relative_rect=pygame.Rect(420,710,150,70),
                                                        manager=manager,
                                                        text='LAUNCH CHROME')



    

    #main loop
    scan_running = True
    go_to_attack_menu = False



    while scan_running:
        time_delta = clock.tick(60)/1000

        scan_screen.fill(DARK_BLUE)
        pygame.draw.rect(scan_screen, LIGHT_GREY, (195, 95, 610, 560))
        pygame.draw.rect(scan_screen, GREY, (200,100,600,550))
        pygame.draw.rect(scan_screen, LIGHT_GREY, (230, 255, 543, 357))
        scan_screen.blit(guide_Img, (235,260))

        guide_text = MiniU_font.render('For The Bot To Work, You Need To Scan The QR', True, (250,250,250))
        guide_text2 = MiniU_font.render('Code On The Chrome Window That Will Pop', True, (250,250,250))
        guide_text3 = MiniU_font.render('Up. Press The Centre Button Below To Start.', True, (250,250,250))

        scan_screen.blit(guide_text,(210,110))
        scan_screen.blit(guide_text2,(210,145))
        scan_screen.blit(guide_text3,(210,180))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                scan_running = False
                sys.exit()
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == back_button:
                    scan_running = False
                    go_to_attack_menu = False

                if event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == forward_button:
                    scan_running = False
                    go_to_attack_menu = True
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == chrome_button:
                    launch_chrome()


            manager.process_events(event)
            #print(event)


        manager.update(time_delta)
        manager.draw_ui(scan_screen)

        frames += 1
        screen.blit(scan_screen, (0,0))
        pygame.display.update()

    if go_to_attack_menu == False:
        back_button.kill()
        forward_button.kill()
        chrome_button.kill()
        make_main_menu_widgets()
    elif go_to_attack_menu == True:
        back_button.kill()
        forward_button.kill()
        chrome_button.kill()
        attack_menu()



def attack_menu():
    global driver
    global frames
    global msg
    global TIMEOUT
    global count
    global U_font
    global MiniU_font
    global contacts

    return_button = pygame_gui.elements.ui_button.UIButton(relative_rect=pygame.Rect((10,720), (200,70)),
                                                            manager=manager,
                                                            text='RETURN TO MAIN MENU')

    again_button = pygame_gui.elements.ui_button.UIButton(relative_rect=pygame.Rect((790,720), (200,70)),
                                                            manager=manager,
                                                            text='!! REPEAT ATTACK !!')

    stop_button = pygame_gui.elements.ui_button.UIButton(relative_rect=pygame.Rect(430,720,150,70),
                                                        manager=manager,
                                                        text='[STOP ATTACK]')


    successful_msgs = 0
    failed_msgs = 0
    msg_number_for_current_contact = 0
    texts_per_second = 0
    current_time_elapsed = 0.00
    count = int(count)

    filter_all()


    elements_found = False
    start_time = time.time()
    attack_menu_running = True
    state = 'running'

    #main loop
    while attack_menu_running:
        time_delta = clock.tick(60)/1000
        attack_screen.fill(DARK_BLUE)

        pygame.draw.rect(attack_screen, LIGHT_GREY, (345,15,370,70))
        pygame.draw.rect(attack_screen, GREY, (350,20,360,60))
        state_text = U_font.render('State: ', True, (250,250,250))
        attack_screen.blit(state_text, (380,30))

        if state == 'running':
            state_text2 = U_font.render('Running', True, (250,0,0))
            attack_screen.blit(state_text2, (500,30))
        elif state == 'finished':
            state_text2 = U_font.render('Finished', True, (0,250,0))
            attack_screen.blit(state_text2, (500,30))            

        pygame.draw.rect(attack_screen, LIGHT_GREY, (95,135,860,510))
        pygame.draw.rect(attack_screen, GREY, (100,140,850,500))
        stat_text = U_font.render('Stats', True, (250,250,250))
        attack_screen.blit(stat_text, (470,145))
        success_msg_text = MiniU_font.render('Successful Texts: {}'.format(str(successful_msgs)), True, (250,250,250))
        attack_screen.blit(success_msg_text, (125, 230))
        failed_msgs_text = MiniU_font.render('Failed Texts: {}'.format(str(failed_msgs)), True, (250,250,250))
        attack_screen.blit(failed_msgs_text, (650, 230))
        rate_text = MiniU_font.render('Rate Of Sending Texts: {}/s'.format(str(texts_per_second)), True, (250,250,250))
        attack_screen.blit(rate_text, (125, 310))
        times_text = MiniU_font.render('Time Elapsed: {}s'.format(str(current_time_elapsed)), True, (250,250,250))
        attack_screen.blit(times_text, (650,310))

        
        if contacts != []:
            current_contact_to_send = str(contacts[0])
            end_time = time.time()
            current_time_elapsed = round(end_time-start_time, 2)
            if current_time_elapsed != 0 or current_time_elapsed != -0:
                texts_per_second = int((successful_msgs+failed_msgs)/current_time_elapsed)
            if TIMEOUT != '-':
                if current_time_elapsed > float(TIMEOUT):
                    contacts = []

        if contacts == []:
            state = 'finished'
            current_contact_to_send = 'NONE'

        
        if elements_found == False and state == 'running':
            try:
                search_box = driver.find_element_by_xpath('//*[@id="side"]/div[1]/div/label/div/div[2]')
                search_box.clear()
                search_box.send_keys(current_contact_to_send)
                search_box.send_keys(Keys.ENTER)
                message_box = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
                elements_found = True
            except:
                failed_msgs += count
                #go to next contact
                contacts.pop(0)
                elements_found = False


        if elements_found == True and state == 'running':
            if msg_number_for_current_contact != count:
                try:
                    message_box.send_keys(msg)
                    message_box.send_keys(Keys.ENTER)
                    successful_msgs += 1
                except:
                    failed_msgs += 1
                msg_number_for_current_contact += 1

            elif msg_number_for_current_contact == count:
                #go to next contact
                contacts.pop(0)
                msg_number_for_current_contact = 0
                elements_found = False 
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                attack_menu_running = False
                sys.exit()
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == return_button:
                    attack_menu_running = False
                    again_button.kill()
                    return_button.kill()
                    stop_button.kill()
                    make_main_menu_widgets()
                elif event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == again_button:

                    state='running'
                    successful_msgs = 0
                    failed_msgs = 0
                    msg_number_for_current_contact = 0
                    texts_per_second = 0
                    current_time_elapsed = 0.00
                    count = int(count)
                    elements_found = False
                    start_time = time.time()

                    filter_all()

                elif event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == stop_button:
                    contacts = []


            manager.process_events(event)
            #print(event)


        manager.update(time_delta)
        manager.draw_ui(attack_screen)

        frames += 1
        screen.blit(attack_screen, (0,0))
        pygame.display.update()

def make_main_menu_widgets():
    global contact1
    global contact2
    global contact3
    global contact4
    global contact5
    global contact6
    global contact7
    global contact8
    global message_box
    global number_of_msgs
    global timeout_in_secs
    global message_preview_button
    global attack_button
    global reset_button
    global random_message_button
    global c1
    global c2
    global c3
    global c4
    global c5
    global c6
    global c7
    global c8
    global msg
    global TIMEOUT
    global count
    global info_button
    global settings_button
    

    #contacts input
    contact1 = pygame_gui.elements.ui_text_entry_line.UITextEntryLine(relative_rect=pygame.Rect((170,215), (200,250)),manager=manager)
    contact2 = pygame_gui.elements.ui_text_entry_line.UITextEntryLine(relative_rect=pygame.Rect((740,215), (200,250)),manager=manager)
    contact3 = pygame_gui.elements.ui_text_entry_line.UITextEntryLine(relative_rect=pygame.Rect((170,305), (200,250)),manager=manager)
    contact4 = pygame_gui.elements.ui_text_entry_line.UITextEntryLine(relative_rect=pygame.Rect((740,305), (200,250)),manager=manager)
    contact5 = pygame_gui.elements.ui_text_entry_line.UITextEntryLine(relative_rect=pygame.Rect((170,395), (200,250)),manager=manager)
    contact6 = pygame_gui.elements.ui_text_entry_line.UITextEntryLine(relative_rect=pygame.Rect((740,395), (200,250)),manager=manager)
    contact7 = pygame_gui.elements.ui_text_entry_line.UITextEntryLine(relative_rect=pygame.Rect((170,485), (200,250)),manager=manager)
    contact8 = pygame_gui.elements.ui_text_entry_line.UITextEntryLine(relative_rect=pygame.Rect((740,485), (200,250)),manager=manager)

    #message input
    message_box = pygame_gui.elements.ui_text_entry_line.UITextEntryLine(relative_rect=pygame.Rect((40,600), (400,600)),manager=manager)
    message_box.set_text('Your Message')
    message_box.set_allowed_characters(list('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ '))

    #no. of msgs
    number_of_msgs = pygame_gui.elements.ui_text_entry_line.UITextEntryLine(relative_rect=pygame.Rect((500,600), (260,600)),manager=manager)
    number_of_msgs.set_text('10')
    number_of_msgs.set_allowed_characters(numbers)

    #timeout input
    timeout_in_secs = pygame_gui.elements.ui_text_entry_line.UITextEntryLine(relative_rect=pygame.Rect((500,710), (260,600)),manager=manager)
    timeout_in_secs.set_text('-')
    timeout_in_secs.set_allowed_characters(numbers2)    

    #buttons
    attack_button = pygame_gui.elements.ui_button.UIButton(relative_rect=pygame.Rect(790,675,200,120),
                                                        manager=manager,
                                                        text='!! LAUNCH ATTACK !!')

    reset_button = pygame_gui.elements.ui_button.UIButton(relative_rect=pygame.Rect(790,545,200,120),
                                                            manager=manager,
                                                            text='RESET TO DEFAULTS')

    message_preview_button = pygame_gui.elements.ui_button.UIButton(relative_rect=pygame.Rect(40,650,180,90),
                                                                    manager=manager,
                                                                    text='Preview Message')

    random_message_button = pygame_gui.elements.ui_button.UIButton(relative_rect=pygame.Rect(260,650,180,90),
                                                                    manager=manager,
                                                                    text='Randomly Generate')

    info_button = pygame_gui.elements.ui_button.UIButton(relative_rect=pygame.Rect(900,50,70,50),
                                                                    manager=manager,
                                                                    text='Info')

    settings_button = pygame_gui.elements.ui_button.UIButton(relative_rect=pygame.Rect(30,50,80,50),
                                                                manager=manager,
                                                                text='Settings')


    try:
        contact1.set_text(c1)
        contact2.set_text(c2)
        contact3.set_text(c3)
        contact4.set_text(c4)
        contact5.set_text(c5)
        contact6.set_text(c6)
        contact7.set_text(c7)
        contact8.set_text(c8)
        message_box.set_text(msg)
        timeout_in_secs.set_text(TIMEOUT)
        number_of_msgs.set_text(count)
    except:
        pass

#---------------------------------------------------------------
#---------------------------------------------------------------
#main loop
#---------------------------------------------------------------
#---------------------------------------------------------------



manager.preload_fonts([{'name': 'fira_code', 'point_size': 18, 'style': 'bold'},
                    {'name': 'fira_code', 'point_size': 18, 'style': 'regular'}])
make_main_menu_widgets()

running = True
while running:
    #make it run at 60 fps constant
    time_delta = clock.tick(60)/1000

    #blit theme
    screen.fill(DARK_BLUE)
    banner()
    outlines()
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()



        if event.type == pygame.USEREVENT:
            if event.user_type == pygame.KEYDOWN and event.key == pygame.K_F1:
                contact1.hide()


            if event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == message_preview_button:
                    preview_window = pygame_gui.windows.ui_message_window.UIMessageWindow(rect=pygame.Rect((300,300),(300,300)),
                                                                                            manager=manager,
                                                                                            window_title='Message Preview',
                                                                                            html_message=message_box.get_text())

            if event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == random_message_button:
                generate_random_message()

            if event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == reset_button:
                message_box.set_text('Your Message')
                number_of_msgs.set_text('10')
                timeout_in_secs.set_text('-')
                
                for i in range(8):
                    locals()['contact' + str(i+1)].set_text('')

            if event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == attack_button:
                c1 = contact1.get_text()
                c2 = contact2.get_text()
                c3 = contact3.get_text()
                c4 = contact4.get_text()
                c5 = contact5.get_text()
                c6 = contact6.get_text()
                c7 = contact7.get_text()
                c8 = contact8.get_text()
                msg = message_box.get_text()
                TIMEOUT = timeout_in_secs.get_text()
                count = number_of_msgs.get_text()

                if c1 != '' or c2 != '' or c3 != '' or c4 != '' or c5 != '' or c6 != '' or c7 != '' or c8 != '':
                    scan_menu()
                else:
                    pygame_gui.windows.ui_message_window.UIMessageWindow(rect=pygame.Rect((400,400), (300,200)),
                                                                        manager=manager,
                                                                        window_title='Error',
                                                                        html_message='ERROR: Need To Select One Contact Name To Proceed!')

            if event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == info_button:
                info_window = pygame_gui.elements.ui_window.UIWindow(rect=pygame.Rect((300,100),(400,600)),
                                                                    manager=manager,
                                                                    window_display_title='More Info')

                info_text_box = pygame_gui.elements.ui_text_box.UITextBox(relative_rect=pygame.Rect(10,10,350,500),
                                                                manager=manager,
                                                                container=info_window,
                                                                html_text='<font size="5">'
                                                                            '<b><u>Description</b></u>'
                                                                            '<br>'
                                                                            'This is a spam bot for the messaging app \'<a href="https://whatsapp.com">Whatsapp</a>\' '
                                                                            'and is made for dickheads who like '
                                                                            'to annoy the fuck out of their friends.'
                                                                            '<br> <br>'
                                                                            '<b><u>Guide</b></u><br>'
                                                                            'The Full Documentation Of This Tool Can Be Found <a href="https://pastebin.com/SV2UdUAh">Here</a>.'
                                                                            '<br> <br>'
                                                                            '<b><u>EXTRAS</b></u><br>'
                                                                            'I\'ve found a way to make yourself an admin in any Whatsapp Group Chat. I\'ve made it into '
                                                                            'a GUI (like the one you\'re reading this in) so the noobs can understand how to use it. '
                                                                            'You can get my auto-admin tool <a href="https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstleyVEVO">Here</a>.'
                                                                            '<br> <br>'
                                                                            '<b><u>Credits</b></u><br>'
                                                                            'Made By t0a5ted, 2020.')
            if event.user_type == pygame_gui.UI_TEXT_BOX_LINK_CLICKED:      
                link = str(event.link_target)
                if link == 'https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstleyVEVO':
                    for i in range(7):
                        system('start chrome.exe "' + link + '"')
                else:
                    system('start chrome.exe ' + link)

            if event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == settings_button:
                settings_window = pygame_gui.elements.ui_window.UIWindow(rect=pygame.Rect(200,300,300,400),
                                                                        manager=manager,
                                                                        window_display_title='Settings')

                info_text_box = pygame_gui.elements.ui_text_box.UITextBox(relative_rect=pygame.Rect(10,10,250,300),
                                                                manager=manager,
                                                                container=settings_window,
                                                                html_text='<font size="5">'
                                                                            'Nothing Here Yet...'
                                                                            '<br> <br> <br>Made By t0a5ted<br>v1.0.0')


        manager.process_events(event)
        #print(event)


    manager.update(time_delta)
    manager.draw_ui(screen)


    frames += 1

    pygame.display.update()