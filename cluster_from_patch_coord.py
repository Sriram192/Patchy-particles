# %%
import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd 

# %%
p1_id = np.arange(1,3000,3)
p2_id = np.arange(3,3001,3)

# %%
filename = "patch_coord_cluster.dat"
line_counter = 0
time_step = []
itera = 0
n_patch = 1000
old_cord_p1 = np.zeros(1000)
old_cord_p2 = np.zeros(1000)
old_num_chains = 0
old_num_chain_ends = 0
elongation = 0
fragmentation = 0
depolymerization = 0
out_filename = "rates.dat"
out_file = open(out_filename,"w")
print("Time_step   elon   frag   depoly   num_chain   num_monomer",file = out_file)
with open(filename,"r") as file1:
    for line in file1:
        line_counter += 1
        if line_counter == 2:
            time_step.append(int(line.split()[0]))
            #print(time_step[itera])
        if line_counter == 4:
            n_patch = int(line.split()[0])
            length = int(n_patch/2)
            curr_cord_p1 = np.zeros(length)
            curr_cord_p2 = np.zeros(length)
            it = 0
        if line_counter >= 10 and line_counter <= n_patch+9:
            t_list = [int(i) for i in line.split()]
            if line_counter%2 == 0:
                curr_cord_p1[int(it/2)] = t_list[2]
            else:
                curr_cord_p2[int(it/2)] = t_list[2]
            it += 1
        if line_counter == n_patch+9:
            line_counter = 0
            num_monomer = 0
            curr_num_chain_ends = 0
            curr_num_chains = 0
            for i in range(0,len(curr_cord_p1)):
                if curr_cord_p1[i] == 0 and curr_cord_p2[i] == 0:
                    num_monomer += 1
                if curr_cord_p1[i] == 0 and curr_cord_p2[i] == 1:
                    curr_num_chain_ends += 1
                elif curr_cord_p1[i] == 1 and curr_cord_p2[i] == 0:
                    curr_num_chain_ends += 1

            curr_num_chains = curr_num_chain_ends/2
            
            if itera >= 1:
                elongation = 0
                fragmentation = 0
                depolymerization = 0
                for k in range(0,len(curr_cord_p1)):
                    if (old_cord_p1[k] == 0 and old_cord_p2[k] ==0 ) and (curr_cord_p1[k] == 1 or curr_cord_p2[k] == 1):
                        elongation += 1
                    elif (old_cord_p1[k] == 1 and old_cord_p2[k] == 0) and (curr_cord_p1[k] == 1 and curr_cord_p2[k] == 1):
                        elongation += 1
                    elif (old_cord_p1[k] == 0 and old_cord_p2[k] == 1) and (curr_cord_p1[k] == 1 and curr_cord_p2[k] == 1):
                        elongation += 1
                    elif (old_cord_p1[k] == 0 and old_cord_p2[k] == 1) and (curr_cord_p1[k] == 1 and curr_cord_p2[k] == 0):
                        depolymerization += 1
                        elongation += 1
                    elif (old_cord_p1[k] == 1 and old_cord_p2[k] == 0) and (curr_cord_p1[k] == 0 and curr_cord_p2[k] == 1):
                        depolymerization += 1
                        elongation += 1
                    if (old_cord_p1[k] == 1 and old_cord_p2[k] == 1) and (curr_cord_p1[k] == 1 and curr_cord_p2[k] == 0):
                        fragmentation += 1
                    elif (old_cord_p1[k] == 1 and old_cord_p2[k] == 1) and (curr_cord_p1[k] == 0 and curr_cord_p2[k] == 1):
                        fragmentation += 1
                    if (old_cord_p1[k] == 1 and old_cord_p2[k] == 0) and (curr_cord_p1[k] == 0 and curr_cord_p2[k] == 0):
                        depolymerization += 1
                    elif (old_cord_p1[k] == 0 and old_cord_p2[k] == 1) and (curr_cord_p1[k] == 0 and curr_cord_p2[k] == 0):
                        depolymerization += 1
                elongation = elongation/curr_num_chains
                fragmentation = fragmentation/curr_num_chains
                depolymerization = depolymerization/curr_num_chains
                print("%d %0.5f %0.5f %0.5f %d %d"%(time_step[itera],elongation,fragmentation,
                                                   depolymerization,curr_num_chains,num_monomer),file = out_file)
                #print(time_step[itera]," ",elongation," ",fragmentation," ",depolymerization," ",curr_num_chains," ",num_monomer,file = out_file)
            old_cord_p1 = curr_cord_p1
            old_cord_p2 = curr_cord_p2
            old_num_chains = curr_num_chains
            old_num_chain_ends = curr_num_chain_ends
            itera += 1
print("done")
out_file.close()                
                        

# %%


# %%



