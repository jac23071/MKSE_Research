import matplotlib.pyplot as pplt

with open("cachesize.csv", 'r') as sizes:
    raw_results = sizes.readlines()
    results = []
    for line in raw_results:
        results.append(line.rstrip().split(','))

for line in results:
    for idx in range(12):
        line[idx] = int(line[idx])

input_sizes = [10, 100, 500, 1000, 1250, 2500, 3750, 5000, 6250, 7500, 8750, 10000]
pplt.title("Input size vs. Cache size", fontsize = 18)
pplt.xlabel("Input size (Number of words)", fontsize = 16)
pplt.ylabel("Number of stored words", fontsize = 16)
pplt.plot(input_sizes, results[0], marker = 'o', color = "#e02200", label = "No Random Selections")
pplt.plot(input_sizes, results[1], marker = 'o', color = "#ffa914", label = "10 Random Selections")
pplt.plot(input_sizes, results[2], marker = 'o', color = "#26ffb0", label = "100 Random Selections")
pplt.plot(input_sizes, results[3], marker = 'o', color = "#531fff", label = "250 Random Selections")
pplt.plot(input_sizes, results[4], marker = 'o', color = "#ff00f2", label = "1000 Random Selections")
pplt.xlim(0, 10000) 
pplt.ylim(0, 2000)
pplt.legend()
pplt.savefig("stash_red_plot.png")