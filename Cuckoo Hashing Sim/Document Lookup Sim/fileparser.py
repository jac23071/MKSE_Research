import re

def file_dictionary_builder(filenames):
    dictionary = []
    doc_keys = dict()

    for name in filenames:
        file_lines = []
        with open(name, 'r') as file:
            file_lines = file.readlines()

        for line in file_lines:
            words = line.split()
            for word in words:
                word = re.sub(r'[^a-zA-Z0-9]', '', word)
                word = word.lower()

                if word not in dictionary:
                    dictionary.append(word)

                if word in doc_keys:
                    if name not in doc_keys[word]:
                        doc_keys[word].append(name)
                    else:
                        continue

                if word not in doc_keys:
                    doc_keys[word] = []
                    doc_keys[word].append(name)

    return dictionary, doc_keys
