'''
adventure game - guess numbers for points and health
This is a demo to show how dictionaries can be used to 
maintain the state of an interactive app.
'''

from logging import root
from random import randint
from tkinter import *

root = Tk()
root.title("Jake's Adventure Game")
root.geometry('500x500')

#Start
def play_game(state,root): #Asks the user if they want to play the game
    ''' move to the appropriate room and check for win or loss '''
    if state['played'] == 'no':
        wantplay = IntVar(master=root, value= 0)
        nextstep = wantplay.get()
        if nextstep == 0:
            playing = Label(root, text="Do you want to play an adventure game? ")
            playing.pack()
            yes_button = Button(root, text="Yes", command=lambda: [playing.pack_forget(), yes_button.pack_forget(), no_button.pack_forget(), yesgame(state,root)])
            yes_button.pack(side=LEFT, expand=TRUE, fill=X)
            no_button = Button(root, text='No', command=lambda: [playing.pack_forget(), yes_button.pack_forget(), no_button.pack_forget(), nogame(state,root)])
            no_button.pack(side=RIGHT, expand=TRUE, fill=X)
            global space
            space = Label()
            space.pack()
            no_button.wait_variable()

    elif state['played'] == 'yes':
        while state['room']!= 'menu':
            root.after(500)
            print_state(state,root)
            end_game(state,root)
            process_next_room(state,root)


#Playing states
def yesgame(state,root): #User wants to play the game
    while state['room']!= 'menu':
        print_state(state,root)
        end_game(state,root)
        process_next_room(state,root)

def nogame(state,root): #User does not want to play the game
        space.pack()
        ok = Label(root, text="----------OK!----------")
        ok.pack()
        space.pack()
        quitting = Label(root, text='quitting game')
        quitting.pack()
        root.after(3000)
        quit()


#Stats
def print_state(state,root): #Prints the current stats
    ''' show values of state variables '''
    for widget in root.winfo_children():
        widget.pack_forget()
    global stats
    stats = Label(root, text='location = ' +str(state['room'])+ ' |  points = ' +str(state['points'])+ ' |  health = ' +str(state['health']))
    stats.pack(side=TOP)
    global dash
    dash = Label(root, text='-'*20)
    dash.pack(side=TOP)


#End
def end_game(state,root): #Checks for win or loss and ends the game accordingly
    '''tells the user the results of the game'''
    if state['health']<=0 or state['points']<=0:
        space.pack()
        lose = Label(root, text='you lose!')
        lose.pack()
        root.after(1000)
        lose.pack_forget()
        state['room'] = 'menu'
        loading_next(state,root)
    elif state['points']>=200:
        space.pack()
        win = Label(root, text='you win!')
        win.pack()
        root.after(1000)
        win.pack_forget()
        state['room'] = 'menu'
        loading_next(state,root)


#Changing Rooms   
def process_next_room(state,root): #Tells the code which room the user is going to
    '''looks at the state['room'] and calls the appropriate function'''
    room = state['room']
    if room=='living room':
        process_living_room(state,root)
    elif room== 'game room':
        process_game_room(state,root)
    elif room=='kitchen':
        process_kitchen (state,root)
    elif room=='dining room':
        process_dining_room(state,root)
    elif room=='office':
        process_office(state,root)
    elif room=='menu':
        root.after(1000)
        again = Label(root, text="Do you want to play again?")
        again.pack()
        replay = Button(root, text='Yes', command= lambda: [again.pack_forget(), replay.pack_forget(), im_done.pack_forget(), new_game(root)])
        replay.pack(side=LEFT, expand=TRUE, fill=X)
        im_done = Button(root, text='No', command= lambda: [again.pack_forget(), replay.pack_forget(), im_done.pack_forget(), done_game(root)])
        im_done.pack(side=LEFT, expand=TRUE, fill=X)
        im_done.wait_variable()

def new_game(root): #Starts a new game for the user
    root.after(500)
    play_game(again_state,root)

def done_game(root): #Ends the game and closes the playing window
    space = Label()
    space.pack()
    thanks = Label(root, text='----------Thanks for playing!----------')
    thanks.pack()
    root.after(3000)
    quit()

