import sys
from time import sleep

if __name__ == '__main__':
    sleep(5)
    print('Este es un valor de retorno')
    sys.stderr.write('Este es un valor de error')
        