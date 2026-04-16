import alt_cuckoohash as ckhash
import fileparser as fp
import sys

def init_server(filenames):
    dictionary, doc_keys = fp.file_dictionary_builder(filenames)
    table, cache = ckhash.create_table(dictionary)

    return table, cache, doc_keys

if __name__ == "__main__":
    if (not sys.argv):
        print("Please input file names to initialize the server")
    
    document_list = sys.argv[1:]
    table, cache, doc_keys = init_server(document_list)

    while(1):
        keywords = input("Please input desired keywords (input nothing to terminate lookup):")
        if(not keywords):
            print("Come again soon! :)")
            exit()

        words = keywords.split()
        for word in words:
            place_list = ckhash.hashing_alg(word, len(table))
            if (table[place_list[0]] == word):
                print("Word found in first case!\n")

            elif (table[place_list[1]] == word):
                print("Word found in second case!\n")

            elif (word in cache): 
                print("Had to linearly scan the cache :(\n")
                
            else:
                print("Word is not in these documents :(")
                continue
            
            found_docs = doc_keys[word]
            output_string = "Keyword " + word + " found in: "
            for doc in found_docs:
                output_string += doc + " "
            print(output_string)