def loading_next(state,root): #Prints the changing room text
    '''prints a loading sequence while taking the user to the next room'''
    next_room = Label(root, text='Going to the ' +state['room'])
    next_room.pack()
    dashes = Label(root, text='--------------------')
    dashes.pack()
    root.after(2000)
    next_room.pack_forget()
    dashes.pack_forget()
    print_state(state,root)
    process_next_room(state,root)

def kitchen(state,root): #Set and send to kitchen
    state['room']= 'kitchen'
    loading_next(state,root)

def office(state,root): #Set and send to office
    state['office_counter'] = 1
    state['room']= 'office'
    loading_next(state,root)

def gameroom(state,root): #Set and send to game room
    state['room']= 'game room'
    loading_next(state,root)

def diningroom(state,root): #Set and send to dining room
    print_state(state,root)
    state['room']= 'dining room'
    loading_next(state,root)


#Rooms
def process_living_room(state,root): #Living room 
    ''' move to kitchen or office'''
    print_state(state,root)
    welcome_living = Label(root, text='Welcome to the living room')
    welcome_living.pack()
    root.after(1000)
    if state['office_counter'] != 1:
        response = Label(root, text="Do you want to eat or go to work?")
        response.pack()
        root.after(500)
        eat = Button(root, text='Eat', command= lambda: [response.pack_forget(), eat.pack_forget(), 
                                                         work.pack_forget(), welcome_living.pack_forget(), 
                                                         kitchen(state,root)])
        eat.pack(side=LEFT, expand=TRUE, fill=X)
        work = Button(root, text='Work', command= lambda: [response.pack_forget(), eat.pack_forget(), 
                                                           work.pack_forget(), welcome_living.pack_forget(), 
                                                           office(state,root)])
        work.pack(side=RIGHT, expand=TRUE, fill=X)
        work.wait_variable()
    else:
        response = Label(root, text="Do you want to eat?")
        response.pack()
        root.after(500)
        yes = Button(root, text='Yes', command= lambda: [welcome_living.pack_forget(), response.pack_forget(), yes.pack_forget(), no.pack_forget(), kitchen(state,root)])
        yes.pack(side=LEFT, expand=TRUE, fill=X)
        no = Button(root, text='No', command= lambda: [welcome_living.pack_forget(), response.pack_forget(), yes.pack_forget(), no.pack_forget(), gameroom(state,root)])
        no.pack(side=LEFT, expand=TRUE, fill=X)
        no.wait_variable()
        end_game(state,root)

def process_game_room(state,root): #Game room
    ''' ask user to guess a number or play craps, and reward or penalize accordingly'''
    
    games = Label(root, text='Welcome to the game room')
    games.pack()
    root.after(1000)
    options = Label(root, text="Do you want to play craps or a guessing game?")
    options.pack()
    craps = Button(root, text="Craps", command=lambda: [options.pack_forget(), craps.pack_forget(), guess.pack_forget(), games.pack_forget() ,launching_craps(state,root)])
    craps.pack(side=LEFT, expand=TRUE, fill=X)
    guess = Button(root, text='Guessing Game', command=lambda: [options.pack_forget(), craps.pack_forget(), guess.pack_forget(), games.pack_forget(), play_guess(state,root)])
    guess.pack(side=RIGHT, expand=TRUE, fill=X)
    guess.wait_variable()

