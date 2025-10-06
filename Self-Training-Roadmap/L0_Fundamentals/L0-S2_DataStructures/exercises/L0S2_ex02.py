import random
def generate_dictionary():

    name_list=['Alice', 'Bob', 'Charlie', 'David', 'Eva']
    age_list = random.sample(range(20,60), len(name_list))
    
    bio_dict = dict(zip(name_list, age_list))
    # print(bio_dict)

    return bio_dict

def find_maxAge_from_dict(dictt):

    max_age = None
    name_of_max = None

    for name, age in dictt.items():
        if max_age is None or age > max_age:
            max_age = age
            name_of_max = name

    return name_of_max, max_age

def ex02():
    if __name__ == "__main__":
        bio_dict = generate_dictionary()
        print("Generated Dictionary:", bio_dict)
        name, max_age = find_maxAge_from_dict(bio_dict)
        print("Oldest Person:", name, "Age:", max_age)

ex02()
import timeit, sys
bio_dict = generate_dictionary()
print(f"find_maxAge_from_dict: {timeit.timeit('find_maxAge_from_dict(bio_dict)', globals=globals(), number=1):.1e} seconds")
print(f"size of the dict: {sys.getsizeof(bio_dict)} bytes")