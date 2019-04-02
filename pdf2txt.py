import pdftotext
from itertools import islice

def window(seq, n=2):
    it = iter(seq)
    result = tuple(islice(it, n))
    if len(result) == n:
        yield result
    for elem in it:
        result = result[1:] + (elem,)
        yield result

def header(str, max_length):
    return len(str) > 0 and not str.startswith(' ') and str[0].isupper() and len(str) < max_length / 1.3

def para_separation(data):
    data_list = list(map(lambda x: x.strip(), data.split('\n')))
    data_list_with_length = map(lambda x: (len(x), x), data_list)
    max_length = sorted(data_list_with_length, key=lambda x: -1 * x[0])[0][0]

    sliding = list(window(data_list, 2))

    indexes = []
    index = 0
    for (i, j) in sliding:
        i = i.strip()
        j = j.strip()
        if ((i.endswith('.') and (len(j.strip()) == 0 or j[0].isupper()))
            or (len(j.strip()) > 0 and j.strip()[0].encode("unicode_escape") != j.strip()[0])
            or header(i, max_length)):
            indexes.append(index)
        index += 1

    new_data_list = []
    index = 0
    for line in data_list:
        new_data_list.append(line)
        new_data_list.append(' ')
        if (index in indexes):
            new_data_list.append('\n')
        index += 1

    result = ''.join(new_data_list).replace('. ', '\n').split('\n')

    return result

# Load your PDF

if __name__ == '__main__':
    sample_path ="/Users/avinash.v/Projects/indix/nlp/data/tax-files/walhalla-memo.pdf"
    sample_path = "/Users/avinash.v/Downloads/Tagging/Town of Hauchuca Sales-Tax-Increase.pdf"
    with open(sample_path, "rb") as f:
        pdf = pdftotext.PDF(f)

        # If it's password-protected

        # with open("secure.pdf", "rb") as f:
        #     pdf = pdftotext.PDF(f, "secret")

        # How many pages?
        print(len(pdf))

        # Iterate over all the pages
        for page in pdf:
            print(para_separation(page))


        # Read all the text into one string
        # print("\n\n".join(pdf))
