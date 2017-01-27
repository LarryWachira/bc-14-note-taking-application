#Andela Kenya boot camp XIV project:
##Note taking command line application ('PyNote')

PyNote is a command line note taking application with a lot of essential features written in Python.
You can store notes, view them, search them and even backup them up locally or on firebase.
Here's a usage list highlighting all of it's features:

##Usage:
1. PyNote create '<note_content>...'
2. PyNote view '<note_id>'
3. PyNote delete '<note_id>'
4. PyNote search '<query_string>...' [--limit=N]
5. PyNote list [--limit=N]
6. *PyNote sync
7. PyNote import
8. PyNote export
9. PyNote help

Features that have require arguments of one type or another are indicated in angle brackets while optional arguments
are enclosed in square brackets.

--------------------------------------------------------

##Installation
The app a number of dependencies as detailed in the `requirements.txt`. To run it, you'll need to install [Python 3.6](http://python.org) from Python's website and setup a virtual environment as illustrated [here](http://docs.python-guide.org/en/latest/dev/virtualenvs/). Dependencies that are built into Python have not been included.

The last and final step will be to install the dependencies by typing `pip install -r requirements.txt`

With that done. All you need now is to clone the repo and run `python app.py -i` in your command line to test out the app.

--------------------------------------------------------

Note: The sync command is currently disabled due to a bug that breaks the exit command
