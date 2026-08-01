class tes:
    def __init__(self,name,value,idx):
        self.name = name
        self.value = value
        self.idx = idx

    def prt(self):
        print(self, self.name)

x = tes("abc",23,9)
print(x.name, x.value, x.idx)

x.prt()