import random

TEXT = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer consequat nec arcu a commodo. Fusce vitae libero sem. 
Sed auctor ligula purus, non cursus neque suscipit a. Sed quis ligula scelerisque, efficitur eros nec, euismod diam. 
Mauris et libero eu ex porta consequat. Nullam commodo auctor gravida. Nullam eros neque, commodo quis risus at, mollis 
accumsan libero. Quisque pellentesque lobortis felis nec maximus. Suspendisse potenti. Sed vitae tincidunt nunc, sed 
porttitor nulla. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec non elementum est. Vestibulum dapibus 
convallis diam eget faucibus. Aenean in felis ac lectus auctor volutpat. Vestibulum dignissim mollis pulvinar. Nunc 
quis ultrices dui. 
"""

WORDS = TEXT.replace('.', '').split()


def get_random_text(num_words):
    words = (''.join(random.choice(WORDS) + ' ' for _ in range(num_words))).strip().strip(',').capitalize() + '.'
    return words
