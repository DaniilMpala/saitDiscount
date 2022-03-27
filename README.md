# Discounts Web application

The discount aggregator web site allows customers to choose the product they want for the minimum price at the nearest store.
We will use RestApi django + ReactJs to develop the site

## Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/DaniilMpala/saitDiscount.git
$ cd saitDiscount
```

Installing required virtual enviroment packages (if not installed):

Linux/Mac

```sh
$ pip install virtualenv virtualenvwrapper
```

Windows

```sh
$ pip install virtualenv virtualenvwrapper-win
```

Create a virtual environment to install dependencies in and activate it:

Linux/Mac

```sh
$ virtualenv venv
$ source venv/bin/activate
```

Windows

```sh
$ virtualenv venv
$ source venv/Scripts/activate
```

Installing required setup packages (if not installed):

```sh
$ pip3 install sphinx setuptools
$ python -m pip install --upgrade pip
```

Then install the dependencies package:

```sh
(venv)$ cd discountsite
(venv)$ pip install -e .
```
Note the `(venv)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment set up by `virtualenv`.

Once `pip` has finished downloading the dependencies:
```sh
(venv)$ manage.py runserver
```
And navigate to `http://127.0.0.1:8000/`.
