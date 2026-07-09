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
    
    def __eq__(self, other):
        if(isinstance(other, word)):
            return self.word == other.word
        elif(isinstance(other, float)):
            return False

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

def create_rand_set(size, tbl_len):
    """Creates a set of a 'size' unique indices for a table of 'tbl_len'"""
    if (size > tbl_len):
        size = tbl_len

    rand_set = set()
    for num_terms in range(size):
        new_int = randint(0, tbl_len - 1)
        while(new_int in rand_set):
            new_int = randint(0, tbl_len - 1)
        rand_set.add(new_int)
    return rand_set

def start_swapchain(data_dict, table, cache, max_swaps, init_wrd, highest_num_swaps, list_num_swaps, loc_dict):
    loc = data_dict[init_wrd.word][init_wrd.placement]
    num_swaps = 0

    #First pick is empty:
    if (table[loc] == float('-inf')):
        table[loc] = init_wrd
    
    #First isn't empty:
    #If not empty, there must already be a word object there
    else:
        swap_word = table[loc]
        table[loc] = init_wrd
        swap_word.inc()
        new_loc = data_dict[swap_word.word][swap_word.get_loc()]
        num_swaps += 1 
        
        while(table[new_loc] != float('-inf')):
            if(num_swaps == max_swaps):
                cache.append(swap_word)
                #put swap_word in loc_dict
                for possibility in data_dict[swap_word.word]:
                    if (possibility in loc_dict):
                        loc_dict[possibility].append(swap_word)
                    else:
                        loc_dict[possibility] = []
                        loc_dict[possibility].append(swap_word)
                        
                # start fake swaps:
                rand_set = create_rand_set(10, len(table))
                loc_set = set()
                for loc in loc_dict:
                    loc_set.add(loc)
                selected_set = rand_set & loc_set
                for rand_idx in rand_set:
                    # access memory and do nothing with it
                    ######################################
                    rand_word = table[rand_idx]
                    if (rand_word == float('inf')): #never true
                        print("If this prints, a catastrophic error has occured. Line 104.")
                    ######################################
                    # if (rand_idx in selected_set):
                    #     stash_word = loc_dict[rand_idx][-1]
                    #     for data_idx in range(4):
                    #         if (data_dict[stash_word][data_idx] == rand_idx):
                    #             break
                    #         # update stash_word's pos to be data_idx
                    #         stash_word.placement = data_idx
                    #     #remove word obj from stash and from all loc_dict locs before starting new swapchain
                    #     cache.remove(stash_word)
                    #     for possibility in data_dict[stash_word]:
                    #         loc_dict[possibility].remove(stash_word)
                    #         if (not loc_dict[possibility]):
                    #             loc_dict.remove(possibility)
                    #     #begin new swapchain
                    #     start_swapchain(data_dict, table, cache, max_swaps, stash_word, highest_num_swaps, list_num_swaps, loc_dict)

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

def place_data_RW(data_dict, table, cache, max_swaps):
    """Places data into their place in the array via Random Walk. Handles swaps
    and stashing.
    """
    highest_num_swaps = 0
    list_num_swaps = []
    loc_dict = dict()

    for term in data_dict:
        wrd = word(term)
        start_swapchain(data_dict, table, cache, max_swaps, wrd, highest_num_swaps, list_num_swaps, loc_dict)
        # #Rand selections for swapchains
        # rand_set = create_rand_set(10, len(table))
        # loc_set = set()
        # for loc in loc_dict:
        #     loc_set.add(loc)
        # select_set = loc_set & rand_set

        # for s_idx in select_set:
        #     if (s_idx not in loc_dict):
        #         break

        #     stash_word = loc_dict[s_idx][-1]
        #     for data_idx in range(4):
        #         if (data_dict[stash_word.word][data_idx] == s_idx):
        #             break
        #         # update stash_word's pos to be data_idx
        #         stash_word.placement = data_idx
        #     #remove word obj from stash and from all loc_dict locs before starting new swapchain
        #     cache.remove(stash_word)
        #     for possibility in data_dict[stash_word.word]:
        #         loc_dict[possibility].remove(stash_word)
        #         if (not loc_dict[possibility]):
        #             loc_dict.pop(possibility)
        #     #begin new swapchain
        #     start_swapchain(data_dict, table, cache, max_swaps, stash_word, highest_num_swaps, list_num_swaps, loc_dict)


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
    
    return loc_dict

