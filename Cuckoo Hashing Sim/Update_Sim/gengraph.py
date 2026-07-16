import matplotlib.pyplot as pplt

input_sizes = [25, 50, 75, 100, 125, 150]
AVG_updates = [148.2, 145.4, 142.2, 137.8, 129.7, 122.2]

pplt.title("Appended Updates vs Remaining Updates", fontsize = 18)
pplt.xlabel("Num Updates Appended", fontsize = 16)
pplt.ylabel("Num Remaining Updates", fontsize = 16)
pplt.plot(input_sizes, AVG_updates, marker = 'o', color = "#e80ce8")
pplt.xlim(0, 150) 
pplt.ylim(0, 150)
pplt.savefig("MKSE_Research/Cuckoo Hashing Sim/Update_Sim/alt_merge_percentage_NUT_150_R_1000.png")
