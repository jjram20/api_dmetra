#Script to clean database removing completed tasks

"""
Set up script to automate execution

Run crontab -e

Add this line, where script.py should point to this script
*/10 * * * * script.py
"""

import sqlite3

#Connect database
connection = sqlite3.connect("../instance/apidatabase.db")

#Create cursor to execute command in database
cursor = connection.cursor()

#Command to delete completed tasks
cursor.execute("DELETE FROM tasks WHERE completed = True")

#Save changes
connection.commit()