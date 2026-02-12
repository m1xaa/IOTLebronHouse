class SimLCD:

    def __init__(self):
        pass

    def clear(self):
        print("[LCD] CLEAR")

    def display(self, line1, line2):
        print("------ LCD ------")
        print(line1)
        print(line2)
        print("-----------------")

    def cleanup(self):
        self.clear()
