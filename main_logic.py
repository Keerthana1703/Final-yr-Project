import pygame
import random
import time 
import pandas as pd
import csv_bs
global phase,Score,incorrect,correct,rank,BLUE,BLACK,email_address
import json
import webbrowser
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
email_address=''
pygame.init()
start_time = time.time()
incorrect=0
Score=[0,0,0]
correct=int(sum(Score))
youtube_links = []
rank=0.0
BLUE= (173, 216, 230)
BLACK=(0,0,0)
def new_line(s):
    if len(s)<75:
        return s," "
    ind=s.find(" ",75)
    return s[:ind],s[ind:]

def drawing(i,j):
    if not board[i]:
        screen.blit(box,j)
    elif board[i]=="X":
        pygame.draw.line(box, (0,0,0), (36,36),(108,107), width=5)
        pygame.draw.line(box, (0,0,0), (36,107),(108,36), width=5)
        screen.blit(box,j)
    else:
        pygame.draw.circle(box,(0,0,0),(72,72),36,width=5)
        screen.blit(box,j)

def player_wins(board):
    player="X"
    computer_mark="O"
    # check if the player has won horizontally
    if board[0] == board[1] == board[2] == player:
        return "player"
    elif board[3] == board[4] == board[5] == player:
        return "player"
    elif board[6] == board[7] == board[8] == player:
        return "player"
    # check if the player has won vertically
    elif board[0] == board[3] == board[6] == player:
        return "player"
    elif board[1] == board[4] == board[7] == player:
        return "player"
    elif board[2] == board[5] == board[8] == player:
        return "player"
    # check if the player has won diagonally
    elif board[0] == board[4] == board[8] == player:
        return "player"
    elif board[2] == board[4] == board[6] == player:
        return "player"
    # check if the computer has won horizontally
    elif board[0] == board[1] == board[2] == computer_mark:
        return "comp"
    elif board[3] == board[4] == board[5] == computer_mark:
        return "comp"
    elif board[6] == board[7] == board[8] == computer_mark:
        return "comp"
    # check if the computer has won vertically
    elif board[0] == board[3] == board[6] == computer_mark:
        return "comp"
    elif board[1] == board[4] == board[7] == computer_mark:
        return "comp"
    elif board[2] == board[5] == board[8] == computer_mark:
        return "comp"
    # check if the computer has won diagonally
    elif board[0] == board[4] == board[8] == computer_mark:
        return "comp"
    elif board[2] == board[4] == board[6] == computer_mark:
        return "comp"
    else:
        return False

def predict():
    copy=board[:]
    for i in range(len(copy)):
        copy=board[:]
        if copy[i]==None:
            copy[i]='X'
            if player_wins(copy):
                return i+1

# Define the function to calculate scores
def score_cal(time, correct):
    return 100 - int(time) + (int(correct) * 10)

# Read in the scores from scores.csv
scores_df = pd.read_csv('scores.csv')

# Calculate the scores for each row
scores_df['scores'] = scores_df.apply(lambda row: score_cal(row['time'], row['correct']), axis=1)

# Group by username and sum the scores
leaderboard_df = scores_df.groupby('username')['scores'].sum().reset_index()

# Sort by score in descending order
leaderboard_df = leaderboard_df.sort_values(by='scores', ascending=False)

# Add a rank column
leaderboard_df['rank'] = leaderboard_df['scores'].rank(method='dense', ascending=False)

# Write the leaderboard to a new CSV file
leaderboard_df.to_csv('leaderboard.csv', index=False)


#print((csv_bs.best_score("scores.csv",score_cal)))
def save_credentials(username):
    # Create a DataFrame to store the credentials
    df = pd.DataFrame({'rank':[rank],'username': [username], 'scores': [0]})
    
    # Load the existing leaderboard file, or create a new one if it doesn't exist
    try:
        leaderboard = pd.read_csv('leaderboard.csv', index_col=0)
    except FileNotFoundError:
        leaderboard = pd.DataFrame(columns=['rank','username', 'scores'])
    
    ## Check if the username already exists in the leaderboard

    print('Leaderboard file created!')
