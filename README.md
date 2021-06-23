# Lab 2: Path Finding

## Intro
More than just making our characters move, we want them to make decisions through code. We'll be setting up multiple scenarios where you'll have to guide your main character sprite through an obstacle course.

In this lab, we will be practicing our conditionals and operators. You will be dealing with "if" statements, using them to program choices that your sprite will make.

## Set Up
* Click the green 'Code' button on the top right of this section.
* Find 'Download ZIP' option and click it
* Unzip the file and move it over to your 'workspace' folder (or wherever you keep your files)

* Find the folder and open the entire folder in VSCode
    * You can find it in your Files and right click on it. Use the "Open with VSCode" option
    * You can also open VSCode, go to 'File' > 'Open' and then find the lab folder

* With VSCode open, go to the top of your window and find `Terminal`
* Click `Terminal`
* Click `New Terminal`

* In the new window that opens at the bottom of VSCode, type in
```
python run_small.py
```

* Hit enter
* You should see a game window open up, with a small grid and game objects.
* You are done with set up!

## Game Explanation
This is a puzzle game where you use Code to control the actions of your character. Your objective is to collect all the diamonds and reach the flag.

However there are obstacles in the way. If you touch an obstacle or go out of bounds, then its game over.

ALSO, every time you pick up a diamond, that square will turn into an obstacle, so you can not go back across it.

Your objective is to pre-plan your route, using conditionals to give the correct directions to your character. Inside of `lab.py` you will find 3 functions, that will apply individually to the three game scenarios we have.

## Lab Steps
* All the code you will need to edit is in `lab.py`
* `run_small.py`, `run_med.py`, and `run_big.py` are used to run the game. If you take a look inside, you can see how we set up the game to be played.
* Everything inside the `engine/` folder are the inner workings of the game. Feel free to take a look, but you won't need to change anything (unless you want to change your sprite speed)
* If at any point in the lab, you would like to change your sprite speed, open up `engine/game.py` and edit the variable `CHARACTER_SPEED`.

### Small Map
Let's get started with the small map scenario. If you notice, we have an obstacle in the center, a diamond at the top center, and the flag at the top right.

