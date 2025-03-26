class Person: 
    def __init__(self, name, age,city): 
        self.name = "_".join(name.split()).lower()
        self.age = age
        self.city = city