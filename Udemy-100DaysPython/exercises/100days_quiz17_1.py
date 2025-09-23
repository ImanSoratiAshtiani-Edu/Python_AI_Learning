# a program for exercise on if statement in one line
# this program return index of the list, if you insert the element-value; or it returns the value of the index you insert!

def convert(inp):
    return list[int(inp)] if inp.isdigit() else list.index(inp)
inp= input("insert an index or a letter: ")
list=['a','b','c','d']
print(convert(inp))