def update_sim(table, cache, data_dict, loc_dict):
    NUM_UPD_TERMS = 150

    #loop thru data_dict and get NU_Terms
    grabbed_terms = 0
    for key in data_dict:
        if (grabbed_terms == NUM_UPD_TERMS): #if we have all needed terms, stop
            break
        upd_word = word(key)
        if upd_word in cache: #if the updword is already a cached term, continue
            continue

        #append cache word to cache and to loc_dict
        cache.append(upd_word)
        for possibility in data_dict[key]:
            if (possibility in loc_dict):
                loc_dict[possibility].append(upd_word)
            else:
                loc_dict[possibility] = []
                loc_dict[possibility].append(upd_word)
        grabbed_terms += 1
    
    #Now n duplicate terms are in loc_dict and the cache
    #Now make a selection of random points
    NUM_RAND_PTS = 1000
    rand_set = create_rand_set(NUM_RAND_PTS, len(table))
    loc_set = set()
    for loc in loc_dict:
        loc_set.add(loc)
    select_set = loc_set & rand_set
    
    num_merges = 0
    for s_idx in select_set:
        for stash_word in loc_dict[s_idx]:
            if (stash_word == table[s_idx]):
                num_merges += 1
    
    with open("MKSE_Research/Cuckoo Hashing Sim/Update_Sim/merge_NUT_150_R_1000.txt", "a+") as outfile:
        success_percentage = num_merges/NUM_UPD_TERMS
        outfile.write(str(success_percentage) + ", ")
        if(len(data_dict) > 9000):
            outfile.write("\n")

def place_data_BFS(data_dict, table, cache, max_swaps):
    """Places data into their place in the array via Breadth First Search. Handles swaps
    and stashing. 
    """
    highest_num_swaps = 0
    list_num_swaps = []

    for word in data_dict:
        # if(word == 'recovery'):
        #     print("and hereeee we gooooo")

        bfs_queue = []
        loc_dict = dict()
        path_layer = 1
        path_ptr = -1
        path_found = 0 # will flip to 1 if a space was found before termination

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
            # Add the possible locs for said term
            for word_idx in range(NUM_HASHES):
                if(data_dict[word][word_idx] in loc_dict):
                    loc_dict[data_dict[word][word_idx]].append(word)
                else:
                    loc_dict[data_dict[word][word_idx]] = []
                    loc_dict[data_dict[word][word_idx]].append(word)
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
                table[bfs_queue[final_idx]] = table[bfs_queue[prev_node]]
                table[bfs_queue[prev_node]] = float('-inf')
                #Now move backwards in BFS path:
                final_idx = prev_node
                path_ptr = prev_ptr
                path_layer -= 1
            #At layer 0 now, so just swap the word upward, finally
            table[bfs_queue[final_idx]] = word
            #Now look @ random indices to look for reintroduceable key terms
            rand_idx_set = create_rand_set(1000, len(table)) #set 1
            loc_set = set() # set 2
            for loc in loc_dict:
                set.add(loc)
            selected_idx_set = rand_idx_set & loc_set
            for idx in selected_idx_set:
                if (table[idx] == float("-inf")):
                    stash_word = loc_dict[idx][-1]
                    for possibility in data_dict[stash_word]:
                        if possibility in loc_dict:
                            loc_dict[possibility].remove(stash_word)
                        if (not loc_dict[possibility]): #if array is now empty
                            loc_dict.pop(possibility)
                    table[idx] = stash_word
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
    

def check_correct_BFS(data_dict, table):
    # seen = set()
    for word in data_dict:
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

def check_correct_RW(data_dict, table):
    # seen = set()
    for term in data_dict:
        wrd = word(term)
        found = 0
        for idx in range(NUM_HASHES):
            tbl_idx = data_dict[wrd.word][idx]
            if (wrd == table[tbl_idx]):
                found = 1
                break
            elif wrd in cache:
                found = 1
                break
        
        if (not found):
            print(wrd.word + " not found!")
    
    # #check table scale:
    # scale_check = len(table)/len(data_dict)
    # print(scale_check)

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
    loc_dict = place_data_RW(data_dict, table, cache, max_swaps)
    update_sim(table, cache, data_dict, loc_dict)
    # print(table)
    # print(cache)
    check_correct_RW(data_dict, table)
    # print("Data dict len: " + str(len(data_dict)))