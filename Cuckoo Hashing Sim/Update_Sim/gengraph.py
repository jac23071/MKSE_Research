import matplotlib.pyplot as pplt
def gen_x_axis(pace_setter, max):
    x_axis = []
    base = pace_setter
    while (pace_setter <= max):
        x_axis.append(pace_setter)
        pace_setter += base
    return x_axis

num_updates = gen_x_axis(50, 1500)
k10 = [72, 112, 152, 192, 232, 272, 312, 352, 392, 432, 472, 512, 552, 592, 632, 672, 712, 752, 792, 832, 872, 912, 952, 992, 1032, 1072, 1112, 1152, 1192, 1232]
k25 = [56, 81, 106, 131, 156, 181, 206, 231, 256, 281, 306, 331, 356, 381, 406, 431, 456, 481, 506, 531, 556, 581, 606, 631, 656, 681, 706, 731, 756, 781]
k35 = [46, 62, 77, 92, 107, 122, 137, 152, 167, 182, 197, 212, 227, 242, 257, 272, 287, 302, 317, 332, 347, 362, 377, 392, 407, 422, 437, 452, 467, 482]
k50 = [32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32]

pplt.title("Appended Updates vs Cache sizes", fontsize = 18)
pplt.xlabel("Num Updates Appended", fontsize = 16)
pplt.ylabel("Cache Sizes", fontsize = 16)
pplt.plot(num_updates, k10, marker = 'o', color = "#f21602", label = "k = 10")
pplt.plot(num_updates, k25, marker = 'o', color = "#fc9d03", label = "k = 25")
pplt.plot(num_updates, k35, marker = 'o', color = "#0324fc", label = "k = 35")
pplt.plot(num_updates, k50, marker = 'o', color = "#e80ce8", label = "k = 50")
pplt.legend()
pplt.xlim(0, 1500) 
pplt.ylim(0, 1500)
pplt.savefig("MKSE_Research/Cuckoo Hashing Sim/Update_Sim/p_merge_percentage_NUT_1500.png")