# Define three sets of questions with varying difficulty levels
def questions():

    global easy_questions,medium_questions,hard_questions
    with open('questions.json') as f:
        questions = json.load(f)

    easy_questions = questions['easy_questions']
    medium_questions = questions['medium_questions']
    hard_questions = questions['hard_questions']
    #READS THE JSON FILE --questions.csv
def send_email(email_address,youtube_links):
    # create message
    message = MIMEMultipart()
    message['Subject'] = 'Video explanations for incorrect answers'
    message['From'] = "finalprojectdummy@zohomail.in"
    message['To'] = email_address

    # create text part
    text = "Click the links below to watch video explanations:\n"
    for link in youtube_links:
        text += link + "\n"
    part1 = MIMEText(text, 'plain')

    # attach parts to message
    message.attach(part1)

    # create SMTP session
    try:
        server = smtplib.SMTP_SSL('smtp.zoho.in', 465)
        server.ehlo()
        server.login("finalprojectdummy@zohomail.in", "tictactoeproject")
        server.sendmail("finalprojectdummy@zohomail.in", email_address, message.as_string())
        server.close()
        print('Email sent successfully')
    except Exception as e:
        print('Something went wrong while sending email:', e) 
def input_box(prompt=""):
    input_str = ""
    while True:
     screen.fill((108, 207, 246)) 
     for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return input_str

            elif event.key == pygame.K_BACKSPACE:
                input_str = input_str[:-1]

            else:
                input_str += event.unicode
     small_font=pygame.font.SysFont('arial',12)
     pygame.draw.rect(screen, BLACK, input_box_rect, 2)
     input_text = small_font.render(email_address, True, BLACK)
     input_box_rect.w = 250
     input_rect = input_text.get_rect(center=input_box_rect.center)
     screen.blit(input_text, input_rect)     #clear the screen
      
    # draw input box
     pygame.draw.rect(screen, (0, 0, 0), input_rect, 2)
     pygame.draw.rect(screen, (255, 255, 255), input_rect)

    # render input text

     txt=vsmall_font.render(input_str, True, (0, 0, 0))
     txt_rect=txt.get_rect(center=(200,320))
     screen.blit(txt,txt_rect) 

    # render 'Press enter to submit' text
     prompt_txt = small_font.render('Press enter to submit', True, (0, 0, 0))
     prompt_rect = prompt_txt.get_rect(center=(216, 500))
     screen.blit(prompt_txt, prompt_rect)
    # screen.fill((108, 207, 246))
     pygame.display.update()
     #screen.fill((108, 207, 246)) 
def display_leaderboard():
     try:
        scores = pd.read_csv('scores.csv')
        scores['Score'] = scores.apply(lambda row: score_cal(row['time'], row['correct']), axis=1)
        leaderboard = scores.groupby('username')['Score'].sum().reset_index()
        leaderboard = leaderboard.sort_values(by='Score', ascending=False)
        leaderboard['rank'] = range(1, len(leaderboard) + 1) 
        screen.fill((108, 207, 246))
        txt = font.render('Leaderboard', True, (0, 0, 0))
        txt_rect = txt.get_rect(center=(216, 50))
        screen.blit(txt, txt_rect)
        x, y = 30, 100
        count = 0
        for i, row in leaderboard.iterrows():
            rank =row['rank']
            name = row['username']
            score = row['Score']
            txt =font.render(f'{rank}-{name} - {score}', True, (0, 0, 0))
            txt_rect = txt.get_rect(center=(216, 80 + (count * 25)))
            screen.blit(txt, txt_rect)
            count += 1
        pygame.display.update()

        # Handle events
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    
                    if event.key == pygame.K_RETURN:
                        display_leaderboard()
                    elif event.key == pygame.K_SPACE and phase=="question":
                         
                         questions()                     
     except Exception as e:
         print(e)
         pass
