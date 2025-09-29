def e1():
    # creare tre variabili
    nome = input("insert the name: ")
    age = int(input("insert the age: "))
    city = input("insert the city: ")
    # creare la tupla:
    persona = (nome.capitalize(), age, city.capitalize())
    print(persona)
def e2():
    # scambio valori con variabili:
    a = 13
    b = 10
    print("before: ","a:",a,"b:",b)
    a, b = b, a
    print("after: ","a:",a,"b:",b)
def e3():
    ## verifica se elemento è presente nella tuple
    frutti = ("kiwi", "banana", "mela")
    frutto = input("inserisci frutto da cercare: ")
    # verifichiamo appartenenza
    if frutto in frutti:
        print(f"{frutto} è presente in {frutti}")
    else:
        print(f"{frutto} non <UNK> presente in {frutti}")
def e4():
    ## esercizio 4:
    n1 = int(input("inserisci num 1: "))
    n2 = int(input("inserisci num 2: "))
    n3 = int(input("inserisci num 3: "))
    numeri = (n1, n2, n3)
    media = sum(numeri) / len(numeri)
    print(media)
def e5():
    ## esercizio 5
    n1 = int(input("inserisci num 1: "))
    n2 = int(input("inserisci num 2: "))
    n3 = int(input("inserisci num 3: "))
    n4 = int(input("inserisci num 4: "))
    n5 = int(input("inserisci num 5: "))
    numeri = (n1, n2, n3, n4, n5)
    sottotupla = numeri[1:4]
    print("original tuple", numeri)
    print("sottotupla", sottotupla)
def e6():
    # esercizio 6 - dictionary - creazione di un dizionario semplice
    persona = {}
    # inseriamo copie di chiavi-valori
    persona["nome"] = input("inserisci il nome: ")
    persona["età"] = input("inserisci il età: ")
    persona["città"] = input("inserisci il city: ")
    print("dati registrati", persona)
def e7():
    ##esercizio 7
    # modificare il dict
    persona = dict(nome='iman', età=13, città='milano')
    # print(persona)
    persona['nome'] = input("inserisci un nome: ")
    print(persona)
def e8():
    ##my exercise
    n = int(input("inserisci la lunghezza del dizionario: "))
    libro = []
    autore = []
    pagina = []
    for i in range(n):
        libro.append(input(f"Enter libro_{i + 1}: "))
        autore.append(input(f"Enter autore_{i + 1}: "))
        pagina.append(int(input(f"pagina_{i + 1}: ")))
    dict = {
        "libro": libro,
        "autore": autore,
        "pagina": pagina
    }
    print(dict)
def e9():
    ##esercizio 8 - my solution
    my_dict = dict(autore="antonio", libro="python per tutti", pagina=1000)
    campo_da_modificare = input("quale campo vorresti modificare? ")
    if campo_da_modificare in my_dict:
        my_dict[campo_da_modificare] = input("inserisci il valore da sostituire: ")
    else:
        print(f"{campo_da_modificare} non è presente in {my_dict}")
    for k in my_dict.keys():
        print(f"{k}: {my_dict[k]}")
    print(my_dict)
def e10():
    ## esercizio 9:
    # visulizzare di un dizionario completo:
    voti = dict()
    n = int(input("quanti studenti vuoi inserire: "))
    for _ in range(n):
        nome = input("inserisci il nome dello studente: ")
        voto = float(input("inserisci il voto dello studente: "))
        voti[nome] = voto
    print("registra voti: ", voti)

def select():
    functions=(e1, e2, e3, e4, e5, e6, e7, e8, e9, e10)
    message= '''
    select the number of exercise:
        Tuple:
            1. creation a tuple literally from 3 variable
            2. exchange the values of some variables 
            3. Verify the existence of a value in a tuple
            4. the average of three numeric variables
            5. slicing a tuple
        Dictionary:
            6. create a dictionary with the specified keys
            7. modify the value of a key
            8. create dictionary of three lists for then convert to csv
            9. modify the value of an inserted key
            10. create a dictionary with inserted values of certain keys
        0 to quit
        your choice: 
        '''
    function_call = int(input(message))
    while True:

        if 0 < function_call <= 10:
            functions[function_call -1]()
            function_call=int(input("Insert another exercise number: "))
        else:
            return

select()