def process_kitchen(state,root): #Kitchen
    ''' let user buy some food and change points/health '''
    print_state(state,root)
    welcome_kitchen = Label(root, text='Welcome to the kitchen')
    welcome_kitchen.pack()
    root.after(1000)
    what_eat = Label(root, text="What do you want to eat?")
    what_eat.pack()
    root.after(500)
    choice_steak = Button(root, text="Steak", command= lambda: [what_eat.pack_forget(), choice_steak.pack_forget(), 
                                                                choice_salad.pack_forget(), choice_sushi.pack_forget(), 
                                                                choice_nothing.pack_forget(), welcome_kitchen.pack_forget(), steak(state,root)])
    choice_steak.pack(side=LEFT, expand=TRUE, fill=X)
    choice_salad = Button(root, text="Salad", command= lambda: [what_eat.pack_forget(), choice_steak.pack_forget(), 
                                                                choice_salad.pack_forget(), choice_sushi.pack_forget(), 
                                                                choice_nothing.pack_forget(), welcome_kitchen.pack_forget(), salad(state,root)])
    choice_salad.pack(side=LEFT, expand=TRUE, fill=X)
    choice_sushi = Button(root, text="Sushi", command= lambda: [what_eat.pack_forget(), choice_steak.pack_forget(), 
                                                                choice_salad.pack_forget(), choice_sushi.pack_forget(), 
                                                                choice_nothing.pack_forget(), welcome_kitchen.pack_forget(), sushi(state,root)])
    choice_sushi.pack(side=LEFT, expand=TRUE, fill=X)
    choice_nothing = Button(root, text="Nothing", command= lambda: [what_eat.pack_forget(), choice_steak.pack_forget(), 
                                                                    choice_salad.pack_forget(), choice_sushi.pack_forget(), 
                                                                    choice_nothing.pack_forget(), welcome_kitchen.pack_forget(), nothing(state,root)])
    choice_nothing.pack(side=LEFT, expand=TRUE, fill=X)

def process_dining_room(state,root): #Dining room
    ''' kick user out if they don't like the food '''
    state['office_counter'] = 0
    welcome_dining = Label(root, text='Welcome to the dining room')
    welcome_dining.pack()
    root.after(1000)
    how_meal = Label(root, text="How is your meal?")
    how_meal.pack()
    root.after(500)
    good_meal = Button(root, text='Good', command= lambda: [welcome_dining.pack_forget(), how_meal.pack_forget(), good_meal.pack_forget(),bad_meal.pack_forget(), good(state,root)])
    good_meal.pack(side=LEFT, expand=TRUE, fill=X)
    bad_meal = Button(root, text='Bad', command= lambda: [welcome_dining.pack_forget(), how_meal.pack_forget(), good_meal.pack_forget(),bad_meal.pack_forget(), bad(state,root)])
    bad_meal.pack(side=LEFT, expand=TRUE, fill=X)
    bad_meal.wait_variable()

def process_office(state,root): #Office
    ''' tells user it is time to go home after a long day of work
    and sends them to the living room and adds 50 points'''
    welcome_office = Label(root, text='Welcome to the office')
    welcome_office.pack()
    root.after(1000)
    response = Label(root, text='Are you finished with your work for the day?')
    response.pack()
    root.after(500)
    done_work = Button(root, text='Yes', command= lambda: [welcome_office.pack_forget(), response.pack_forget(), 
                                                           done_work.pack_forget(), keep_work.pack_forget(), 
                                                           stop_work(state,root)])
    done_work.pack(expand=TRUE, side=LEFT, fill=X)
    keep_work = Button(root, text='No', command= lambda: [welcome_office.pack_forget(), response.pack_forget(), 
                                                          done_work.pack_forget(), keep_work.pack_forget(), 
                                                          continue_work(state,root)])
    keep_work.pack(expand=TRUE, side=RIGHT, fill=X)


#Office options
def stop_work(state,root): #Ends work for the user
    space.pack()
    productive_day = Label(root, text='You had a productive day and gained 50 points')
    productive_day.pack()
    state['points'] += 50
    state['room'] = 'living room'
    root.after(750)
    end_game(state,root)
    loading_next(state,root)

def continue_work(state,root): #Keeps user at work for a bit longer
    space.pack()
    productive_day = Label(root, text="Wow! You're a hard worker! You stayed at work for 1 more hour.")
    productive_day.pack()
    reward = Label(root, text='Your great day earned you 75 points but came at the cost of 5 health')
    reward.pack()
    state['points'] += 75
    state['health'] -= 5
    state['room'] = 'living room'
    root.after(750)
    end_game(state,root)
    loading_next(state,root)
    

#Kitchen options
def nothing(state,root): #What to do if user wants nothing
    state['health'] -= 5
    nextroom = Label(root, text="Where would you like to go next?")
    nextroom.pack()
    go_office = Button(root, text= 'Office', command= lambda: [nextroom.pack_forget(), go_office.pack_forget(), go_game_room.pack_forget(), office(state,root)])
    go_office.pack(side=LEFT, expand=TRUE, fill=X)
    go_game_room = Button(root, text='Game Room', command= lambda: [nextroom.pack_forget(), go_office.pack_forget(), go_game_room.pack_forget(), gameroom(state,root)])
    go_game_room.pack(side=LEFT, expand=TRUE, fill=X)
    go_game_room.wait_variable()

