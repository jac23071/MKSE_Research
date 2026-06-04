from hashlib import sha256
from math import floor
from random import randint
import sys
from time import time

class word:
    def __init__(self, word):
        self.word = word
        self.placement = 0
        
    def inc(self):
        if(self.placement != 3):
            self.placement += 1
    
    def get_loc(self):
        return self.placement
    
    def __str__(self):
        return self.word

def init_table(table, table_size):
    """Initializes a table with all -inf vals to signify empty space. Returns nothing."""
    for i in range(table_size):
        table.append(float('-inf'))
    return

def hashing_alg(data_piece, table_size):
    """Hashes a piece of data and returns a list of placements."""
    inverse_piece  = data_piece[::-1] + "abcxyz"
    third_piece = data_piece + "123789"
    fourth_piece = data_piece[::-1] + "1237890"

    hash_obj = sha256()

    hash_obj.update(data_piece.encode())
    placement_1 = int(hash_obj.hexdigest(), 16) % table_size

    hash_obj.update(inverse_piece.encode())
    placement_2 = int(hash_obj.hexdigest(), 16) % table_size

    hash_obj.update(third_piece.encode())
    placement_3 = int(hash_obj.hexdigest(), 16) % table_size

    hash_obj.update(fourth_piece.encode())
    placement_4 = int(hash_obj.hexdigest(), 16) % table_size

    place_list = [placement_1, placement_2, placement_3, placement_4]
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
    list_num_swaps = []

    for term in data_dict:
        wrd = word(term)
        loc = data_dict[term][0]
        num_swaps = 0

        #First pick is empty:
        if (table[loc] == float('-inf')):
            table[loc] = wrd
        
        #First isn't empty:
        #If not empty, there must already be a word object there
        else:
            swap_word = table[loc]
            table[loc] = wrd
            swap_word.inc()
            new_loc = data_dict[swap_word.word][swap_word.get_loc()]
            num_swaps += 1 
            
            while(table[new_loc] != float('-inf')):
                if(num_swaps == max_swaps):
                    cache.append(swap_word)
                    # start fake swaps:
                    for i in range(num_swaps):
                        rand_idx = randint(0, len(table) - 1)
                        # access memory and do nothing with it
                        ######################################
                        rand_word = table[rand_idx]
                        if (rand_word == float('inf')): #never true
                            print("If this prints, a catastrophic error has occured. Line 95.")
                        ######################################
                        for cache_word in cache:
                            for idx in range(4):
                                if data_dict[cache_word.word][idx] == rand_idx and table[rand_idx] == float('-inf'):
                                    table[rand_idx] = cache_word
                                    cache.remove(cache_word)
                    highest_num_swaps = max_swaps
                    list_num_swaps.append(num_swaps)
                    break

                else:
                    temp = table[new_loc]
                    table[new_loc] = swap_word
                    swap_word = temp
                    swap_word.inc()
                    new_loc = data_dict[swap_word.word][swap_word.get_loc()]
                    num_swaps += 1

                    if (table[new_loc] == float('-inf')):
                        table[new_loc] = swap_word
                        if (num_swaps > highest_num_swaps):
                            highest_num_swaps = num_swaps
                            break
            list_num_swaps.append(num_swaps)

            if (table[new_loc] == float('-inf')):
                table[new_loc] = swap_word
            
            for i in range(500):
                rand_idx = randint(0, len(table) - 1)
                for cache_word in cache:
                    for idx in range(4):
                            if data_dict[cache_word.word][idx] == rand_idx and table[rand_idx] == float('-inf'):
                                table[rand_idx] = cache_word
                                cache.remove(cache_word)

    #calc percentage in cache not-put-backable:
    ############################################
    num_npb = 0
    for cached_word in cache:
        if (cached_word.get_loc() == 3):
            num_npb += 1
    percent = float(num_npb)/float(len(cache))
    print("Percent npbables: " + str(percent))
    ############################################
    
    avg = 0
    sum = 0
    for i in range(len(list_num_swaps)):
        sum += list_num_swaps[i]
        avg = float(sum)/float((len(list_num_swaps)))

    with open("MKSE_Research/Cuckoo Hashing Sim/result_file.txt", "w+") as outfile:
        outfile.write(str(len(data_dict) - len(cache)))
        outfile.write("\n")
        outfile.write(str(len(cache)))
        outfile.write("\n")
        outfile.write(str(avg))

if __name__ == "__main__":
    #Important Vars
    scale = 1.8
    max_swaps = 5
    raw_data = sys.argv[1:]
    # raw_data = ["BIG", "SMALL", "HUGE", "TINY", "ENORMOUS", "MINISCULE"]

    table_size = floor(len(raw_data) * scale)
    table = []
    cache = []

    init_table(table, table_size)
    data_dict = hash_data(raw_data, table_size)
    place_data(data_dict, table, cache, max_swaps)
