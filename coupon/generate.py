from random import randrange
def generate_code():
    """ 
    
    client needed thousands and this worked well.
    i.e. in shell:
        # now make a file out of all the codes
        codesFileStream = open('codes.csv', 'w')
        for code in codes:
            codesFileStream.write(code +"\n")
            
        codesFileStream.close() 
    
    """
    CODE_LENGTH = 8
    MAX_TRIES = 1024
    CODE_CHARSET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789'

    def code_exists(code):
        return False  # Coupon.objects.filter(code=code).exists()

    loop_num = 0
    unique = False
    while not unique:
        if loop_num < MAX_TRIES:
            code = ''
            for i in xrange(CODE_LENGTH):
                code += CODE_CHARSET[randrange(0, len(CODE_CHARSET))]
            if not code_exists(code):
                unique = True
                return code
        else:
            raise ValueError("Couldn't generate a unique code")
