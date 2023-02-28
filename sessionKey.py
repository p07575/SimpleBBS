from random import choice
import string

def GenPasswd2(length=8, chars=string.ascii_letters + string.digits):
    return ''.join([choice(chars) for i in range(length)])

# GenPasswd2(8,string.digits) + GenPasswd2(15,string.ascii_letters)