from hashlib import sha256
from math import floor
import sys
from time import time 

def init_table(table, table_size):
    """Initializes a table with all -inf vals to signify empty space. Returns nothing."""
    for i in range(table_size):
        table.append(float('-inf'))
    return

def hashing_alg(data_piece, table_size):
    """Hashes a piece of data and returns a list of placements."""
    inverse_piece  = data_piece[::-1]

    hash_obj = sha256()
    hash_obj.update(data_piece.encode())
    placement_1 = int(hash_obj.hexdigest(), 16) % table_size
    hash_obj.update(inverse_piece.encode())
    placement_2 = int(hash_obj.hexdigest(), 16) % table_size

    if (placement_1 == placement_2):
        inverse_piece += "abcxyz"
        hash_obj.update(inverse_piece.encode())
        placement_2 = int(hash_obj.hexdigest(), 16) % table_size

    place_list = [placement_1, placement_2]
    return place_list

def hash_data(data_list, table_size):
    """Hashes all data and places the placement list into a dict with the original 
    data being the key.
    """
    data_dict = {}
    for word in data_list:
        data_dict[word] = hashing_alg(word, table_size)
    return data_dict

def place_data(data_dict, table, cache, max_swaps):
    """Places data into their place in the array. Handles swaps and caching. Returns
    nothing, but prints time taken and maximum number of swaps. 
    """
    highest_num_swaps = 0
    start_time = time()
    list_num_swaps = []

    for word in data_dict:
        loc = data_dict[word][0]
        num_swaps = 0

        if (table[loc] == float('-inf')):
            table[loc] = word

        else:
            swap_word = table[loc]
            table[loc] = word
            new_loc = data_dict[swap_word][1]
            num_swaps += 1

            while(table[new_loc] != float('-inf')):
                if (num_swaps == max_swaps):
                    cache.append(swap_word)
                    highest_num_swaps = max_swaps
                    list_num_swaps.append(num_swaps)
                    break

                else:
                    temp = table[new_loc]
                    table[new_loc] = swap_word
                    swap_word = temp
                    new_loc = data_dict[swap_word][1]
                    num_swaps += 1

                    if (table[new_loc] == float('-inf')):
                        table[new_loc] = swap_word
                        if (num_swaps > highest_num_swaps):
                            highest_num_swaps = num_swaps
                            break
            list_num_swaps.append(num_swaps)

            if (table[new_loc] == float('-inf')):
                table[new_loc] = swap_word
    end_time = time()
    total_time = end_time - start_time

    # print("Total time = " + str(total_time) + " and highest number of swaps = " + str(highest_num_swaps))
    # print("Table: \n---------------------------------")
    # print(table)
    # print("Cache: \n---------------------------------")
    # print(cache)
    avg = 0
    sum = 0
    for i in range(len(list_num_swaps)):
        sum += list_num_swaps[i]
        avg = float(sum)/float((len(list_num_swaps)))

    with open("result_file.txt", "w+") as outfile:
        outfile.write(str(len(data_dict) - len(cache)))
        outfile.write("\n")
        outfile.write(str(len(cache)))
        outfile.write("\n")
        outfile.write(str(avg))
            
    
if __name__ == "__main__":
    #Important Vars
    scale = 2.000
    max_swaps = 2000
    raw_data = sys.argv[1:]
    # raw_data = ["BIG", "SMALL", "HUGE", "TINY", "ENORMOUS", "MINISCULE"]

    table_size = floor(len(raw_data) * scale)
    table = []
    cache = []

    init_table(table, table_size)
    data_dict = hash_data(raw_data, table_size)
    place_data(data_dict, table, cache, max_swaps)
