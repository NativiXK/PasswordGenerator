from menu import Menu

menu = Menu()

if __name__ == "__main__":
    try:
        menu.run()
    except Exception as msg:
        print(msg.with_traceback())
        input()