questions()
pygame.init()
pygame.font.init()
screen=pygame.display.set_mode((432,604))
screen.fill((108, 207, 246))

font=pygame.font.SysFont('arial',25) 
small_font=pygame.font.SysFont('arial',15)
large_font=pygame.font.SysFont('arial',45)
vsmall_font=pygame.font.SysFont('arial',20)

board=[None]*9
empty=[i for i in range(9)]
clock=pygame.time.Clock()
box=pygame.Surface((144,142))

#setup for login page
username,password='',''
active=-1
login_rects=[pygame.Rect((108,284),(288,21)),pygame.Rect((108,355),(288,21))]
looks=[pygame.Rect((106,282),(291,24)),pygame.Rect((107,353),(290,24))]
print(login_rects[0].right)
login_box=pygame.Surface((288,21))
login=True
on_top=False
txt=small_font.render("click here!!",True,(0,0,0))
the_rect=txt.get_rect(center=(288,426))
entered=False
login_try=""

get_question=True
option_box=pygame.Surface((432,107))
difficulty=1
phase="login"
wait=False,False
#creating rectangles for the game
box_rects=[]
for i in range(0,426,142):
    box_rects.append(box.get_rect(topleft=(i,107)))
for i in range(0,426,142):
    box_rects.append(box.get_rect(topleft=(i,249)))
for i in range(0,426,142):
    box_rects.append(box.get_rect(topleft=(i,391)))

option_box_rects=[]
for i in range(4):
    option_box_rects.append(option_box.get_rect(topleft=(0,108+i*107)))
