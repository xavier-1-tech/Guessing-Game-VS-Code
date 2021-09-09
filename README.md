# Guessing-Game-VS-Code

A simple Number Guessing Game web application which provides that will be deployed to AWS Elastic Beanstalk using jenkins. It will have the following functionality:  
- The Computer randomly selects a number between 1 and 10  
- The player can input a number between 1 and 10 as a guess  
- The game allows for 3 attempts before game over 
- Refresh button to restart the app (still has bugs)  

The project makes use of Python3, Flask, SQLite, HTML5, CSS, JavaScript Bootstrap and JQuery.

## Why a guessing game?

I felt that doing an object oriented guessing game app and combining it with the flask microframework was the best way to keep what I had learned from python fresh in my mind through practice.

## Getting Started

git clone https://github.com/xavier-1-tech/Guessing-Game.git && cd guess_app

##### Create virtualenv and activate

pip install -r requirements.txt

Linux & Mac:
export FLASK_APP=app.py  
flask run  #flask run --host=0.0.0.0 (if require server to be publicly accessible)  

Windows:
set FLASK_APP=app.py
flask run  #flask run --host=0.0.0.0 (if require server to be publicly accessible) 

Navigate to: http://localhost:5000/

##### The code

First we must import the modules that we will be working with in flask:
```python
import random

from flask import Flask, render_template, request

application = app = Flask(__name__)
```
- Importing flask allows us to utilize features of the microframework.
- Importing the render_template gives the web app the ability to use html, css and other web based scripts and code.
- The Flask request object contains the data that the app needs to make HTTP request to other sites. Usually used for APIs.

Now we need to set up app to be communicate with AWS Elastic BeanStalk
```python
application = app = Flask(__name__)
```
For some reason, AWSEB seems to only understand your application if its py file is title Application.py and the route are designated as `application.route` instead of `app.route`. By default flask uses `app.route` and depend on how complex your web app is, you will have a lot of `app.routes`. A quick way to designate `application.route` is to simply create a variable that holds the value `app = Flask(__name__)` python will then rationalize that every `app.route` means `application.route` and it will function accordingly.

Now we define of our class and functions:

The class section:
```python
class GuessGame:
    def __init__( self ):
        self.comp_num = random.randint(1, 10)
        self.counter = 0
        self.game_over = False
```

By creating the class `GuessGame` we can now house the main variables.
- `self.comp_num = random.randint(1, 10)` is the variable responsible for the random number that the computer will pick.
- `elf.counter = 0` is the variable responsible for counting the players attempts.
- `self.game_over = False` is the variable responsible for checking to see if the player has failed or won.

The function section:
```python
def increment_goes( self ):
        self.counter += 1

    def check_game_over( self, the_input ):
        # checks for whether the game is finished
        if the_input == self.comp_num or self.counter == 3:
            self.game_over = True
        if the_input == self.comp_num:
            return "You Won"
        if self.counter == 3:
            return "Maximum Guess limit: 3"
        return ""
``` 

- The first function named `increment_goes( self )` will house the code that will allow the counter to count up by 1.
- The second function `check_game_over( self, the_input )` will house the code that will run the game essentially.
  - The if state code set essentially checks for whether the user guessed the correct number or whether the user has reached the guess attempt limit. This is represented by this code line here `if the_input == self.comp_num or self.counter == 3:` If either of those statements end up being true, game over will be triggered. This code line represents that `self.game_over = True`
  - The next if statement `if the_input == self.comp_num:` controls the end result if the user guesses the right number. `return "You Won"` triggers the special win page when the if statement is fulfiled
  - The last if statement `if self.counter == 3:` handles the maximum counter limit. It is current set to 3 but it can be change by changing the figure in the statement. `return "Maximum Guess limit: 3"` triggers the special limit page when the if statement is fulfiled. 


Condesning the functions into gloabal variables:
```python
global game
game = GuessGame()
```
- A global variable is a variable that can be accessed from anywhere, from any function. By creating the global variable `game` and making it hold the class `GuessGame()` (this is represented by `game = GuessGame()`) we are essentially making the `GuessGame()` class global and accessible from anywhere.
- We do this so that we can make setting up out `app.route` functionality easier.


Setting up the `app.route`s
```python
@app.route("/", methods=['GET', 'POST'])
```
- Flask has different methods to handle http requests. The aim of requests are to allow clients to access resource on the server. The current requests available to flask are:

Request  | Purpose
------------- | -------------
GET  | The most common method. A GET message is send, and the server returns data
POST  | Used to send HTML form data to the server. The data received by the POST method is not cached by the server.
HEAD  | Same as GET method, but no response body.
PUT  | 	Replace all current representations of the target resource with uploaded content.
DELETE  | Deletes all current representations of the target resource given by the URL.

`@app.route("/", methods=['GET', 'POST'])`:
- `@app.route()` Represents app routing and it is used to map the specific URL with the associated function that is intended to perform some task.
- `"/"` is the default symbol that reprensents a flask app's homepage.
- `methods=['GET', 'POST'])` allows the home page to have the ability to post data and to get data.

This portion of the code creates the index fuction, which will link the game functions to the homepage.
```python
def index():
    global game
    message = ""
```
- The `index()` function houses the global variable `game` and the empty string `message` variable.
- `""` represent and empty string. Normally this is used to add an empty line but in this case it is user to represent a replaceable string element. `message = ""` represents that.

