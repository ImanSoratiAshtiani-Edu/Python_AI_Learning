import pdb
pdb.set_trace()
class MyList:
    def __init__(self, items):
        self.data = items

    def __getitem__(self, index):

        print(f"GET item at index {index}")
        return self.data[index]

    def __setitem__(self, index, value):
        print(f"SET item at index {index} to {value}")
        self.data[index] = value

    def __delitem__(self, index):
        print(f"DELETE item at index {index}")
        del self.data[index]
lst = MyList(["iman", "reza", "ali"])

print(lst[0])       # calls __getitem__
lst[1] = "hossein"  # calls __setitem__
del lst[2]          # calls __delitem__
