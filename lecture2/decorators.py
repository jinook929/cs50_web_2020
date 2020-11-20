def announce(f):
    def wrapper():
        print("About to run the functions...")
        f()
        print("Done with the functions.")
    return wrapper

@announce
def hello():
    print("Hello!")

hello()