with open("MKSE_Research/Cuckoo Hashing Sim/Update_Sim/upd_avgtime_R_200.csv", 'r') as timefile:
    raw_nums = timefile.readlines()
    nums = raw_nums[0].split(',')
    sum = 0
    for num in nums:
        if (num):
            num = float(num)
            sum += num
    print(sum/(len(nums) - 1))