def steak(state,root): #What to do if user wants steak
    enjoy = Label(root, text='Please enjoy your steak in the dining room!')
    enjoy.pack()
    root.after(1000)
    enjoy.pack_forget()
    state['points'] -= 20
    state['health'] += 10
    diningroom(state,root)

def salad(state,root): #What to do if user wants salad
    enjoy = Label(root, text='Please enjoy your salad in the dining room!')
    enjoy.pack()
    root.after(1000)
    enjoy.pack_forget()
    state['points'] -= 5
    state['health'] += 10
    diningroom(state,root)
    
def sushi(state,root): #What to do if user wants sushi
    enjoy = Label(root, text='Please enjoy your sushi in the dining room!')
    enjoy.pack()
    root.after(1000)
    enjoy.pack_forget()
    state['points'] -= 20
    state['health'] += 10
    diningroom(state,root)
    


#Dining room options
def good(state,root): #User says food is good
    grateful = Label(root, text="I'm glad you like it")
    grateful.pack()
    root.after(500)
    nextroom = Label(root, text="Where would you like to go next?")
    nextroom.pack()
    root.after(500)
    go_office = Button(root, text= 'Office', command= lambda: [grateful.pack_forget(), nextroom.pack_forget(), go_office.pack_forget(), go_game_room.pack_forget(), office(state,root)])
    go_office.pack(side=LEFT, expand=TRUE, fill=X)
    go_game_room = Button(root, text='Game Room', command= lambda: [grateful.pack_forget(), nextroom.pack_forget(), go_office.pack_forget(), go_game_room.pack_forget(), gameroom(state,root)])
    go_game_room.pack(side=LEFT, expand=TRUE, fill=X)
    go_game_room.wait_variable()

def bad(state,root): #User says food is bad
    ungrateful = Label(root, text="You are ungrateful and I'm kicking you out!")
    ungrateful.pack()
    root.after(500)
    bye = Label(root, text="Goodbye!")
    bye.pack()
    root.after(500)
    state['room']='menu'
    loading_next(state,root)
    end_game(state,root)


#Guessing Game
def play_guess(state,root): #Beginning code of guessing game. (contains choices 1-4)
    '''guessing game'''
    global answer
    answer = randint(1,4)
    guess = Label(root, text="guess a number between 1 and 4 to get 20 points: ")
    guess.pack()
    root.after(1000)
    global choice
    choice = IntVar ()
    guess1 = Button(root, text='1', command= lambda: [choice.set(1), guess.pack_forget(), 
                                                      guess1.pack_forget(), guess2.pack_forget(), 
                                                      guess3.pack_forget(), guess4.pack_forget(), 
                                                      guessing_cont(state,root)])
    guess1.pack(expand=TRUE, fill=X, side=LEFT)
    guess2 = Button(root, text='2', command= lambda: [choice.set(2), guess.pack_forget(), 
                                                      guess1.pack_forget(), guess2.pack_forget(), 
                                                      guess3.pack_forget(), guess4.pack_forget(), 
                                                      guessing_cont(state,root)])
    guess2.pack(expand=TRUE, fill=X, side=LEFT) 
    guess3 = Button(root, text='3', command= lambda: [choice.set(3), guess.pack_forget(), 
                                                      guess1.pack_forget(), guess2.pack_forget(), 
                                                      guess3.pack_forget(), guess4.pack_forget(), 
                                                      guessing_cont(state,root)])
    guess3.pack(expand=TRUE, fill=X, side=LEFT)
    guess4 = Button(root, text='4', command= lambda: [choice.set(4), guess.pack_forget(), 
                                                      guess1.pack_forget(), guess2.pack_forget(), 
                                                      guess3.pack_forget(), guess4.pack_forget(), 
                                                      guessing_cont(state,root)])
    guess4.pack(expand=TRUE, fill=X, side=LEFT)
    guess4.wait_variable()
    global chosen