* Let's first see what happens when we don't give our character any commands
* Open up your terminal (if it isn't open already) and type in `python run_small.py` and hit enter
* Notice how our character immediately starts going to the right, but doesn't stop!
* Let's look ahead and make an observation. If we want to get the diamond AND get to the flag, we need to start the game by moving up.
    * PS: If we don't give any directions, our sprite just moves to the right at the beginning of the game. This is just default behavior.
* Go into `lab.py` and find the function:
```python
def lab_run_small(coord_name):
    """
    This function is given to the game in run_small.py
    """
    pass
```
* Notice how the comments say that this function runs in run_small.py
* `lab_run_small` is a function we call in the game engine, that will be used to decide what direction to go. 
    * It takes in a variable called `coord_name`. This variable is how we represent the grid. It is similar to chess, with the x-axis having letters and y-axis having numbers.
    * For example a0 will be at block (0, 0) in the grid.
    * Everytime a sprite steps into a new block in the grid, it will call the `lab_run_small` function and expect a direction.
    * If no new direction is given, the sprite will keep moving in the same direction.
* To get us started, let's write a conditional that will make our character move upwards at the start of the game
* Replace the function with:
```python
def lab_run_small(coord_name):
    """
    This function is given to the game in run_small.py
    """
    if coord_name == 'a0':
        return up
```
* If you notice, we check if coord_name equals `a0`, which is the starting position of our character.
* At the begining of the game, that conditional is triggered immediately, and we set our character's direction to `up`
* Make sure to save your file and then run the game again with `python run_small.py`

* Notice how our sprite now moves up!
* However, we keep moving up until we go out of bounds. So we must add another conditional to make sure our character turns again.
* Replace the function again with:
```python
def lab_run_small(coord_name):
    """
    This function is given to the game in run_small.py
    """
    if coord_name == 'a0':
        return up
    if coord_name == 'a2':
        return right
```
* If you see, we check to see if our current position is the 'a2' block. If that conditional is True, then we tell our character to turn right. 
* This should move our character through the diamond (collecting it) and to the flag!
* Save your file and run the game with `python run_small.py`
* Your character should make it to the end, and you win!

### Medium Map
Now that you got your feet wet, let's try something a little more challenging.

* Let's take a look at the new map by running `python run_med.py`
* Notice how we have to get a diamond, backtrack, and then move towards the flag.
* Now let's take a look at our function:
```python
def lab_run_med(coord_name):
    """
    This function is given to the game in run_med.py
    """
    global got_treasure
    pass
```
* Notice the line `global got_treasure`. Don't mind this for now, we'll be using it later.
* Let's do our first crack at solving the game. Replace the `lab_run_med` function with:
```python
def lab_run_med(coord_name):
    """
    This function is given to the game in run_med.py
    """
    global got_treasure
    if coord_name == 'a0':
        return up
    if coord_name == 'a3':
        return right
    if coord_name == 'd3':
        return down
    if coord_name == 'd0':
        return up
    if coord_name == 'd3':
        return right
```
* This looks similar to what we did last lab. Just find each position, and give the direction we want there.
* Save your file and run `python run_med.py` to take a look at what happens.

* That's not right! If you notice, at the 'd3' block, our conditionals clash. The only one that gets run is whichever appears first.
* In order to fix this, we need to add another boolean! This will keep track of whether we got the treasure yet.
* Now our thinking will be: 
    * if we get to 'd3' but don't have the treasure, then move down and towards the diamond
    * if we get to 'd3' AND have the treasure, then move right and towards the flag
* `got_treasure` is a boolean that starts off as `False` (since we don't have the treasure at the beginning). After we get the treasure, then we can update it to `True` and use it to trigger new conditionals!
    * PS: The global keyword means that the variable we want to use is "outside" of the function. This allows us to reference it inside the function. MOST IMPORTANTLY, if we change the value during one run of our function, that value will STAY THE SAME. 
    * https://www.w3schools.com/python/python_variables_global.asp
* Change our function now to:
```python
def lab_run_med(coord_name):
    """
    This function is given to the game in run_med.py
    """
    global got_treasure
    if coord_name == 'a0':
        return up
    if coord_name == 'a3':
        return right
    if coord_name == 'd3':
        return down
    if coord_name == 'd0':
        got_treasure = True
        return up
    if coord_name == 'd3' and got_treasure == True:
        return right
```
* Notice that when we know we are at block 'd0' (which is where the diamond is), we can change the `got_treasure` variable to `True`. This means that we now have the treasure, and can change our behavior because of it.
* The last conditional is now `coord_name == 'd3' and got_treasure == True`, meaning that BOTH statements need to be true, for us to turn right
* Save your file and run `python run_med.py` to test your changes. Do you think this will work? Take a good look at our code and take a guess.

* What happened here?
* If you notice, the conditionals are applied from TOP to BOTTOM. 
* If you were to take your current position and evaluate each statement one by one starting from the top, you would notice that both times at 'd3' we trigger the same conditional and go downwards!
* This is because `coord_name == d3` generally applies to all conditions where we are at 'd3'. It will greedily trigger those conditions and not allow anything else involving 'd3' to trigger below it.
* Luckily, this is a simple fix. Let's take the more SPECIFIC conditional and move it up top.
* Move around the last conditional so our function now looks like:
```python
def lab_run_med(coord_name):
    """
    This function is given to the game in run_med.py
    """
    global got_treasure
    if coord_name == 'd3' and got_treasure == True:
        return right
    if coord_name == 'a0':
        return up
    if coord_name == 'a3':
        return right
    if coord_name == 'd3':
        return down
    if coord_name == 'd0':
        got_treasure = True
        return up
    if coord_name == 'g3':
        return down
```
* Now if you notice, the first time we land on 'd3', half of the first conditional returns True. 
* However since its a double conditional joined by an `AND` operator, and we haven't set `got_treasure = True` yet, the entire statement becomes `False`.
* Therefore, we skip it this time, and match the condition to `coord_name == 'd3'`
* The next time we arrive at 'd3', we have already got the diamond and set `got_treasure = True`
* Now that both sides of the `AND` operator are `True`, we trigger that condtional, making us turn right.
* Save your file and run `python run_med.py`
* You should successfully backtrack and win the game!

### Big Map
Alright, now you're experienced. You know your stuff. Let's put you on the big map.

I will leave you to figure this out on your own. You should be able to use the learnings from the Small and Med Maps to solve this larger case.

I have provided you with two extra global booleans to use:
* `got_treasure_1`
* `got_treasure_2`

Try to solve the game with only using those two (it should be do-able). Remember how conditionals are evaluated, and be careful to not accidentally trigger the wrong ones!

You can run the big map by using the command `python run_big.py`

Message me and tell me how many steps your sprite took to win the game! Try to keep it as low as you can!
