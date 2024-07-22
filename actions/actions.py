'''This is an example module of actions to be performed'''

def lightson(debug=False, dryrun=False):
    '''Example for a lights on action'''
    if debug or dryrun:
        print("DEBUG: lightson")
    else:
        print("DOING lightson")

def lightsoff(debug=False, dryrun=False):
    '''Example for a lights off action'''
    if debug or dryrun:
        print("DEBUG: lightsoff")
    else:
        print("DOING lightsoff")
