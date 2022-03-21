class Member:
    def __init__(self, name, age, premium=False, activated=True, id = None):
        self.name = name
        self.age = age
        self.premium = premium
        self.activated = activated
        self.id = id