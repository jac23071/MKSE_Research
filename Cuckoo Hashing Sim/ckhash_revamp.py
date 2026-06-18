from hashlib import sha256
from math import floor
from random import randint
import sys
from time import time

#Number of hashes each word has:
NUM_HASHES = 4

class word:
    def __init__(self, word):
        self.word = word
        self.placement = 0
        
    def inc(self):
        if(self.placement != NUM_HASHES - 1):
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

def place_data_RW(data_dict, table, cache, max_swaps):
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
                            for idx in range(NUM_HASHES):
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
            
            for i in range(1000):
                rand_idx = randint(0, len(table) - 1)
                for cache_word in cache:
                    for idx in range(NUM_HASHES):
                            if data_dict[cache_word.word][idx] == rand_idx and table[rand_idx] == float('-inf'):
                                table[rand_idx] = cache_word
                                cache.remove(cache_word)

    # #calc percentage in cache not-put-backable:
    # ############################################
    # num_npb = 0
    # for cached_word in cache:
    #     if (cached_word.get_loc() == 3):
    #         num_npb += 1
    # percent = float(num_npb)/float(len(cache))
    # print("Percent npbables: " + str(percent))
    # ############################################
    
    avg = 0
    sum = 0
    for i in range(len(list_num_swaps)):
        sum += list_num_swaps[i]
    avg = float(sum)/float((len(data_dict)))

    with open("MKSE_Research/Cuckoo Hashing Sim/result_file.txt", "w+") as outfile:
        outfile.write(str(len(data_dict) - len(cache)))
        outfile.write("\n")
        outfile.write(str(len(cache)))
        outfile.write("\n")
        outfile.write(str(avg))

def place_data_BFS(data_dict, table, cache, max_swaps):

    for word in data_dict:
        # if(word == 'recovery'):
        #     print("and hereeee we gooooo")
            
        highest_num_swaps = 0
        list_num_swaps = []

        bfs_queue = []
        path_layer = 1
        path_ptr = -1
        path_found = 0 # will flip to 1 if a space was found before termination

        # if (word == "cities"):
            # print("Stop point here:")
            # print(data_dict[word][0])

        found_in_layer1 = 0 # will be set to true iff the space was found in layer one
        for possible_space in range(NUM_HASHES):
            if(table[data_dict[word][possible_space]] == float('-inf')):
                table[data_dict[word][possible_space]] = word
                path_found = 1
                found_in_layer1 = 1
                break
            else:
                bfs_queue.append(data_dict[word][possible_space])
        
        final_idx = -1 # will be set to the idx of the empty space found in the bfs queue
        while(path_layer != max_swaps and not path_found and not found_in_layer1): # end when ptr reaches max depth
            for seg_idx in range(1, pow(NUM_HASHES, path_layer) + 1): #traverse length of full segment
                if (path_found):
                    break
                word_idx = bfs_queue[path_ptr + seg_idx]
                tbl_word = table[word_idx]
                for tbl_word_idx in range(NUM_HASHES):
                    next_node_idx = data_dict[tbl_word][tbl_word_idx]
                    bfs_queue.append(next_node_idx)
                    if (table[next_node_idx] == float('-inf')):
                        final_idx = path_ptr + pow(NUM_HASHES, path_layer) + (NUM_HASHES * (seg_idx - 1)) + tbl_word_idx + 1
                        path_found = 1
                        break
            path_ptr += pow(NUM_HASHES, path_layer)
            if (not path_found):
                path_layer += 1
        
        if (not path_found): #Coudn't find empty space in 5 layers
            cache.append(word)
            continue
        elif (not found_in_layer1): #empty Space found, location at final_idx
            #if a space is found, we need to swap previous nodes upwards, only stopping when -
            #-the previous layer == 0

            if (path_layer > highest_num_swaps):
                highest_num_swaps = path_layer
            list_num_swaps.append(path_layer + 1)

            while(path_layer != 0):
                prev_ptr = path_ptr - pow(NUM_HASHES, path_layer)
                dist = final_idx - path_ptr
                prev_node = prev_ptr + (dist + (NUM_HASHES - (dist % NUM_HASHES)))//NUM_HASHES if dist % NUM_HASHES != 0 else prev_ptr + dist//NUM_HASHES
                #Now swap forwards:
                # if (table[prev_node] == 'build'):
                    # print("Pause here to examine behaviour")
                # if (bfs_queue[final_idx] < 0 or bfs_queue[final_idx] > 4500):
                #     print("Here we go again")
                table[bfs_queue[final_idx]] = table[bfs_queue[prev_node]]
                table[bfs_queue[prev_node]] = float('-inf')
                #Now move backwards in BFS path:
                final_idx = prev_node
                path_ptr = prev_ptr
                path_layer -= 1
            #At layer 0 now, so just swap the word upward, finally
            table[bfs_queue[final_idx]] = word
            #TODO: Double n triple check the math to ensure this works!
        else:
            continue
    
    avg = 0
    sum = 0
    for i in range(len(list_num_swaps)):
        sum += list_num_swaps[i]
    avg = float(sum)/float((len(data_dict)))

    with open("MKSE_Research/Cuckoo Hashing Sim/result_file.txt", "w+") as outfile:
        outfile.write(str(len(data_dict) - len(cache)))
        outfile.write("\n")
        outfile.write(str(len(cache)))
        outfile.write("\n")
        outfile.write(str(avg))
    
    print("Table:")
    print(table)
    print("Stash:")
    print(cache)

def check_correct(data_dict, table):
    # seen = set()
    for word in data_dict:
        # if (word in seen):
        #     print(word + " appears multiple times!")
        # else:
        #     seen.add(word)
        
        found = 0
        for idx in range(NUM_HASHES):
            tbl_idx = data_dict[word][idx]
            if (word == table[tbl_idx]):
                found = 1
                break
            elif word in cache:
                found = 1
                break
        
        if (not found):
            print(word + " not found!")
    
    # #check table scale:
    # scale_check = len(table)/len(data_dict)
    # print(scale_check)

if __name__ == "__main__":
    #Important Vars
    scale = 1.00
    max_swaps = 5
    raw_data = sys.argv[1:]
    # raw_data = ["BIG", "SMALL", "HUGE", "TINY", "ENORMOUS", "MINISCULE"]

    table_size = floor(len(raw_data) * scale)
    table = []
    cache = []

    init_table(table, table_size)
    data_dict = hash_data(raw_data, table_size)
    place_data_BFS(data_dict, table, cache, max_swaps)
    check_correct(data_dict, table)
    print("Data dict len: " + str(len(data_dict)))
    # for idx in range(len(table)):
    #     if (table[idx] == 'business'):
    #         print("##################################")
    #         print("Alert! line 280! idx: " + str(idx))
    # print(data_dict['cities'])
    # print(data_dict['very'])