# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 17:33:49 2022

@author: kmj05
"""


import pickle
import os
os.chdir(r'Z:\Soo B\Katie\projects\freezing_score\pickle_files')

# open pickle
with open("987_N_ctxA", "rb") as f:
    rawdata = f.read()
    
ctxA_987_N = pickle.loads(rawdata)



#%%


# pickle: save/open


import pickle
import os
path = r'Z:\Soo B\Katie\projects\freezing_score\pickle_files\10s_between_light\condition_4'
os.chdir(path)
# save pickle
with open('full_timestamps(4)', 'wb') as handle:
    pickle.dump(hi, handle, protocol=pickle.HIGHEST_PROTOCOL)


import pickle
import os
os.chdir(r'Z:\Soo B\Katie\projects\freezing_score\pickle_files\10s_between_light\condition_1')
# open pickle
with open("full_timestamps", "rb") as f:
    rawdata = f.read()
    
my_3d = pickle.loads(rawdata)



#%%

# delete area from the dictionary

def delete_area(my_input, my_type):
    mouse_list = []
    for mouse in my_input:
        mouse_list.append(mouse)
    for mouse in mouse_list:
        del my_input[mouse][my_type]
    return my_input

condition_1 = delete_area(condition_1, 'area_list')


    
#%%
    


# extract one of (freeze_only,area_list, timestamps) from final_dict
def extract_fz_only(my_input, my_type):
    mouse_list = []
    auto_dict = {}
    for mouse in my_input:
        mouse_list.append(mouse)
    for mouse in mouse_list:
        auto_dict[mouse] = my_input[mouse][my_type]
    return auto_dict

auto_dict = extract_fz_only(ctxB_after, 'freeze_list')



#%%


# convert into percentage, half second , 1/3

def fz_to_percentage():
    def data(numbers):
        boolean, x = [], []
        for idx, num in enumerate(numbers):
            x.append(num)
            if idx%3 == 0:
                counter = x.count(0)
                thresh = len([i for i in x if i>5])
                if (counter >= 2) and (thresh == 0):  #if 2 or more out of 3 are 0 --> fz
                    boolean.append(1)
                else:  #if less or equal to 1 out of 3 are 0 --> not fz
                    boolean.append(0)
                x = []
        total, counter = 0, 0
        for value in boolean:
            if value == 1:  #if freezing is true
                counter += 1
            elif value == 0:
                if counter >= 5:  #if more than 5 in a row is freezing
                    total += counter*3  #3 frames per fz or not fz value
                counter = 0
        total += counter*3  #add up last values too 
        return total / len(numbers) * 100
    my_dict = {}
    for key, value in auto_dict.items():
        freeze = []
        for x in value:
            aye = data(x)
            freeze.append(aye)
        my_dict[key] = freeze
    return my_dict

my_dict = fz_to_percentage()
        
    
    

#%%


# fs to control separate

#condition1
my_fs = {key: value for key,value in my_dict.items() if not ('833_N' in key or '833_RL' in key or '868_N' in key)}
my_ctr = {key: value for key,value in my_dict.items() if ('833_N' in key or '833_RL' in key or '868_N' in key)}
#condition5
my_fs = {key: value for key,value in my_dict.items() if not ('833_R' in key)}
my_ctr = {key: value for key,value in my_dict.items() if ('833_R' in key)}

#else:
my_fs = {key: value for key,value in my_dict.items() if not ('ctr' in key)}
my_ctr = {key: value for key,value in my_dict.items() if ('ctr' in key)}




#%%


import pickle
import os

path = r'Z:\Soo B\Katie\projects\freezing_score\pickle_files\only_after\condition_4\FS'
os.chdir(path)

for mouse,value in my_fs.items():
    with open(mouse, 'wb') as handle:
        pickle.dump(value, handle, protocol=pickle.HIGHEST_PROTOCOL)




#%%


# plotting!!

def day_type_and_plot_title(conditions):
    if conditions['day_type'] == 'md':
        day_type = ['D1', 'D2', 'D3', 'D4']
        day = 'Multi-day'
    elif conditions['day_type'] == 'sd':
        day_type = ['D1', 'D2']
        day = 'Single-day'
    #for title
    condition = conditions['fs_or_ctr']
    tone = conditions['tone_duration']
    cycle = conditions['number_of_cycles']
    title = f'{day}, {tone}, {cycle} cycles ({condition})'
    #for title
    return day_type, title


# segregate by days, dictionary output
def segregate_by_day(days, my_input):
    dictionary = {}
    for x in days:
        my_fs_d1 = {key:value for key,value in my_input.items() if x in key}
        dictionary[x] = my_fs_d1
    return dictionary


# plot graphs, contextB as separate plot
from matplotlib import pyplot as plt

def plotting(day_type, dictionary, title):
    plt.style.use('seaborn')
    if len(day_type) == 4:
        fig, axs = plt.subplots(nrows=1, ncols=3, sharey=True, figsize=[10,4.8])
        axs = axs.ravel()
    elif len(day_type) == 2:
        fig = plt.figure()
    fig.suptitle(title,fontsize=15)
    fig.tight_layout()
    i = 0
    for day, by_day in dictionary.items():
        # maximum list length
        temp = []
        for x in by_day.values():
            temp.append(len(x))
        temp = max(temp)
        # average by index
        average = []
        for x in range(temp):
            hi = []
            for y in by_day.values():
                try:
                    hi.append(y[x])
                except:
                    pass
            mean = sum(hi)/len(hi)
            average.append(mean)
        if day == day_type[-1]:
            fig = plt.figure()
            plt.plot(average,linewidth=2.5, color='#7f7f7f')
            over = 0
            for name, individual in by_day.items():    
                plt.scatter(range(len(individual)),individual,s=17, label=name[0:8])
                if len(individual) < temp:    
                    plt.vlines(x=len(individual),ymin=-3,ymax=105, colors='#bf80ff')
                    over += 1
            under = over
            over = len(by_day.values()) - over
            if under == 0:
                plt.title(f'{title}: context B',fontsize=15)
            else:
                plt.title(f'{title}: context B | {under} : {over}',fontsize=15)
            plt.ylim([-3,105])
            plt.xticks(range(0, temp, 1))
            plt.xlabel('Presentation #',fontsize=13)
            plt.ylabel('Freezing Percentage',fontsize=13)
            plt.legend(bbox_to_anchor=(1.3, 1.0),fontsize=12)
            plt.tight_layout(pad=1.5)
        else:
            if len(day_type) == 4:
                axs[i].plot(average,linewidth=2.5, color='#7f7f7f')
                for name, individual in by_day.items():    
                    axs[i].scatter(range(len(individual)),individual,s=17, label=name[0:8])
                axs[i].set_title(day)
                axs[i].set_ylim([-3, 105])
                axs[i].set_xticks(range(0, temp, 1))
                axs[i].set_xlabel('Presentation #',fontsize=13)
                axs[0].set_ylabel('Freezing Percentage',fontsize=13)
                axs[2].legend(bbox_to_anchor=(1.0, 1.0),fontsize=12)
                plt.tight_layout()
            elif len(day_type) == 2:
                plt.plot(average,linewidth=2.5, color='#7f7f7f')
                for name, individual in by_day.items():    
                    plt.scatter(range(len(individual)),individual,s=17, label=name[0:8])
                plt.ylim([-3, 105])
                plt.xticks(range(0, temp, 1))
                plt.xlabel('Presentation #',fontsize=13)
                plt.ylabel('Freezing Percentage',fontsize=13)
                plt.legend(bbox_to_anchor=(1.3, 1.0),fontsize=12)
                plt.tight_layout()
        i+=1
    
    
    
    

# CONDITIONS DICTIONARY:
# day_type: md, sd (multiday(4 days), single-day(2 days)) these include context B.
# fs_or_ctr: FS, ctr
# tone_duration: 1s, 10s
# number_of_cycles: 8, 15
conditions = {'fs_or_ctr': 'ctr',
              'day_type': 'sd',
              'tone_duration': '1s',
              'number_of_cycles': '8'}



day_type, title_for_plot = day_type_and_plot_title(conditions)

if conditions['fs_or_ctr'] == 'fs':
    dictionary = segregate_by_day(day_type, my_fs)
elif conditions['fs_or_ctr'] == 'ctr':
    dictionary = segregate_by_day(day_type, my_ctr)

plotting(day_type, dictionary, title_for_plot)





#%%

# maximum list length
temp = []
for x in my_fs.values():
    temp.append(len(x))
temp = max(temp)

# combined plots
import matplotlib.pyplot as plt
plt.figure()
plt.title('2 days, 1s, cycle: 8 FS, D2')
for k,v in my_fs_d1.items():
    mouse = k
    auto = v
    plt.ylim([0,100])
    plt.xticks(range(0, temp, 1))
    plt.plot(auto, label=mouse)
    # plt.axvline(x = 8)
    plt.legend()
    plt.tight_layout()
    
# individual plots
import matplotlib.pyplot as plt
for k,v in my_fs.items():   
    plt.figure()
    mouse = k
    auto = v
    plt.ylim([0, 100])
    plt.plot(auto, label=mouse)
    plt.title(mouse)


#%%


#automatic scoring organize (manual scoring)

def csv_convert(path):
    import csv    
    csv_file = []
    mouse_list,manual_fz = [], []
    
    with open(path, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            csv_file.append(row)
    
    for line in csv_file:
        if 'wt' in line[0]:
            mouse_list.append(f'{line[0]} {line[1]}')
            mouse_list.append(f'{line[0]} D2')
            mouse_list.append(f'{line[0]} D3')
        if 'freezing %' in line[0]:
            temp = []
            for x in line:
                if ('freezing %' not in x) and (len(x) > 0):
                    temp.append(float(x)*100)
            manual_fz.append(temp)
    
    manual_fz = list(zip(mouse_list, manual_fz))
    return manual_fz
    
manual = csv_convert(r'C:\Users\kmj05\OneDrive - personalmicrosoftsoftware.uci.edu\Downloads\Soo & Katie - Manual freeze-scoring_ trained (4).csv')
       


#%%


# plot graphs, contextB as a subplot
from matplotlib import pyplot as plt

def plotting(day_type, dictionary, title):
    if len(day_type) == 4:
        fig, axs = plt.subplots(nrows=2, ncols=2, sharey=True)
    elif len(day_type) == 2:
        fig, axs = plt.subplots(nrows=1, ncols=2, sharey=True)
    fig.suptitle(title)
    axs = axs.ravel()
    fig.tight_layout()
    i = 0
    for day, by_day in dictionary.items():
        # maximum list length
        temp = []
        for x in by_day.values():
            temp.append(len(x))
        temp = max(temp)
        # average by index
        average = []
        for x in range(temp):
            hi = []
            for y in by_day.values():
                try:
                    hi.append(y[x])
                except:
                    pass
            mean = sum(hi)/len(hi)
            average.append(mean)
            
        if day == day_type[-1]:
            axs[i].plot(average,linewidth=2.5, color='#7f7f7f')
            for name, individual in by_day.items():    
                axs[i].scatter(range(len(individual)),individual,s=12, label=name[0:8])
            axs[i].set_title(day+ ' (context B)')
            axs[i].legend(bbox_to_anchor=(1.0, 1.0),fontsize=9)
        else:
            axs[i].plot(average,linewidth=2.5, color='#7f7f7f')
            for individual in by_day.values():    
                axs[i].scatter(range(len(individual)),individual,s=12)
            axs[i].set_title(day)
        axs[i].set_ylim([0, 100])
        axs[i].set_xticks(range(0, temp, 1))
        i+=1

plotting(day_type, dictionary, title_for_plot)
    



#%%

# standard deviation, area colored

import numpy as np
from matplotlib import pyplot as plt

fig, axs = plt.subplots(nrows=2, ncols=2, sharey=True)
fig.suptitle('multiday, 1s, 8 cycles (FS)')
axs = axs.ravel()
fig.tight_layout()

i = 0
for day, by_day in dictionary.items():
    # maximum list length
    temp = []
    for x in by_day.values():
        temp.append(len(x))
    temp = max(temp)
    # average by index
    average = []
    std_min, std_max = [], []
    for x in range(temp):
        hi = []
        for y in by_day.values():
            try:
                hi.append(y[x])
            except:
                pass
        mean = sum(hi)/len(hi)
        std = np.std(np.array(hi))
        average.append(mean)
        std_min.append(mean-2*std)
        std_max.append(mean+2*std)
        
    if day == 'D4':
        axs[i].plot(average,'k')
        axs[i].fill_between(range(0, temp, 1), std_min, std_max, color='black', alpha=0.1)
        axs[i].set_title(day)
    else:
        axs[i].plot(average,'b')
        axs[i].fill_between(range(0, temp, 1), std_min, std_max, color='blue', alpha=0.1)
        axs[i].set_title(day)
    axs[i].set_ylim([0, 100])
    axs[i].set_xticks(range(0, temp, 1))
    
    i+=1
    
    
    
#%%



# for comparing manual and auto, graph

avg_diff = {}
lst = []
for k,v in manual_dict.items():
    for key in my_dict.keys():
        manual_split = k.split('_')
        manual_split[2] = manual_split[2][0:-3]
        manual_split.append((k.split())[-1])
        dict_split = key.split('_')
        dict_split[4] = dict_split[4][-2:]
        if set(manual_split).issubset(dict_split):
            a = sum(my_dict[key])
            break
    b = sum(v)
    avg_diff[k] = abs(b-a)
    lst.append(k)


x=[]
y=[]
for k,v in avg_diff.items():
    x.append(k)
    y.append(v)
    
plt.bar(lst, y)
plt.ylim([0, 60])
plt.title('only >15')
plt.tight_layout()
plt.show()


# zip and plot
# a = list(zip(mouse_list, auto_fz, manual_fz))
# manual_fz is mouselist + manual fz 

import matplotlib.pyplot as plt
i = 0
for k,v in manual_dict.items():    
    plt.figure()
    mouse = k
    for key in my_dict.keys():
        manual_split = k.split('_')
        manual_split[2] = manual_split[2][0:-3]
        manual_split.append((k.split())[-1])
        dict_split = key.split('_')
        dict_split[4] = dict_split[4][-2:]
        if set(manual_split).issubset(dict_split):
            auto = my_dict[key]
            break
    manual = v
    plt.ylim([0, 100])
    plt.plot(manual, label='manual')
    plt.plot(auto, label='automatic')
    plt.title(mouse)
    plt.legend()
    i+=1



#%%


by_day = {key:value for key,value in my_ctr.items() if 'D4' in key}

import numpy as np
# maximum list length
temp = []
for x in by_day.values():
    temp.append(len(x))
temp = max(temp)
# average by index
average = []
std_min, std_max = [], []
for x in range(temp):
    hi = []
    for y in by_day.values():
        try:
            hi.append(y[x])
        except:
            pass
    mean = sum(hi)/len(hi)
    std = np.std(np.array(hi))
    average.append(mean)
    std_min.append(mean-2*std)
    std_max.append(mean+2*std)
    

from matplotlib import pyplot as plt

plt.figure()
plt.plot(average)
plt.fill_between(range(0, temp, 1), std_min, std_max, color='blue', alpha=0.1)
plt.ylim([0, 100])
plt.xticks(range(0, temp, 1))
plt.title('4 days, 1s, 8 cycles with context B: D4')



#%%   
'''
# convert into percentge, half second
def data(numbers):
    total, counter = 0,0
    for num in numbers:
        if num == 0:
            counter += 1
        elif num != 0:
            if counter >= 15:
                total += counter
            counter = 0
    total += counter
    return total / len(numbers) * 100

my_dict = {}
for key, value in auto_dict.items():
    freeze = []
    for x in value:
        aye = data(x)
        freeze.append(aye)
    my_dict[key] = freeze

'''    
    
#%%

'''
def my_filter(counter):
    total = 0
    # look for clusters
    idx_list = []
    for idx,value in enumerate(counter):
        if value != 0:
            idx_list.append(idx)
    start = 0
    slice_list = []
    for idx, value in enumerate(idx_list):
        if idx == 0:
            previous = value
        else:
            current = value
            if (current - previous) > 3:
                end = idx
                slice_list.append(idx_list[start:end])
                start = idx
            previous = current
    # only_big = []
    for mini_list in slice_list:
        if len(mini_list) > 3:
            total += len(mini_list)
            # only_big.append(mini_list)
    return (len(counter) - total)

def data(numbers):
    total, counter = 0, []
    strike = 0
    for num in numbers:
        #create limit
        if len(counter) <= 15:
            limit = 3
        else: 
            limit = len(counter) * 0.2
        #reset function
        if (strike > limit) or (num > 5):
            if len(counter) > 15:
                total += len(counter)
                # res = my_filter(counter)
                # total = total + res
            counter.clear()
            strike = 0
        #append number, give strike if not 0
        if num > 5:
            strike += 1
        counter.append(num)
        
    return total / len(numbers) * 100

my_dict = {}
for key, value in auto_dict.items():
    freeze = []
    for x in value:
        aye = data(x)
        freeze.append(aye)
    my_dict[key] = freeze
'''
    
#%%

"""
# clump_filter = []
# for mini_list in only_big:
#     check = len([x for x in mini_list if x!=0]) / len(mini_list)
#     if check > 0.5:
#         clump_filter.append(mini_list)
#     else:
#         diff = []
#         for idx, value in enumerate(mini_list):
#             if idx == 0:
#                 previous = value
#             else: 
#                 current = value
#                 diff.append(current - previous)
#         average_diff = sum(diff) / (len(diff)-1)
#         if average_diff < 2:
#             clump_filter.append(mini_list) 
# clump = 0
# for my_list in clump_filter:
#     clump += (my_list[-1] - my_list[0] + 1)


