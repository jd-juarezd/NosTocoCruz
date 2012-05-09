from django.db import models

class Notifications():
    def __init__(self, message, buttonNeeded=False, button=""):
        self.message = message
        if (buttonNeeded):
            self.buttonNeeded = True
            self.button = button
        else:
            self.buttonNeeded = False
            self.button = ""
    
    def __unicode__(self):
        return self.message
