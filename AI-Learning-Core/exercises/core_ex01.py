import random
def core_ex01():
    lista =  random.sample(range(100, 200) , 10)
    summ=0
    for element in lista:
        summ +=element
    return lista, summ