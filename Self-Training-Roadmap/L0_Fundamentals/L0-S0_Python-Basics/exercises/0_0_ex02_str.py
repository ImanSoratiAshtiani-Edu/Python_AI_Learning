import datetime

name = "iman"
grade = 19
year = datetime.datetime.now().year

bio = {"name": name, "year": year, "grade": 19}

print(f"Hello {name}, your grade in {year} is {grade}.")
print("Hello {}, your grade in {} is {}.".format(name, year, grade))
print("Hello {a}, your grade in {b} is {c}.".format(a=name, b=year, c=grade))
print("Hello {name}, your grade in {year} is {grade}.".format_map(bio))