from datetime import datetime, timedelta
from time import sleep

def runAndWait(function, duration):
    '''run a function and wait until its given quota runs out
    
    @param function:function function to be called
    @param duration:int duration of quota in milliseconds
    '''
    stop = datetime.now() + \
                   timedelta(milliseconds=duration)
            
    function()
            
    remaining = stop - datetime.now()
    if remaining.days < 0:  # input processing needed too long
        remaining = -1
    else:
        remaining = round(remaining.microseconds / 1000000, 3)
    if remaining > 0:
        sleep(remaining)