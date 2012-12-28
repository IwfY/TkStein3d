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

def mixColors(colorTuple1, colorTuple2, amount):
    '''mix two colors
    
    amount is a value from 0.0 to 1.0 indicating the amount of the second color
    in the result'''
    r1, g1, b1 = colorTuple1
    r2, g2, b2 = colorTuple2
    
    r = r1 * (1.0 - amount) + r2 * amount
    g = g1 * (1.0 - amount) + g2 * amount
    b = b1 * (1.0 - amount) + b2 * amount
    
    return (r, g, b)
