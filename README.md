ABOUT: MY little solution with heart, for you
=========================

- [Pre-words](#pre-words)
- [How-to](#how-to)
    * [Install](#install)
        + [Structure](#structure)
        + [Preparation](#preparation)
    * [Run](#run)
        + [Step 1. (exercise)](#step-1--exercise-)
        + [Step 2. (exercise)](#step-2--exercise-)
- [Testcases](#testcases)
    * [Run](#run-1)
- [Post-words](#post-words)
- [Tasks DONE](#tasks-done)
- [Optional(s)](#optional-s-)
    * [Step 3.](#step-3)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with
markdown-toc</a></i></small>

Pre-words
=========
The assessment was a pretty comprehensive task, although, I think it's a bit too long for such an interview, which could
take up to more than 12hrs. So that's the main reason You won't find every task ready, but of course, was a great
opportunity to meet with a fully new regex parser. At the very first time was struggling with it, but when I felt how
should I handle different situations based on their docs examples, was more easy. I do love (if we are at the love
stories) the raw regexps, but I also do know that not everyone likes at, but hates it :P.

You know: `Me loves RE but He hates RE.`


How-to
======
Here you can find the *user-manual* for the installing and running phases of this tool

Install
------

**TAKE CARE:** For every step I'll use Windows 10 machine.

### Structure

First thing first after unzipping the file sent via e-mail is to meet the structure. Right under the root folder of the
source files:

* _input/_ -> contains the only input (feel free to add as much as you want)
* _notebooks/_ -> contains the only notebook required to have a client which communicates to the Flask server
* _tests/_ -> contains the unittests
* _thelovegeometry/_ -> its the module which parses the love stories
* _thelovegeometry_service/_ -> its the module to serve HTTP requests via the help of the Flask API
* _requirements.txt_ -> contains a list of dependencies
* other project specific files

### Preparation

Now we should create a virtual environment. This step is optional, but strongly recommended, to have an isolated
environment for this project (but if you're okay I if disturb your little hood, there you go... :D).

Check which version do you have assigned to the **py** command, for that you will need a PowerShell opened right where
all the source files are:

```shell
> py -0
Installed Pythons found by C:\WINDOWS\py.exe Launcher for Windows
 -3.10-64 *
 -3.9-64
 -3.8-64
```

If the star is near a version at least _3.6_, then you should be ok!
For the development, I've been using _Py 3.8.5_.

Let's create that venv:
`py -3.8 -m virtualenv venv`

Activate that:
`venv\Scripts\Activate.ps1`

Now let's install all the dependencies the project has:
`pip install -r requirements.txt`

As it is a smaller project, and is not the case to include a setup[.cfg|.py] file to differentiate between the
requirements, I've chosen this way of gathering the requirements.

**Happiness**. We are ready with the very first step. :smile:


Run
---
From the root of the project folder, type in the already activated _PowerShell_ window:

* For checking the usage of the tool:

```shell
>python -m thelovegeometry -h
2021-09-14 16:31:20,917:INFO:Logger setup is done
usage: python -m thelovegeometry [-h] [-f FILE]

The tool is able to parse LOVE stories full of drama, based on the PyPeg2 module

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  path to the input file

```

### Step 1. (exercise)

* Run the parser as a module:
  `python -m thelovegeometry -f input/thelovegeometry.input`

### Step 2. (exercise)

* Run the Flask API:
  `python -m thelovegeometry_service.run`

* Run the Jupiter:
  `jupyter notebook`
* Open the notebook file at: **notebooks/client_inside_a_notebook.ipynb**
* Play after your taste with it

Testcases
=========
Please find every testcase under the **./tests/** folder.

I'am using PyTest since a while, here so.

To be able to run those, first the dependencies should have been installed. If it is already done, this step should be
skipped now.

For this, execute all the steps written under the [Preparation](#preparation) section.

Run
---

Simply run the **pytest** module in the root folder of the project. As it has its own configuration file, does not
require any options:
`pytest`

Post-words
==========
Although there are a few things not polished for the ultimate better as time is important for both of us, and this is
normal I think, as we all humans. Just like who wrote the guidelines: contains a few mistakes/typos, like the one from
the output structure example (`'D': { 'hates': 'A' }`, where *A* is not inside a list), but of course, I've tried to be
as close as I could to the description.


Tasks DONE
==========

- [x] **1**
- [x] **2**
- [x] _3_
- [ ] _4_
- [ ] _5_

Optional(s)
===========

Step 3.
-------

The validator is being created inside the Parser module. Of course, it should apply a pattern which enables the
open-close principle, to be flexible in terms of validations in the near future.

The choice was pretty easy: that's the best place as of now to be close enough, but NOT part of (neither the Flask API -
as I think it should not contain that business logic). One more thing: this way we are disabling the real time check
ability, but this is known, and was not the requirement now.

It behaves of course in a way to be optional if the user wants to validate the parsed love story or not. Returns a List
of messages by each love state, if any of the following error happens:

* Loving and hating at once the same person or persons if multiple
* Somebody loves and/or hates itself
* Somebody loves and/or hates somebody (even itself) multiple times

For checking those _reports_ just run the module itself.
`validate_and_print_error_messages_of_love_statements(...)` function calls the validation within the **__main__.py**.