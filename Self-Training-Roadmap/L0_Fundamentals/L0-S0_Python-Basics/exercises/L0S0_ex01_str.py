import timeit

sentences = [
    "  Hello World!  ",
    "Python 3.12.1 is out.",
    "سلام دنیا",
    "    DATA, 2025!!   ",
    "   \tclean Me\t\n"
]
def clean_text(text):
    return [sentence.strip() for sentence in text]

def ascii_only(text):
    return [sentence for sentence in text if sentence.isascii()]

def to_uppercase(text):
    return [sentence.upper() for sentence in text]

def check_start_end(text):
    for sentence in text:
        if sentence.startswith("DATA") or sentence[-1].isdigit():
            sentence = "*"+sentence
    return ["*"+sentence if sentence.startswith("DATA") or sentence[-1].isdigit() else sentence for sentence in text]

def replace_digits(text):
    tab = str.maketrans("0123456789", "XXXXXXXXXX")
    return [sentence.translate(tab) for sentence in text]

def join_sentences(text):
    return '#'.join(text)

def main():
    if __name__=="__main__":
        print(join_sentences(sentences))
        print(replace_digits(sentences))
        print(check_start_end(sentences))
        print(to_uppercase(sentences))
        print(ascii_only(sentences))
        print(clean_text(sentences))
main()  
print(f"{timeit.timeit(main, number=1):.5f} seconds")  