# change into %

# my_dict = {}
# for key, value in auto_dict.items():
#     freeze = []
#     for x in value:
        
#         aye = len([i for i in x if i == 0]) / len(x) * 100
        
#         freeze.append(aye)
#     my_dict[key] = freeze
    
    
    
    
# convert into percentge, half second
def data(numbers):
    total, counter = 0,0
    for idx,num in enumerate(numbers):
        if num <= 1:
            counter += 1
        elif num != 0:
            if counter >= 20:
                total += counter
            counter = 0
    total += counter
    return total / len(numbers) * 100

my_dict = {}
for key, value in auto_dict.items():
    freeze = []
    for x in value:
        aye = data(x)
        freeze.append(aye)
    my_dict[key] = freeze



my_dict = {}
for key, values in auto_dict.items():
    freeze = []
    for x in values:
        total = 0
        aye,hi = [], 0
        for num in x:
            if num == 0:
                aye.append(num)
            if num != 0:
                # if len(aye) > 15:
                hi += len(aye)
                aye = []
        freeze.append(hi)
    my_dict[key] = freeze
        
        
        
    #     aye = len([i for i in x if i == 0]) / len(x) * 100
    #     freeze.append(aye)
    # my_dict[key] = freeze





# ayy = []

# for key, value in b.items():
#     freeze = []
#     for x in value:
#         lst = []
#         for idx, num in enumerate(x):
#             if num == 0:
#                 lst.append(idx)
#         i = 0
#         previous = -9999
#         yee = []
#         for z in lst:
#             current = z
#             if previous+5 >= current:
#                 yee.append(current)
#             elif previous+5 < current:
#                 if len(yee) > 14:
#                     i = i+len(yee)
#                 yee = []
#             previous = current
#         hi = i/len(x)*100
#         freeze.append(hi)
#     temp = (key, freeze)
#     ayy.append(temp)




# lst = []
# for idx, num in enumerate(value):
#     if num == 0:
#         lst.append(idx)



# i = 0
# previous = -9999
# yee = []
# for num in lst:
#     current = num
#     if previous+1 >= current:
#         yee.append(current)
#     elif previous+1 < current:
#         if len(yee) > 14:
#             i = i+len(yee)
#         yee = []
#     previous = current


"""