while True:
    
    screen.fill((108, 207, 246))
    for i in pygame.event.get():
        if i.type==256:
            pygame.quit()
        if i.type==pygame.KEYDOWN:
            if i.key==pygame.K_SPACE and phase=="end_game":
                Score=[0,0,0]
                difficulty=1
                board=[None]*9
                phase="question"
                wait=False,False
                get_question=True
                incorrect=0
                empty=[i for i in range(9)]
                questions()
            if phase=='login':
                if active==0:
                    if i.key==pygame.K_BACKSPACE:
                        username=username[:-1]
                    else:
                        username+=i.unicode
                if active==1:
                    if i.key==pygame.K_BACKSPACE:
                        password=password[:-1]
                    else:
                        if not i.unicode==r'\r':
                            password+=i.unicode
                if i.key==pygame.K_RETURN and phase=='login':
                    if active==0:
                        username=username[:-1]
                    else:
                        password=password[:-1]
                    entered=True
                    save_credentials(username)
    res=player_wins(board)
    #print(phase,res)
    mouse_buttons=pygame.mouse.get_pressed()
    mouse=pygame.mouse.get_pos()
    if res=="player":
        for i,j in enumerate(box_rects):
            box.fill((52, 84, 209))
            drawing(i,j)
        txt=font.render("You Win!!",True,(0,0,0))
        txt_rect=txt.get_rect(center=(216,53))
        screen.blit(txt,txt_rect)
        pygame.display.update()
        time.sleep(2)
        res2=res
        res=''
        board=[None]*9
        timeee=time.time()-start_time
        start_time=time.time()
        csv_bs.add_score(username,int(timeee),sum(Score),"scores.csv")
       

        
        phase="end_game"
        continue
        phase="end_game"
        continue

    elif res=="comp":
        for i,j in enumerate(box_rects):
            box.fill((52, 84, 209))
            drawing(i,j)
        txt=font.render("Computer Wins!!",True,(0,0,0))
        txt_rect=txt.get_rect(center=(216,53))
        screen.blit(txt,txt_rect)
        pygame.display.update()
        time.sleep(2)
        res2=res
        res=''
        board=[None]*9
        timeee=time.time()-start_time
        start_time=time.time()
        csv_bs.add_score(username,int(timeee),sum(Score),"scores.csv")
        phase="end_game"
        continue
    # To check for tie
    if not empty:
        for i,j in enumerate(box_rects):
            box.fill((52, 84, 209))
            drawing(i,j)
        txt=font.render("Tie!!",True,(0,0,0))
        txt_rect=txt.get_rect(center=(216,53))
        screen.blit(txt,txt_rect)
        pygame.display.update()
        time.sleep(3)
        exit()
    if phase=="player":
        move=predict()
        if move:
            txt=font.render(f"hint: You can win by marking position {move} ",True,(0,0,0))
        else:
            txt=font.render(f"hint: No hint available at the moment",True,(0,0,0))
        txt_rect=txt.get_rect(topleft=(21,553))
        screen.blit(txt,txt_rect)
        txt=font.render("Your turn!!",True,(0,0,0))
        txt_rect=txt.get_rect(center=(216,53))
        screen.blit(txt,txt_rect)
        
        #print(mouse_buttons)
        if wait[1] and wait[0]:
            screen.fill((108, 207, 246))
            for i,j in enumerate(box_rects):
                box.fill((52, 84, 209))
                drawing(i,j)
            txt=font.render("Question Time!!",True,(0,0,0))
            txt_rect=txt.get_rect(center=(216,53))
            screen.blit(txt,txt_rect)
            pygame.display.update()
            time.sleep(1)
            wait=False,False
            phase="question"
            continue
        elif not wait[1] and wait[0]:
            screen.fill((108, 207, 246))
            for i,j in enumerate(box_rects):
                box.fill((52, 84, 209))
                drawing(i,j)
            txt=font.render("Invalid!!",True,(0,0,0))
            txt_rect=txt.get_rect(center=(216,53))
            screen.blit(txt,txt_rect)
            pygame.display.update()
            time.sleep(1)
            wait=False,False

        mouse=pygame.mouse.get_pos()
        for i,j in enumerate(box_rects):
            box.fill((52, 84, 209))
            print(i,j)
            drawing(i,j)
            if j.collidepoint(mouse):
                #print(i+1)
                box.fill((52, 84, 230))
                drawing(i,j)
                if mouse_buttons[0]:
                    if not board[i]:
                        board[i]='X'
                        empty.remove(i)
                        wait=True,True
                    else:
                        wait=True,False

    elif phase=="comp":
        if empty:
            choice=random.choice(empty)
            board[choice]="O"
            empty.remove(choice)
        phase="question"
        #print(choice)
        screen.fill((108, 207, 246))
        for i,j in enumerate(box_rects):
            box.fill((52, 84, 209))
            drawing(i,j)
        txt=font.render("Computers turn!!",True,(0,0,0))
        txt_rect=txt.get_rect(center=(216,53))
        screen.blit(txt,txt_rect)
        pygame.display.update()
        time.sleep(1)
    elif phase=="question":
        #print(len(easy_questions))
        if difficulty==1 and get_question:
            question=easy_questions.pop()
            get_question=False
        elif difficulty==2 and get_question:
            question=medium_questions.pop()
            get_question=False
        elif difficulty==3 and get_question:
            question=hard_questions.pop()
            get_question=False
        #print(question)
        #print("in")
        screen.fill((108, 207, 246))
        #print(len(option_box_rects))
        mouse=pygame.mouse.get_pos()
        
        for i,j in enumerate(option_box_rects):
            if j.collidepoint(mouse):
                option_box.fill((52, 84, 230))
            else:
                option_box.fill((52, 84, 209))
            txt=small_font.render(question["options"][i],True,(0,0,0))
            #print(question["options"][i])
            txt_rect=txt.get_rect(midtop=(216,36))
            option_box.blit(txt,txt_rect)
            screen.blit(option_box,j)
            #print(new_line(question["question"]))
            txt=small_font.render(new_line(question["question"])[0],True,(0,0,0))
            txt_rect=txt.get_rect(center=(216,36))
            screen.blit(txt,txt_rect)
            txt=small_font.render(new_line(question["question"])[1],True,(0,0,0))
            txt_rect=txt.get_rect(center=(216,57))
            screen.blit(txt,txt_rect)
            #pygame.display.update()
            
    
        pygame.display.update()
        #time.sleep(2)
        #print(mouse)
        ans=-1
        if mouse_buttons[0]==True:
            for i,j in enumerate(option_box_rects):
                if j.collidepoint(mouse):
                    ans=i
            if ans!=-1:
                phase="result"
                get_question=True
                time.sleep(1)
    elif phase=="result":
     screen.fill((108, 207, 246))
     if question['options'][ans]==question['answer']:
        txt=small_font.render('Correct Answer!!',True,(0,0,0))
        txt_rect=txt.get_rect(center=(216,213))
        screen.blit(txt,txt_rect)
        if difficulty<3:
            difficulty+=1
        Score[difficulty-1]+=1
        phase="player"
     else:
        #question['options'][ans] != question["answer"]:
        youtube_links.append(question["youtube_link"])
        txt=small_font.render('Wrong Answer!!',True,(0,0,0))
        txt_rect=txt.get_rect(center=(216,213))
        screen.blit(txt,txt_rect)
        if difficulty == 1:
            youtube_link = easy_questions[-1]['youtube_link']
        elif difficulty == 2:
            youtube_link = medium_questions[-1]['youtube_link']
        elif difficulty == 3:
            youtube_link = hard_questions[-1]['youtube_link']
        txt=small_font.render(f'Try this video to  more: {youtube_link}',True,(0,0,0))
        txt_rect=txt.get_rect(center=(216,248))
        screen.blit(txt,txt_rect)
        phase="comp"
        incorrect+=1
     pygame.display.update()
     time.sleep(2)

    elif phase=="end_game":
     # youtube_links = []
      #global phase, score, incorrect
      phase="end_game"
      pygame.time.set_timer(pygame.USEREVENT+1,0)
      pygame.time.set_timer(pygame.USEREVENT+2,0)
      screen.fill((108, 207, 246)) 
      if res2=='player':
          BACKGROUND_COLOR = (108, 207, 246)
          FONT_NAME = 'C:\\Users\\keert\\OneDrive\\Desktop\\keer\\assets\\fonts\\OpenSans-SemiBold.ttf'

