import random

MAX_BITES = 3

#Keeps track of how many times the snake has already
#bitten us. If it reaches MAX_BITES, we die and the game is over.
CURRENT_BITES = 0
ALIVE = True
MAP_SIZE = 10

def playCookTheSnake():
    """
    Is the main function for the game "Cooking a snake"
    Run this function to play
    """    
    global CURRENT_BITES
    CURRENT_BITES = 0
    
    global ALIVE
    ALIVE = True
    
    gameDescription = "First, you must light the fire. Search through the darkness for the fire pit. Don't run into the snake though!"
    
    gameControls = "Use WASD to move up/left/down/right on the map to search.\n @ = you\n S = the SNAKE\n F = fire pit\n # = unexplored space\n . = explored space"
    
    print("\nThe goal is to COOK THE SNAKE.\n")
    
    
    #print out the introductory material
    print(gameDescription)
    print("-"*50)
    print(gameControls)
    
    #start the game
    died = playGame()
    
    #check to see if the player survived
    if died:
        for i in range(40, 0, -1):
            print(i*"$")
        print("You died.")
        return 0 
        
    
    # They won, so congratulate them!
    print("YUM! That's a delicious snake.")
    print("You won the game and only got bit " + str(CURRENT_BITES) + 
          " times!")
    return 0

def playGame():
    """
    Runs each of the 5 different games.
    
    mode (int): 0 <= mode < 5
    
    Returns: (bool) True if the player died, False if they didn't
    """
    
    #Don't let the snake or the fire positions
    #be within 10 spaces of the player (unfair)

    snakePos = generatePosition([3, 3])
    firePos  = generatePosition([3, 3])
    
    #Player starts at the bottom left of the map
    playerPos = [0,0]
    
    #They can only see 1 around them
    #visibleBlocks keeps track of the visible spaces
    visibleBlocks = [[0,0], [0,1], [1, 0], [1,1]]
    step = 0
    paused_snake = 0
    updateMessage = ""
    commandMessage = "Light the fire (F)!"
    
    fireLit = False
    caughtSnake = False
    snakeInPot = False
    
    while CURRENT_BITES < MAX_BITES:
        print(str(fireLit)+" "+str(caughtSnake)+" "+str(snakeInPot))
        print("-"*50)
        drawMap(playerPos, snakePos, firePos, visibleBlocks)
        print("-"*20)
        print(commandMessage)
        
        if len(updateMessage)>0:
            print(updateMessage)
            updateMessage = ""
            
        print("Bites: "+str(CURRENT_BITES))
        
        move = ""
        
        while not move in ['W', 'A', 'S', 'D', 'w', 'a', 's', 'd']:
            move = input("Enter W A S D to move:")
        
        if move == 'W' or move == 'w':
            movePlayer(playerPos, -1, 0, caughtSnake)
        elif move == 'A' or move == 'a':
            movePlayer(playerPos, 0, -1, caughtSnake)
        elif move == 'S' or move == 's':
            movePlayer(playerPos, 1, 0, caughtSnake)
        else:
            movePlayer(playerPos, 0, 1, caughtSnake)
            
        #The snake is fast for three moves, then has to rest for one turn
        #It knows where the player is and moves towards it
        
        #After the snake bites, PAUSED_SNAKE is > 0
        # and decrements by one each step until it reaches 0
        # (escape time for the player)
        
        #As long as we haven't caught the snake
        if not caughtSnake:
            if step % 4 < 3 and paused_snake == 0:
                moveSnake(snakePos, playerPos, fireLit)
            elif paused_snake > 0:
                paused_snake -= 1
                
        updateVisibleBlocks(playerPos, visibleBlocks)
        
        collisionWith, updateMessage = handleCollisions(playerPos, snakePos, firePos, fireLit)
        
        #collisions is a dictionary of boolean values with entity names as keys
        if collisionWith['snake']:
            if not fireLit:
                #The snake is pursuing us
                paused_snake = 2
            else:
                #We are trying to catch the snake, and we did
                commandMessage = "Put the snake in the fire (F)!"
                snakePos = [100,100]
                caughtSnake = True
                
        elif collisionWith['fire']:
            if not fireLit:
                fireLit = True
                commandMessage = "Catch the snake (S)!"
            elif caughtSnake:
                snakeInPot = True
                return False
        
        step += 1
    
    return True
    
