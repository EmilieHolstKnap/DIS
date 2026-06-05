# DIS Flask Tutorial 2025
Flask tutorial for the Databases and Information Systems 2025 course

# Preliminaries
This repository contains the step-by-step of my hands-on Flask tutorial. 

The starting point is where the actual Flask hands-on starts, but please read all the remarks before, and the recommendations section after.

## Helpful cheatsheets:
It is very useful to know some basic terminal commands.

Here is a very short terminal cheatsheet:

|Command         |Description                           |
|----------------|--------------------------------------| 
|pwd             |Shows present working directory       |
|mkdir *dirname* |Make directory                        |
|cd *dirname*    |Change directory                      |
|cd ..           |Go to parent directory of current dir |
|ls              |List files                            |


And here is a very short git cheatsheet:
|Command       |Description                                            |
|-------------------------------|--------------------------------------| 
|git clone *remote_url*         |clones a git repository               |
|git add *files*                |add files to stage                    |
|git commit -m *commit_message* |commit staged files with message      |
|git push                       |push changes to remote                |
|git pull                       |pulls changes from remote             |

## Learn some basic Python
We will not use very advanced Python features, but please check some [Python tutorials](https://docs.python.org/3/tutorial/).

Make sure you learn things like variables, functions, indentation, lists, maps (dictionaries), if-then-else, for loops, class (OO programming), and how to import libraries.


## Prepare your computer for the hands-on
This is a Flask tutorial, which will require Python and PostgreSQL installed on your computer.

Please refer to the [official Python website](https://www.python.org/downloads/) on how to install it. 

Any version of Python greater than 3 should be fine.

On Windows, make sure to have "add python.exe to PATH" marked during the installation.

You probably already did this, but make sure you have PostgreSQL and PGAdmin installed.

Install a text editor for programming. I recommend [VSCode](https://code.visualstudio.com/) and installing the VSCode Python extension.

Git is a requirement for this project. So make sure you have it [installed](https://git-scm.com/downloads).

# Starting point (hands-on)
This is where, during the lecture, I will start the hands-on.

Please follow this from top to bottom, don't skip any point, and take into consideration the Linux/MacOS/Windows differences.

Note: I only have access to Linux (Ubuntu/NixOS) and Windows 11.

Please let me know issues regarding MacOS and older versions of Windows.

## Minimal Flask App
Our app is just a vary basic TODO list.
We will only be able to add and visualize our TODOs.

All the instructions here are a compilation of the [official Flask website](https://flask.palletsprojects.com/en/stable/) with some additional things.
Any information missing about Flask here is probably there.

Let's open a terminal (use PowerShell on Windows) and navigate to a directory where we want to place our project:
```shell
cd Documents
```
Create a folder with the name of your project:
```shel
mkdir minimal
```
Open the just-created folder:
```shell
cd minimal
```
We need to start a Python virtual environment.

Please read the [official documentation](https://flask.palletsprojects.com/en/stable/installation/#virtual-environments) to understand what this is about. 
First, let's bootstrap the virtual environment:
```shell
 python -m venv .venv
```
Next, we need to activate the virtual environment.

There is an operating system quirk here!

On Linux/MacOS, we just do:
```shell
. .venv/bin/activate
```
But on Windows, we need to change some execution policies first:
```shell
Set-ExecutionPolicy Unrestricted -Scope Process
```
And then we can activate with a different command:
```shell
.venv\Scripts\activate
```
Note: Every time you open a new terminal instance, you will need to activate the virtual environment again. 

On Windows, this also includes doing the change of execution policies command again.

From here we are ready to install Python libraries!

We first start with Flask. It is easy:
```shell
pip install flask
```
How about we use the same code from the [official Flask quick start](https://flask.palletsprojects.com/en/stable/quickstart/#a-minimal-application)?

I will be assuming you are using VSCode as your text editor.

From the same terminal instance we have been using so far, open VSCode, passing the name of the file we will be creating:
```shell
code app.py
```
Paste the following code into the file, and save it:
```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
```
Now we can start the Flask webserver:
```shell
flask run --debug
```
Open a web browser and navigate to [`http://127.0.0.1:5000`](http://127.0.0.1:5000).

Congratulations, you have started your very minimal web application.

Press `ctrl+c` to stop the Flask server.

### Adding Templates to the Minimal Flask App
Our example so far has no HTML code, it just prints some text as a webpage.

As you notice, Flask did quite a lot already, it converted a Python string into a basic HTML page.

The main magic of web frameworks like Flask is the convenient way of generating dynamic webpages for us.
In Flask, part of this magic happens with templates.

So here is a key Flask concept:

> Templates are files that contain static data as well as placeholders for dynamic data.
In our case, the templates will be HTML files containing the placeholders for our dynamic data.

Let's create a new folder called templates:
``` shell
mkdir templates
```

Inside of this folder we will a file: 

``` shell
code templates/todo.html
```
we paste the following there:
```html
<!doctype html>
<title>Todo:</title>

<form method="POST" action="/todo">
    <input type="text" name="new_todo" placeholder="Add another todo here" class="form-input" required>
    <input type="submit" value="Add" class="btn">
</form>

{% for todo in todos %}
    <li><a>{{ todo }}</a></li>
{% endfor %}
```
This is [Jinja2](https://jinja.palletsprojects.com/en/stable/) code: an extended HTML programming language. 

Inside of `{% %}` we have Jinja2 commands, and inside of `{{  }}` we print Python values as HTML.
The interesting bit here is the `form` with a `POST` method, which generates a HTTP `POST` request that we can capture in the Python code later.
The next block of code just lists whatever we will have in the `todo` variable that is passed to this template.

### Adding a SQLite Database to the Minimal Flask App
SQLite is a quick-and-dirty alternative to Postgres.

It is a SQL database, but it is not a dedicated database server.

Therefore, it makes the application setup easier, as we don't need to have a separate program running. 
In the real world, people use things like Postgres because it has way better multi-core performance, and it scales with more replicas. 

SQLite is just a toy database tool, but it is enough for our goals in this minimal example. 

In the MVC Flask app, we will use Postgres.

Let's edit the `app.py` file again.

Replace all its content with the code in [`minimal/app.py`](https://github.com/rafaelcgs10/dis2025/blob/main/minimal/app.py).

Read all the comments in that file, and when you are done come back to this point in the tutorial.

You can run the app again by following the same instructions from this [sub-section](https://github.com/rafaelcgs10/dis2025/blob/main/README.md#minimal-flask-app).

But this time go to [`http://127.0.0.1:5000/todo`](http://127.0.0.1:5000/todo).

Our app is very basic: it only allow us to add and list TODOs.

But we have covered some import concepts: templates, database interactions, and HTTP requests. 

## Minimal MVC Flask app
Our app is very simple (it only has two small files), which is something great for learning purposes.
If your project can be executed in very few hundred lines of code, I don't think it is a big sin to keep everything in a single file.
But if your project has multiple entities, complex algorithms, maybe even a login system, then having everything together is not the best idea.
Things will get de-organized if we have thousands of lines of code in a single file. 
The [Clean Code](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882) book has some decent general rules. [Here is a good summary of them](https://gist.github.com/wojteklu/73c6914cc446146b8b533c0988cf8d29).

The Model View Controller is a very common pattern on how to organize a web application. Let's recall what each thing is:
* Model: The internal representation of the information 
* View: The interface for the user
* Controller: Links model and view

To justify using MVC, we will increment the TODO list app with categories. We will have two entities: TODO and Categories.
Naturally, we will have their respective models, views, and controllers.

You've already learned how to create folders and files using the terminal.
You can just manually reproduce the file structure in the folder `minimal_mvc`. Or you can use the `git clone` command to get a local copy of this repository.
You can run the webserver as usual, and browse to [`http://127.0.0.1:5000/todo`](http://127.0.0.1:5000/todo) again.

At this point, you should try to investigate how things work on your own.
The project is still minimal.
Some interesting places to look are the `models`  directory, where we define the classes of the models, and we make all the interactions with the database.
The `templates` directory is just a bit more sophisticated.
The controllers glue the models with their views.
The routes there are registered differently; we are using Flask's [Blueprint](https://flask.palletsprojects.com/en/stable/tutorial/views/#create-a-blueprint) feature to specify the route.
Later, we just registered the blueprints from both controllers in our old `app.py`, which is now much smaller.

## Switching to PostgreSQL 
Starting from our last MVC version, we can easily switch from SQLite to PostgresSQL.
All the code we need is in the `minimal_mvc_pg` folder.
The main changes occurred in the `database.py` file, and in the models.
SQLite and PostgresSQL have almost the same SQL language, and their Python libraries also have minor differences in usage.
Open those files to understand the changes.

One important difference now is that the `psycopg2` library requires some system libraries from the PostgresSQL installation.
Hence, not having PostgresSQL installed will make the installation `psycopg2` fail.
This is the point where you need to have PostgresSQL, and PGAdmin already installed.
On top of that, on Windows, there is another quirk: `psycopg2` requires some MSVC libraries.
For Windows users follow these additional instructions:

1. Download and install [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/).
2. Using Microsoft C++ Build Tools, install MSVC v140 in Individual components (It is kinda ridiculous to install such a huge package just because of this).

Now we can install `psycopg2`.
Before, with flask, we did `pip install flask`. But as we add new libraries manually install each dependency will not scale.
We now use a special file to list our Python dependencies.
This is the `pyproject.toml` file. If you look into this file, you will notice it has the `flask` and the `psycopg2` dependencies.
The famous Python `requirements.txt` is an old school way of doing something similar, but we should keep up with times.

We need to the same setup as before with the Python virtual environment, but this time we install all the dependencies with the command

``` shell
pip install -e .
```

Before we can run our app, we need to make sure that we can connect to PostgresQL.
The first step is to create a new database named `todo` using PGAdmin.
In PGAdmin, right click on top of your connected server, and click: Create -> Database.
Just name the database as `todo`, and save it.

Open the `database.py` file, and update the database configuration to match your local settings.
In particular, make sure that you set the proper user and password there.

Just run the app as usual:

``` shell
flask run --debug
```

# Recommendations (extras):
None of these are project requirements but rather recommendations of things to learn.

These recommendations will make your application closer to a real-world system. You may need to know some of these things for your future job, so why not take this chance to learn them?
### Please focus on meeting the hard requirements of the project (check lecture 0 slides) before doing any "extras".

What to learn (sorted by priority):
1. Use docker + docker-compose: You are writing software on your computer, which has certain system libraries, in certain versions. How can you ensure the rest of your team can use the development in the same environment as you? One way is to use [Docker](https://www.docker.com/). Docker is not a virtual machine, it is a container solution based on a Linux kernel feature called [Cgroups](https://en.wikipedia.org/wiki/Cgroups). You can use Docker on Windows and MacOS, but for both, the Docker installation relies on virtualization.
   
  * To install Docker on your Linux computer, refer to your distribution instructions. For example, Ubuntu users can follow [this](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository).
  * To install Docker on your Windows computer, you can follow [these instructions](https://docs.docker.com/desktop/setup/install/windows-install/). Beware that you need to 1. activate hardware virtualization in the BIOS/UEFI of your computer; and 2. enable wsl on Windows.
  * To install Docker on your MacOS computer, refer to [this](https://docs.docker.com/desktop/setup/install/mac-install/).
  
  In the `minimal_mvc_pg` folder, there are an usual docker + docker-compose + entrypoint setup.
  
  Read the comments in those files.
  
  To execute the dockerized version of the app, just raise it with the docker-compose command:
  
``` shell
docker-compose up
```

Tip: use [lazydocker](https://github.com/jesseduffield/lazydocker) to manage your docker containers.

2. Learn some CSS: CSS is how you will make your app look cool. There are many resources out there on how to use CSS.
3. Implement unit tests: Unit tests are meant to test certain functionalities in isolation. They usually don't connect to separate services and are very minimalistic. The main value of unit tests is confidence when code changes: changing code may break unit tests, which informs what behavior has changed. Unit tests can also work as a form of documenting the functionality of certain blocks of code. Whatever programming language you choose to use, there are probably at least a few unit test frameworks for it. For example, [pytest](https://docs.pytest.org/) is a good unit test framework for Python.
4. Deploy your application somewhere: There are many ways to deploy an application to some cloud infrastructure.
One easy way is to use services like [Fly](https://fly.io), and [Render](https://render.com). Those are some with web server free tiers, and a PostgreSQL server for free too. Heroku used to be a very good one, but they don't have free tiers anymore.