def guessing_cont(state,root): #Tells the user if they chose correctly or not
    root.after(500)
    chosen = int(choice.get())
    playagain='y'
    global correct
    correct = Label(root, text="You guessed it. You get 20 points!")
    global wrong
    wrong = Label(root, text="Wrong guess. The answer was " +str(answer))
    global minus_ten
    minus_ten = Label(root, text="You lose 10 points")
    while playagain == 'y':
        if chosen==answer:
            state['points'] += 20
            stats.pack_forget(), dash.pack_forget()
            print_state(state,root)
            space.pack()
            correct.pack()
        else:
            state['points'] -= 10
            stats.pack_forget(), dash.pack_forget()
            print_state(state,root)
            space.pack()
            wrong.pack()
            root.after(250)
            minus_ten.pack()
        root.after(500)
        playagain = Label(root, text='Do you want to play again?')
        playagain.pack()
        guess_again_yes = Button(root, text='Yes', command= lambda: [correct.pack_forget(), wrong.pack_forget(), 
                                                                     minus_ten.pack_forget(), playagain.pack_forget(), 
                                                                     space.pack_forget(), guess_again_yes.pack_forget(), 
                                                                     guess_again_no.pack_forget(), guess_yes(state,root)])
        guess_again_yes.pack(expand=TRUE, side=LEFT, fill=X)
        guess_again_no = Button(root, text='No', command= lambda: [correct.pack_forget(), wrong.pack_forget(), 
                                                                     minus_ten.pack_forget(), playagain.pack_forget(), 
                                                                     space.pack_forget(), guess_again_yes.pack_forget(), 
                                                                     guess_again_no.pack_forget(), guess_no(state,root)])
        guess_again_no.pack(expand=TRUE, side=RIGHT, fill=X)

def guess_yes(state,root): #Allows the user to keep playing the guessing game
    print_state(state,root)
    play_guess(state,root)

def guess_no(state,root): #Ends the guessing game
    state['room'] = 'living room'
    end_game(state,root)
    loading_next(state,root)


#Craps functions
def launching_craps(state,root): #Prints launching screen for the craps game
    global craps
    craps = Label(root, text='Launching Craps')
    craps.pack()
    dash = Label(root, text='-'*20)
    dash.pack()
    space = Label()
    space.pack()
    root.after(1500)
    dash.pack_forget()
    play_craps(state,root)

def play_craps(state,root): #Determines if the user has enough points to play craps and asks how much tey want to bet
    ''' repeatedly asks the user if they want to play
        if so, it calls play1game()
        and continues until they don't want to play anymore
    '''
    if state['points'] == 0:
        craps.pack_forget(), 
        notenough = Label(root, text='You do not have enough points to play craps')
        notenough.pack()
        end_game(state,root)
    else:
        craps.pack_forget(), 
        playvar = 'y'
        while playvar == 'y' and state['points'] != 0:
            global casino
            casino = Label(root, text="How much would you like to bet? ")
            casino.pack()
            global amount
            amount = Entry(root)
            amount.pack()
            global submit_bet
            submit_bet = Button(root, text='Submit', command=lambda: [submit_bet.pack_forget(), casino.pack_forget(), clear_entry(state,root)])
            submit_bet.pack()
            submit_bet.wait_variable()

def clear_entry(state,root): #Removes the betting screen after user presses submit
    bet = int(amount.get())
    amount.pack_forget()
    after_bet(state,root,bet)

