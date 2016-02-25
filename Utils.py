import os

def run(name='test1.py'):
    filename = os.getcwd() + name
    exec(compile(open(filename).read(), filename, 'exec'))
