def announce(function):
    def wrapper():
        print 'Entering function', function.__name__
        function()
        print 'Leaving function', function.__name__
    return wrapper()

if __name__ == "__main__":
    announce()