# Initialize pygame and create the screen
          pygame.init()
          screen = pygame.display.set_mode((432, 600))
          pygame.display.set_caption("Quiz Results")
          clock = pygame.time.Clock()
# Define text colors and sizes
          BLACK = (0, 0, 0)
          SMALL_SIZE = 12
          MEDIUM_SIZE = 16
          LARGE_SIZE = 45
# Load fonts
          font = pygame.font.Font(FONT_NAME, MEDIUM_SIZE)
          small_font = pygame.font.Font(FONT_NAME, SMALL_SIZE)
    # Clear the screen and fill with the background color
          screen.fill(BACKGROUND_COLOR)

    # Render and display the quiz results
          txt = small_font.render(f'Number of questions answered correctly: {sum(Score)}', True, BLACK)
          txt_rect = txt.get_rect(center=(216, 83))
          screen.blit(txt, txt_rect)
          txt = small_font.render(f'Number of questions answered incorrectly: {incorrect}', True, BLACK)
          txt_rect = txt.get_rect(center=(216, 118))
          screen.blit(txt, txt_rect)

    # Render and display the "Try Again" and "See History" buttons
          txt = font.render('Press SPACE to Try Again', True, BLACK)
          txt_rect = txt.get_rect(center=(216, 154))
          screen.blit(txt, txt_rect)
          txt = font.render('Press ENTER to See History', True, BLACK)
          txt_rect = txt.get_rect(center=(216, 220))
          screen.blit(txt, txt_rect)

    # Render and display the video explanation links
          if incorrect > 0:
            txt = font.render("Click the links below to watch video explanations:", True, BLACK)
            txt_rect = txt.get_rect(center=(216, 300))
            screen.blit(txt, txt_rect)
            y = 320
            for link in youtube_links:
               txt = small_font.render(link, True,(255, 0, 0))
               txt_rect = txt.get_rect(center=(216, y))
               screen.blit(txt, txt_rect)
               y += 30
          pygame.display.update()
    # Render and display the "Send to Email" prompt and button
          prompt_text = small_font.render("Click the button below to send video explanations to your email address:", True, BLACK)
          prompt_rect = prompt_text.get_rect(center=(216, 480))
          screen.blit(prompt_text, prompt_rect)
          input_box_rect = pygame.Rect(100, 300, 232, 50)
          send_rect = pygame.Rect(116, 530, 200, 50)
          pygame.draw.rect(screen, BLUE, send_rect)
          txt = small_font.render("Send Links to Email", True, BLACK)
          txt_rect = txt.get_rect(center=send_rect.center)
          screen.blit(txt, txt_rect)

    # Update the display and set the FPS
          pygame.display.update()
  
          while True:
           
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
            # Quit the game if the user closes the window
                        pygame.quit()
                        sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        display_leaderboard()
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # check if a link was clicked
                    pos = pygame.mouse.get_pos()
                    y = 320
                    for link in youtube_links:
                        txt = small_font.render(link, True, (0, 0, 255))
                        txt_rect = txt.get_rect(center=(216, y))
                        if txt_rect.collidepoint(pos):
                            webbrowser.open(link)
                            break
                        y += 20
                    if send_rect.collidepoint(event.pos):
                         email_address = input_box(prompt="Enter your email address:")
                         send_email(email_address,youtube_links)
                     #screen.fill((108, 207, 246))      
            
            
            pygame.display.update()
      #pygame.display.update()
            screen.fill((108, 207, 246))
      elif res2=="comp":
          
          BACKGROUND_COLOR = (108, 207, 246)
          FONT_NAME = 'C:\\Users\\keert\\OneDrive\\Desktop\\keer\\assets\\fonts\\OpenSans-SemiBold.ttf'
