import matplotlib.pyplot as pplt
import subprocess

def run_test(test_data):
    args = ["python3", "cuckoohash.py"]
    args += test_data
    
    subprocess.run(args=args)

    output = []
    with open("result_file.txt", 'r') as outfile:
        output = [line.rstrip() for line in outfile]

    for i in range(len(output) - 1):
        output[i] = int(output[i])
    
    output[2] = float(output[2])
    
    return output

if (__name__ == "__main__"):
    test_data = []
    with open("google-10000-english-usa.txt") as data_file:
        test_data = [line.rstrip() for line in data_file]
    
    trial_10 = run_test(test_data[:10])
    trial_100 = run_test(test_data[:100])
    trial_500 = run_test(test_data[:500])
    trial_1000 = run_test(test_data[:1000])
    trial_2500 = run_test(test_data[:2500])
    trial_5000 = run_test(test_data[:5000])
    trial_7500 = run_test(test_data[:7500])
    trial_10000 = run_test(test_data)

    trial_results = [trial_10, trial_100, trial_500, trial_1000, trial_2500, trial_5000, trial_7500, trial_10000]

    list_sizes = [10, 100, 500, 1000, 2500, 5000, 7500, 10000]
    table_sizes = []
    cache_sizes = []
    avg_num_swaps = []

    for i in range(8):
        table_sizes.append(trial_results[i][0])
        cache_sizes.append(trial_results[i][1])
        avg_num_swaps.append(trial_results[i][2])
    
    # pplt.title("Input size vs. Table Storage and Cache size \n (Table scale: x2.00)", fontsize = 18)
    # pplt.xlabel("Input size (Number of words)", fontsize = 16)
    # pplt.ylabel("Number of stored words", fontsize = 16)
    # pplt.plot(list_sizes, table_sizes, marker = 'v', color = "#ff3355")
    # pplt.plot(list_sizes, cache_sizes, marker = 'o', color = "#05f7db")
    # pplt.xlim(0, 10000)
    # pplt.ylim(0, 10000)
    # pplt.savefig("fig_2.00.png")

    # sum = 0
    # avg = 0
    # for i in range(len(avg_num_swaps)):
    #     sum += avg_num_swaps[i]
    #     avg = float(sum) / float(len(avg_num_swaps))
    
    # with open("avgs.txt", "a+") as avgs:
    #     avgs.write("2.000 : " + str(avg))
    #     avgs.write('\n')
    
    # pplt.title("Table Scale vs. Average Number of Swaps", fontsize = 18)
    # pplt.xlabel("Table Scale Relative to Input Size", fontsize = 16)
    # pplt.ylabel("Average Number of Swaps", fontsize = 16)
    # pplt.plot([1.000, 1.125, 1.250, 1.375, 1.500, 1.625, 1.750, 1.875, 2.000], [1670.225164723272, 1632.9702387257225, 1370.7204949813502, 1494.213356329819, 1274.8802132172502, 1373.5472146714317, 1138.9927323344707, 1345.8778474392627, 1214.675838093912], marker = '*', color = "#43d11f")
    # pplt.xlim(1, 2)
    # pplt.ylim(1000, 1750)
    # pplt.savefig("fig_ScaleVSwap.png")

    # # Plot Input size vs Cache Size graphs
    # #######################################################################
    # pplt.title("Input size vs. Cache size \n (Max Swaps: 15)", fontsize = 18)
    # pplt.xlabel("Input size (Number of words)", fontsize = 16)
    # pplt.ylabel("Number of stored words", fontsize = 16)
    # pplt.plot(list_sizes, cache_sizes, marker = 'o', color = "#05f7db")
    # pplt.xlim(0, 10000)
    # pplt.ylim(0, 2000)
    # pplt.savefig("Small_Swaps/fig_15s_small_1.8.png")
    # ########################################################################
    
    # #Add avgs to file:
    # #########################################################################
    # sum = 0
    # avg = 0
    # for i in range(len(avg_num_swaps)):
    #     sum += avg_num_swaps[i]
    #     avg = float(sum) / float(len(avg_num_swaps))
    
    # with open("Small_Swaps/avgs_swap_test_small_1.8.txt", "a+") as avgs:
    #     avgs.write("Maximum 15 Swaps : " + str(avg))
    #     avgs.write('\n')
    # ##########################################################################

    #Plot avgs into graph
    ##########################################################################
    pplt.title("Maximum Number of Swaps vs. Average Number of Swaps", fontsize = 18)
    pplt.xlabel("Maximum Number of Swaps", fontsize = 16)
    pplt.ylabel("Average Number of Swaps", fontsize = 16)
    pplt.plot([1, 3, 5, 7, 9, 11, 13, 15], [1.0, 2.359938892123858, 3.7133611917780196, 5.067130243054754, 6.418678954396966, 7.770064841546669, 9.121450728696374, 10.472836615846077], marker = '*', color = "#fccf38")
    pplt.xlim(0, 10000)
    pplt.ylim(0, 7000)

    pplt.title("Max Num of Swaps vs. Avg Num of Swaps", fontsize = 18)
    #(Table Scale = 1.8 (Orange) and 2.2 (Purple))
    pplt.xlabel("Maximum Number of Swaps", fontsize = 16)
    pplt.ylabel("Average Number of Swaps", fontsize = 16)
    pplt.plot([1, 3, 5, 7, 9, 11, 13, 15], [1.0, 2.178938712300417, 3.3596471719661047, 4.461505307256615, 5.577954938177401, 6.694404569098188, 7.810854200018974, 8.92730383093976], marker = '*', color = "#e629f0")
    pplt.xlim(0, 15)
    pplt.ylim(0, 15)
    pplt.savefig("Small_Swaps/fig_MaxVAvg.png")
    ########################################################################