def after_bet(state,root,bet): #Lets the user know if their bet was invalid as well as letting the user know if they won or lost
    if bet > state['points']:
        space = Label()
        space.pack()
        invalid_amount = Label(root, text='Invalid Amount')
        invalid_amount.pack()
        too_large = Label(root, text='Bet may not be larger than ' +str(state['points']))
        too_large.pack()
        new_bet = Label(root, text='Enter new bet')
        new_bet.pack()
    elif bet < 1:
        space = Label(root)
        space.pack()
        invalid_amount = Label(root, text='Invalid Amount')
        invalid_amount.pack()
        too_small = Label(root, text='Bet must be greater than 0')
        too_small.pack()
        new_bet = Label(root, text='Enter new bet')
        new_bet.pack()
    else:
        win = Label(root, text="Good job, you won")
        lose = Label(root, text="Sorry, you lost")
        user_won = play1game(root)
        if user_won:
            root.after(750)
            space = Label()
            space.pack()
            win.pack()
            space.pack()
            state['points'] += bet
        else:
            root.after(750)
            space = Label()
            space.pack()
            lose.pack()
            space.pack()
            state['points'] -= bet
        root.after(1000)
        global current_points
        current_points = Label(root, text="You have " +str(state['points'])+ " points")
        current_points.pack()

        if state['points']== 0:
            root.after(500)
            end_game(state,root)
        
        playvar = Label(root, text="Do you want to play again?")
        playvar.pack()
        yesbutton = Button(root, text="Yes", command=lambda: [playvar.pack_forget(), win.pack_forget(), 
                                                              lose.pack_forget(), current_points.pack_forget(), 
                                                              yesbutton.pack_forget(), nobutton.pack_forget(), 
                                                              space.pack_forget(), rolling_again.pack_forget(), 
                                                              rolls.destroy, before7.pack_forget(), 
                                                              current_points.pack_forget(), stats.pack_forget(), 
                                                              dash.pack_forget(), againyes(state,root)]
                                                              )
        yesbutton.pack(side=LEFT, expand=TRUE, fill=X)
        nobutton = Button(root, text='No', command=lambda: [playvar.pack_forget(), win.pack_forget(), 
                                                            lose.pack_forget(), current_points.pack_forget(), 
                                                            yesbutton.pack_forget(), nobutton.pack_forget(), 
                                                            space.pack_forget(), rolling_again.pack_forget(), 
                                                            rolls.destroy, before7.pack_forget(), 
                                                            current_points.pack_forget(), stats.pack_forget(), 
                                                            dash.pack_forget(), againno(state,root)]
                                                            )
        nobutton.pack(side=RIGHT, expand=TRUE, fill=X)
        nobutton.wait_variable()

def againyes(state,root): #Lets the user play again
    print_state(state,root)
    space.pack()
    play_craps(state,root)

def againno(state,root): #Ends the craps game for the user
    print_state(state,root)
    state['room'] = 'living room'
    end_game(state,root)
    loading_next(state,root)

def roll2dice(root): #Rolls 2 dice for the user
    ''' simulates rolling 2 dice and returns the sum of the dice '''
    root.after(2000)
    space.pack_forget(), rolling.pack_forget(), rolling_again.pack_forget()
    die1 = randint(1,6)
    die2 = randint(1,6)

    sum = die1+die2
    global rolls
    rolls = Label(root, text="you rolled a " +str(die1)+  " and a " +str(die2))
    rolls.pack()
    return sum

def play1game(root): #Plays the beginning of a craps game and pronts rolling screens
    ''' simulates one game of craps and returns True if user wins, false if they
        lose and it prints out all fo the rolls of the dice.
    '''
    amount.pack_forget()
    space.pack()
    space.pack()
    global rolling
    rolling = Label(root, text='\U0001F3B2 Rolling \U0001F3B2')
    rolling.pack()
    global rolling_again
    rolling_again = Label(root, text=('\U0001F3B2 Rolling again \U0001F3B2'))
    space.pack()
    roll1 = roll2dice(root)
    global before7
    before7 = Label(root, text='you must roll a ' +str(roll1)+ ' before a 7')
    if roll1 == 2 or roll1 == 3 or roll1 == 12:
        return False
    elif roll1 == 7 or roll1 == 11:
        return True
    else:
        before7.pack()
        result = play_rest_game(roll1,root)
        return result

def play_rest_game(point,root): #Plays the rest of the craps game for the user
    ''' returns True if they roll the point before a 7, False otherwise '''
    space.pack()
    space.pack()
    rolling_again.pack()
    space.pack()
    roll = roll2dice(root)
    while roll != point and roll!=7:
        space.pack()
        rolling_again.pack()
        space.pack()
        roll=roll2dice(root)
        if roll==point:
            return True
        else:
            return False


starting_state = {'room':'game room','points':100,'health':10, 'office_counter':0, 'played':'no'}
again_state = {'room':'game room','points':100,'health':10, 'office_counter':0, 'played':'yes'}

play_game(starting_state,root)

global space
space = Label()

root.mainloop()

