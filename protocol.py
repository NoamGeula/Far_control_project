

LENGTH_FIELD_SIZE = 4
PORT = 8820
#NISAYON PUSH
def check_cmd(cmd):
    """
    
    Check if the command is defined in the protocol, including all parameters
    For example, DELETE c:\work\file.txt is good, but DELETE alone is not
    no need to check here if the file exists
    """
    lst = cmd.split(' ')
    if lst[0] == "DIR" or lst[0] == "DELETE" or lst[0] == "EXECUTE" and len(lst) == 2:
        return True
    elif lst[0] == "TAKE_SCREENSHOT"and len(lst) == 1:
        return True
    elif lst[0] == "COPY" and len(lst) == 3:
        return True
    elif lst[0] == 'EXIT':
        return True
    else:
        return False
    # (3)



def create_msg(data):
    """
    Create a valid protocol message, with length field
    """

    # (4)
    """ for the data = THIS IS A MESSAGE this function will do the following
    calculate the size the message and then find how many digit are in this size
    for example for the data = THIS IS A MESSAGE :
    the length is 17 
    the length of 17 is 2
    those the return value of the function will be 0217THIS IS A MESSAGE
    dont forget to encode the message at the end so it will be in bytes
    """
    x = ''
    oreh = len(data)
    oreh = str(oreh)
    byt = str(len(oreh))
    byt1 = byt.zfill(2)
    y = f'{byt1}{oreh}{data}'
    return y.encode()
    #return "0217THIS IS A MESSAGE".encode()


def get_msg(my_socket):
    """
    Extract message from protocol, without the length field
    If length field does not include a number, returns False, "Error"

    for example : if the message waiting in socket is "0217THIS IS A MESSAGE"
    first we will receive 2 bytes from the socket this will be 
    the length of the message size, now for the above example we will read
    extra 2 letters (according to the number we got on the first two bytes) 
    and it will be 17 which means the message has 17 letters in it
    then we will read these extra 17 letters and will return the text of the message with 
    # the True value    
    """
    
    x = my_socket.recv(2)
    x = x.decode()
    y = my_socket.recv(int(x))
    y = y.decode()
    z = my_socket.recv(int(y))
    z = z.decode()
    # (5)
    return True, z