def handleCollisions(playerPos, snakePos, firePos, fireLit):
    """
    Checks for collisions between the player and the snake or the fire
    Returns the time for the snake to pause after a bite
    """
    result = {"snake":False, "fire":False}
    if playerPos == snakePos:
        global CURRENT_BITES
        
        message = ""
        if not fireLit:
            CURRENT_BITES += 1
            message = "YOU GOT BIT!!!"
            
        result['snake'] = True
        #pause the snake for 2 steps to let the player escape a bit
        return result, message
    
    elif playerPos == firePos:
        result['fire'] = True
        return result, "You lit the fire!"
    
    return result, ""
    
def moveSnake(snakePos, playerPos, fireLit):
    """
    Generate the new snake position (it can move sideways 2x as quickly)
    It knows where the player is and moves toward it.
    
    If the fire is lit, the snake will run away from the player
    
    """
    multiplier = 1
    
    if fireLit:
        #The snake is blinded with rage and fear
        speed = random.randint(1, 2)
        axis = random.randint(0, 1)
        multiplier = 1

        if (random.randint(0, 1) == 0):
            multiplier = -1
            
        snakePos[axis] += speed * multiplier
        
    else: 
        if playerPos[0] < snakePos[0]:
            snakePos[0] -= 1
        elif playerPos[0] > snakePos[0]:
            snakePos[0] += 1
        elif playerPos[1] < snakePos[1]:
            snakePos[1] -= 2
        elif playerPos[1] > snakePos[1]:
            snakePos[1] += 2
        
    #check to make sure it isn't out of bounds
    if snakePos[0] < 0:
        snakePos[0] = 0
    
    if snakePos[1] < 0:
        snakePos[1] = 0
    
    if snakePos[0] >= MAP_SIZE:
        snakePos[0] = MAP_SIZE - 1
        
    if snakePos[1] >= MAP_SIZE:
        snakePos[1] = MAP_SIZE - 1
        
    
    
    
def movePlayer(playerPos, dx, dy, caughtSnake):
    """
    Changes the position of the player.
    Is responsible for checking bounds and collision with pit/snake
    
    If we've caught the snake, it is thrashing around and can 
    affect our movement
    """
    if caughtSnake:
        if random.randint(0, 2):
            if random.randint(0, 1) == 0:
                dx *= -1
            else:
                dy *= -1
    
    playerPos[0] += dx
    playerPos[1] += dy
    
    
            
    
    for i in range(2):
        if playerPos[i] < 0:
            playerPos[i] = 0
        elif playerPos[i] >= MAP_SIZE:
            playerPos[i] = MAP_SIZE - 1    
            
    
    
def updateVisibleBlocks(playerPos, visibleBlocks):
    """
    Adds the newly visible blocks to the list if they aren't already
    there
    """
    
    for i in range(-1, 2):
        for j in range(-1, 2):
            visiblePos = [playerPos[0]+i, playerPos[1]+j]
            if not visiblePos in visibleBlocks:
                visibleBlocks.append(visiblePos)
            
            
def drawMap(playerPos, snakePos, firePos, visibleBlocks):
    
    for i in range(MAP_SIZE):
        for j in range(MAP_SIZE):
            drawLocation = [i,j]
            if drawLocation == playerPos:
                print("@", end="")
            elif drawLocation == snakePos and snakePos in visibleBlocks:
                print("S", end="")
            elif drawLocation == firePos and firePos in visibleBlocks:
                print("F", end="")
            elif drawLocation in visibleBlocks:
                print(".", end="")
            else:
                print("#", end="")
        
        print("\n", end="")
        
def generatePosition(lowerBound):
    """
    Returns a random position (as a list of length 2)
    on a 2d map of size MAP_SIZE.
    
    Exclude any values underneath the lowerBound coordinate
    
    Note: position is relative to the top left of map and starts at 0
    
    ###
    ##F
    ###
    
    (F is at [2, 1])
    """
    
    newPos = [0,0]
    
    while newPos[0] <= lowerBound[0] or newPos[1] <= lowerBound[1]:
        for i in range(2):
            newPos[i] = random.randint(0, MAP_SIZE-1)
     
    return newPos
