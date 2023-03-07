#Selenium related imports:
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


from time import sleep # for waiting between chats
from os import system, name # for clearing the screen
import configparser

# Counts every time the bot sent a message, will be displayed in the console
message_count = 0

# Accesses the config.ini file
config = configparser.ConfigParser()
config.read('config.ini')

# TOPICS
# checks if Input equals true and if yes gives the user an input entry
if config['TOPICS'].getboolean('Input'):
    topics = str(input("Topics: "))

# if Input is false it uses the topics that were preconfigured by the user 
else:
    topics = config['TOPICS']['Topics']


# Connects to the Firefox webdriver and opens Omegle
driver = webdriver.Firefox()
driver.get('https://www.omegle.com/')


# finds the input box that takes the topics for the chats
bar = driver.find_element(By.CLASS_NAME, 'newtopicinput')

# enters the topics
bar.send_keys(topics)
bar.send_keys(Keys.ENTER)

# Clicks on the chat button to start chatting
driver.find_element(By.ID, "textbtn").click()

"""
Finds all the checkboxes by using the XPath for checkboxes
because the checkboxes for agreeing to the TOS don't have a class or an id
"""
checkboxes = driver.find_elements(By.XPATH,'//input[@type="checkbox"]')

# Clicks on every checkbox
for checkbox in checkboxes:
    # tries because not every checkbox is enabled and disabled checkboxes raise exceptions
    try:
        checkbox.click()
    except Exception:
        # don't do anything if a checkbox is disabled
        pass

""" 
find an input element with the XPath of the specified because the button
doesn't have a tag but it has this value and clicks on it
"""
driver.find_element(By.XPATH,'//input[@value = "Confirm & continue"]').click()

# The message that the bot sends, configured in the config.ini file
Message = config['MESSAGE']['Message']

# waiting time before sending a message and after sending a message, configured in the config.ini file
before = int(config['WAITING']['Before'])
after = int(config['WAITING']['After'])

# Function to clear the console
clear = lambda: system('cls' if name=='nt' else 'clear')

while True:
    
    sleep(before)

    # tries because the text box might have not loaded yet and that will raise an exception
    try:
        # The text box for sending messages
        chatbox = driver.find_element(By.CLASS_NAME, "chatmsg")

        # sends the message
        chatbox.send_keys(Message)
        chatbox.send_keys(Keys.ENTER)

        #clears the console and prints the counting message incremented by 1
        clear()
        message_count+=1
        print(f"Sent {message_count} times")

        sleep(after)

        # The button for disconnecting from a chat and starting a new one
        disconnect_button = driver.find_element(By.CLASS_NAME, "disconnectbtn")

        # clicks on the button 2 times to end the chat and 1 time to start a new one 
        for i in range(3):
            disconnect_button.click()
    except Exception:
        # does nothing so the bot will just try again until he succeeds 
        pass