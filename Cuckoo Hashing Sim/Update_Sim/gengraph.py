import matplotlib.pyplot as pplt

input_sizes = [10, 100, 500, 1000, 1250, 2500, 3750, 5000, 6250, 7500, 8750, 10000]
AVG_percentages = [.066, .673, 1.000, .570, .457, .207, .124, .113, .110, .085, .065, .055]

pplt.title("Input size vs. Avg. % Update Merges", fontsize = 18)
pplt.xlabel("Input size (Number of words)", fontsize = 16)
pplt.ylabel("Percentage of Merges", fontsize = 16)
pplt.plot(input_sizes, AVG_percentages, marker = 'o', color = "#e02200")
pplt.xlim(0, 10000) 
pplt.ylim(0, 1)
pplt.savefig("Merge_percentage_NUT_100_R_1000.png")
