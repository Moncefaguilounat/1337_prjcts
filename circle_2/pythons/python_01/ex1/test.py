class   Message:
    def __init__(self, sender, receiver, contenue, date):
        self.sender = sender
        self.receiver = receiver
        self.contenue = contenue
        self.date = date


m1 = Message("moncef", "mshishto", "ilvy", "this morning")
m2 = Message("mshishto", "moncef", "ilvy more", "this evening")
m3 = Message("moncef", "mshishto", "marry me", "this evening")
print(f"m1 details are : {m1.sender} sent {m1.date} to {m1.receiver} the message {m1.contenue}")
print(f"m2 details are : {m2.sender} sent {m2.date} to {m2.receiver} the message {m2.contenue}")
print(f"m3 details are : {m3.sender} sent {m3.date} to {m3.receiver} the message {m3.contenue}")