# Initialize pygame and create the screen
          pygame.init()
          screen = pygame.display.set_mode((432, 600))
          pygame.display.set_caption("Quiz Results")
          clock = pygame.time.Clock()
# Define text colors and sizes
          BLACK = (0, 0, 0)
          SMALL_SIZE = 12
          MEDIUM_SIZE = 16
          LARGE_SIZE = 45
# Load fonts
          font = pygame.font.Font(FONT_NAME, MEDIUM_SIZE)
          small_font = pygame.font.Font(FONT_NAME, SMALL_SIZE)
    # Clear the screen and fill with the background color
          screen.fill(BACKGROUND_COLOR)
          screen.blit(txt,txt_rect)
          txt = small_font.render(f'Number of questions answered correctly: {sum(Score)}', True, BLACK)
          txt_rect = txt.get_rect(center=(216, 83))
          screen.blit(txt, txt_rect)
          txt = small_font.render(f'Number of questions answered incorrectly: {incorrect}', True, BLACK)
          txt_rect = txt.get_rect(center=(216, 118))
          screen.blit(txt, txt_rect)
          #txt=font.render('Computer Wins!!',True,BLACK)
          #txt_rect=txt.get_rect(center=(216,75))
          screen.blit(txt,txt_rect)
          txt=font.render('Press SPACE to Try Again',True,BLACK)
          txt_rect=txt.get_rect(center=(216,154))
          screen.blit(txt,txt_rect)
          txt=font.render('Press ENTER to See History',True,BLACK)
          txt_rect=txt.get_rect(center=(216,220))
          screen.blit(txt,txt_rect)
         # pygame.display.update()
          # display YouTube links for incorrect answers
          if incorrect > 0:
             txt = font.render("Click the button below to send video explanations to your email address:", True, BLACK)
             txt_rect = txt.get_rect(center=(216, 300))
             screen.blit(txt, txt_rect)
             y = 320
             for link in youtube_links:
                txt = small_font.render(link, True, (255, 0, 0))
                txt_rect = txt.get_rect(center=(216, y))
                screen.blit(txt, txt_rect)
                y+=30
             pygame.display.update()
           # Render and display the "Send to Email" prompt and button
          prompt_text = small_font.render("Click the button below to send video explanations to your email address:", True, BLACK)
          prompt_rect = prompt_text.get_rect(center=(216, 480))
          screen.blit(prompt_text, prompt_rect)
          input_box_rect = pygame.Rect(100, 300, 232, 50)
          send_rect = pygame.Rect(116, 530, 200, 50)
          pygame.draw.rect(screen, BLUE, send_rect)
          txt = small_font.render("Send Links to Email", True, BLACK)
          txt_rect = txt.get_rect(center=send_rect.center)
          screen.blit(txt, txt_rect)
          pygame.display.update() 
          while True:
           
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
            # Quit the game if the user closes the window
                        pygame.quit()
                        sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        display_leaderboard()
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # check if a link was clicked
                    pos = pygame.mouse.get_pos()
                    y = 320
                    for link in youtube_links:
                        txt = small_font.render(link, True, (0, 0, 255))
                        txt_rect = txt.get_rect(center=(216, y))
                        if txt_rect.collidepoint(pos):
                            webbrowser.open(link)
                            break
                        y += 20
                    if send_rect.collidepoint(event.pos):
                         email_address = input_box(prompt="Enter your email address:")
                         send_email(email_address,youtube_links)
                     #screen.fill((108, 207, 246))      
            
            
            pygame.display.update()
      #pygame.display.update()

    elif phase=='login':
        #print(username,password)
        screen.fill((108, 207, 246))
        for j,i in enumerate(login_rects):
            if mouse_buttons[0] and not login_rects[1].collidepoint(mouse) and not login_rects[0].collidepoint(mouse):
                active=-1
            if active==j:
                x=(255, 240, 124)
                pygame.draw.rect(screen,(0,0,0),looks[j],2)
                #print(i.right)
            else:
                x=128, 255, 114
            login_box.fill(x)
            if j==0:
                txt=small_font.render(username,True,(0,0,0))
                txt_rect=txt.get_rect(center=(144,10))
                login_box.blit(txt,txt_rect)
            else:
                txt=small_font.render(len(password)*"*",True,(0,0,0))
                txt_rect=txt.get_rect(center=(144,11))
                login_box.blit(txt,txt_rect)
            screen.blit(login_box,i)
            txt=small_font.render("Username",True,(0,0,0))
            screen.blit(txt,(36,284))
            txt=small_font.render("Password",True,(0,0,0))
            screen.blit(txt,(36,355))
            if i.collidepoint(mouse) and mouse_buttons[0]:
                active=j
        if the_rect.collidepoint(mouse):
            color=(230, 57, 70)
            if mouse_buttons[0]:
                phase="new_user"
        else:color=100, 50, 255
        txt=small_font.render("click here!!",True,color)
        screen.blit(txt,the_rect)
        txt=small_font.render("To create a new account",True,(0,0,0))
        txt_rect=txt.get_rect(center=(180,426))
        screen.blit(txt,txt_rect)

        txt=large_font.render("LOGIN",True,(0,0,0))
        txt_rect=txt.get_rect(center=(216,142))
        screen.blit(txt,txt_rect)
        txt=small_font.render("press ENTER after filling the details.",True,(0,0,0))
        txt_rect=txt.get_rect(center=(216,178))
        screen.blit(txt,txt_rect)
        
        if entered:
            out=csv_bs.login(username,password,"hello.csv")
            if out==-1:login_try="Not a valid username!!"
            elif out==-2:login_try="Wrong password!!"
            elif out==-3:login_try="Username not found!!"
            else:
                login_try="Log in Successful!!"
                txt=small_font.render(login_try,True,(0,0,0))
                txt_rect=txt.get_rect(center=(216,249))
                screen.blit(txt,txt_rect)
                phase="question"
            entered=False
        txt=small_font.render(login_try,True,(0,0,0))
        txt_rect=txt.get_rect(center=(216,249))
        screen.blit(txt,txt_rect)        
        pygame.display.update()

    pygame.display.update()
    clock.tick(60)

    
  