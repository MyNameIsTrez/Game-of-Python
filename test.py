import time

from test_obj import Test_obj

def setup():
    test_obj = Test_obj()

    test_obj.calc()
    time.sleep(3)
    return test_obj

def main():
    test_obj = setup()
    
    while True:
        test_obj.calc()
        time.sleep(3)

if __name__ == '__main__':
    main()
