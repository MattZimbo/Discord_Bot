import os

DEBUG_ENABLED = False

'''
Default Debug print line
'''
def Debug(*args, **kwargs):
    if DEBUG_ENABLED:
        print("[DEBUG]", *args, **kwargs)

''' 
Setting Global Debug state
'''
def set_debug(state: bool):
    global DEBUG_ENABLED
    DEBUG_ENABLED = state