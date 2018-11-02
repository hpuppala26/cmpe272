def roomvalidate(username,roomname):
    difference = roomname.replace(username,"",1)
    reconstructed = "".join(sorted([username,difference]))
    if roomname == reconstructed:
        return True
    else:
        return False    