The portions of the code below contain the if states and request methods that will reference the functions the `GuessGame()` class by using the `game` variable.
```python
if request.method == 'POST':
    game.increment_goes()
    form = request.form
    user_guess = int(form["guess"])
```
- `if request.method == 'POST':` is an if statement that is checking to see if the user has submitted a request to send data.
- `game.increment_goes()` is referencing the `increment_goes()` function from the `GuessGame()` class to start the attempt counter check.
- `form = request.form` is linking the post method to a form submition as the data input.
- `user_guess = int(form["guess"])` is ensuring that the data input or user guess is an integer and that it is entered via the form.

```python    
    if game.comp_num == user_guess:
        message = "Well done. You got it right!"
    elif game.comp_num > user_guess:
        message = "Too Low"
    else:
        message = "Too High"
    result = game.check_game_over(user_guess)
```
- `if game.comp_num == user_guess:` this if statement is checking to see if the number the user input in the form is equal to the the random number the computer selected. if that statement is true, `message = "Well done. You got it right!"` is triggered. This will display some text saying *Well done. You got it right!*
- `elif game.comp_num > user_guess:` this if statement is checking to see if the number the user input in the form is lower than the number the computer selected. If that check ends up being true then `message = "Too Low"` is passed. This is a way to guide the user or player to getting right number.
- `else: message = "Too High"` this statement checks to see if the number the user input in the form is higher than the number the computer selected. If that check ends up being true then `message = "Too High"` is passed. This is a way to guide the user or player to getting right number.
- `result = game.check_game_over(user_guess)` This references the function `check_game_over()` in the `GuessGame` class.

```python
    if game.check_game_over(user_guess):
       return render_template("game-over.html", message=result)
    return render_template("index.html", message=message)
```
- `if game.check_game_over(user_guess):` this statement is checking to see if any output was produced from the referenced `check_game_over()` function. If an outcome has been produced then `return render_template("game-over.html", message=result)` is called.
- `return render_template()` produces the html, CSS design for the app page.
- `"game-over.html"` is the name of the html file being referenced to be displayed in the browser.
- `message=result` displays the specific message text for the outcome produced.

##### Referencing The Design Templates

To achieve the look and feel, html and CSS were used to stlye the homepage and the game-over page.
You can design it however you wish within reason of the functionality of the app you are creating, but please note:
1. In-order for flask to see your html templates, they must be placed in a folder/directory title *templates* in your project folder/directory
2. In-order for flask to see your CSS styles, JavaScript code and other scripts, they must be placed in a folder/directory title *static* in your project folder/directory
    -When linking to the css in your html file, please ensure that it looks something link this: `<link href="static/css/nameoffile.css" rel="stylesheet" type="text/css">`. A reference to thhe Static folder/directory must be present.
    
After you have style the page to your liking, your must create the elements that would perform the function of your web app. This depends on the type of app being created, but in this case, we need:

On the Homepage:
1. A form input field
2. A form submit button
3. A paragraph element to display information

When creating the form element and the subsequent input field and button, ensure the follow are done:
- Add the `method = 'POST'` inside the form opening tag. e.g. `<form method = 'POST'>`
- Ensure that the name of the input field is the same as the input string designated inside the `user_guess` variable in the code. In this case that would be `guess`. It should look like this `<input name = "guess" type="text"/>` to reference this `user_guess = int(form["guess"])`
- Ensure that the value of the form submit button also references the input string designated inside the `user_guess` variable in the code, which would be `guess`. Implementation below:

```html
 <form method = 'POST' id="email-form" name="email-form" data-name="Email Form" class="form">
          <input name = "guess" type="text" class="field w-input" maxlength="256" data-name="guess" placeholder="" id="guess"/>
          <input type="submit" value="guess" data-wait="Please wait..." class="button w-button"/>
        </form>
```

The paragraph element will be autofilled by various message strings dependant on the situation from the code. This done by placeing the `{{ message }}` between opening and closing paragraph tags `<p></p>`.
`{{ }}` allow for value substitution of variable inside of it during template rendering. In our case, `message` is the variable being substituted. The follow messages can be displayed
- Too High
- Too Low
- Well done. You got it right!

```html
      <p class="note-para">
          {{ message }}
      </p>
```

On the Game-over page:
1. A paragraph element to display information
2. Button to reload the game (work in progress)

```html
 <p class="game-over">
        {{ message }}
      </p>
```

## Issues I faced when deploying it?

### Issue 1

- **Issue:** When attempting to deploy the app to the vritual cloud environment on the AWS Elastic Beanstalk, the venv would degrade and the deployment would fail.
- **Cause:** The program I used to build this app was Pycharm. Pycharm automatically creates a virtual environment for each project and this inturn has many Pycharm link files attached to it. When I uploaded those files to my Github repo, and tried to deploy them through Jenkins, the Pycharm made venv and extra files clashed the AWS Elastic Beanstalk venv, causing it to fail.
- **Solution** I rebuilt the app using VS Code. This new set of file had no exccess program specific files and was able to be successfully deployed.

## Authors

**Xavier Henry**

## License

This project is licensed under the MIT License
