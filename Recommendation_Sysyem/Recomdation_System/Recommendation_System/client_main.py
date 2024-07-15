from client.client import Client

if __name__ == "__main__":
    client = Client('localhost', 12346)
    if client.login_handler.login():
        client.main_loop()
    else:
        print("Exiting the program due to failed login.")
