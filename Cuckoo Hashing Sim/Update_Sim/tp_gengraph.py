import matplotlib.pyplot as pplt
def gen_x_axis(pace_setter, max):
    x_axis = []
    base = pace_setter
    while (pace_setter <= max):
        x_axis.append(pace_setter)
        pace_setter += base
    return x_axis

num_updates = gen_x_axis(50, 600)
stable_values = [256, 182, 137, 112, 105, 95, 91, 74, 60, 62, 56, 59]
pplt.title("Num Selected Pts vs Init Stable Vals", fontsize = 18)
pplt.xlabel("Num Selected Pts", fontsize = 16)
pplt.ylabel("Init Stable Vals", fontsize = 16)
pplt.plot(num_updates, stable_values, marker = 'o', color = "#f21602")
pplt.xlim(0, 600) 
pplt.ylim(0, 275)
pplt.savefig("MKSE_Research/Cuckoo Hashing Sim/Update_Sim/p_merge_NUT_1500_R_600_stablegraph.png")
