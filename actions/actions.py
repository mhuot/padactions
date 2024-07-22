def lightson(DEBUG=False, DRYRUN=False):
    if DEBUG or DRYRUN:
        print("DEBUG: lightson")
    else:
        print("DOING lightson")

def lightsoff(DEBUG=False, DRYRUN=False):
    if DEBUG or DRYRUN:
        print("DEBUG: lightsoff")
    else:
        print("DOING lightsoff")
