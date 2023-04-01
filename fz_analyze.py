
# check for missing/excess presentation
for i,x in master_dict.items():
    if len(x['timestamps']) not in [16, 9,21]:
        print(i)
        print(len(x['timestamps']))
        print()
        
# pick out outliers on purpose
hi = {}
for i,x in auto_dict.items():
    if 'wt8' in i:
        pass
    else:
        hi[i] = x

auto_dict = hi
        

#%%


import pickle
import os
os.chdir(r'G:\My Drive\lab\pickle\fz_score\2023_03_31__17_11_20')

# save pickle
with open('master.pkl', 'wb') as handle:
    pickle.dump(master_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)


#%%

# open file from fz_score

import pickle
import os
os.chdir(r'G:\My Drive\lab\pickle\fz_score\2023_03_31__11_57_20')

# open pickle
with open("master.pkl", "rb") as f:
    rawdata = f.read()
    
master_dict = pickle.loads(rawdata)
        
#%%

# extract only fz and dictionary of {mouse: [[pxl shift by index],[],[]]}

# after
def after(my_dict):
    indexed = {}
    for mouse, value in my_dict.items():
        fz = value['pxl_shift']   #pixel shift
        idx = value['on_off_idx']  #index of light on and off
        fz_list = []  
        fz_list.append(fz[0:idx[0][0]])  #append initial delay, 0 to first light
        for i in range(len(idx)-1):
            fz_list.append(fz[idx[i][1]:idx[i+1][0]])  #for each presentation index, from off to next presentation on
        fz_list.append(fz[idx[len(idx)-1][1]:])  #last, until end of vid
        # for x in idx:  #for each presentation index
        #     fz_list.append(fz[x[1]:x[1]+3600])  #light off index to light off + 60s
        indexed[mouse] = fz_list  #append to dictionary
    return indexed

indexed = after(master_dict)


# # between
# def between(my_dict):
#     indexed = {}
#     for mouse, value in my_dict.items():
#         con = mouse.split()[0][-1]
#         if (con == '3') or (con == '4') or (con == '7') or (con == '8'):  #if 10s tone
#             fz = value['pxl_shift']   #pixel shift
#             idx = value['on_off_idx']  #index of light on and off
#             fz_list = []  
#             fz_list.append(fz[0:idx[0][0]])  #append initial delay, 0 to first light
#             for x in idx:  #for each presentation index
#                 fz_list.append(fz[x[0]:x[1]])  #light on index to light off
#             indexed[mouse] = fz_list  #append to dictionary
#     return indexed

# indexed = between(master_dict)


#%%



# convert into percentage, half second , 1/3

def fz_to_percentage(auto_dict):
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



# extract one of (freeze_only,area_list, timestamps) from final_dict
def extract_fz_only(my_input, my_type):
    mouse_list = []
    auto_dict = {}
    for mouse in my_input:
        mouse_list.append(mouse)
    for mouse in mouse_list:
        auto_dict[mouse] = my_input[mouse][my_type]
    return auto_dict



def dataframe():
    
    import pandas as pd
    
    data = {'day_type': ['MD','MD','MD','MD','SD','SD','SD','SD'],
            'tone_duration': ['1s','1s','10s','10s','1s','1s','10s','10s'],
            'num_of_cycles': ['8','15','8','15','8','15','8','15']}
    
    conditions = pd.DataFrame(data, index = ['con1','con2','con3','con4',
                                             'con5','con6','con7','con8'])
    return conditions


def reduce_master(auto_dict, my_time, keys):
    
    import pandas as pd
    
    # make framework dictionary: {condition: {FS:0, ctr:0}}
    reduced_dict = {}
    for i in range(1,9):
        con = 'con'+str(i)
        _ = keys.loc[con]
        reduced_dict[con] = {'info': (_['day_type'], _['tone_duration'],
                                      _['num_of_cycles']), 'FS':{}, 'ctr':{}}
    
    # combine reduced fz and timestamps into df
    for vid, perc in auto_dict.items():  #for individual video in fz_perc 
       
        # arrange specifics of video
        day = vid.split()[1]
        other = vid.split()[0]
        other = other.split('_')
        mouse = "_".join([other[0],other[1]])
        ctr_or_fs = other[2]
        condition = other[3]
        
        # make dataframe of fz and timestamps and append to reduced dict
        d = {'Freeze(%)': perc, 'Timestamps': my_time[vid]}
        df = pd.DataFrame(data=d)
        
        temp = reduced_dict[condition][ctr_or_fs]
        if mouse in temp.keys():
            temp[mouse].update({day: df})
        else:
            temp.update({mouse: {day: df}})
            
    return reduced_dict


auto_dict = fz_to_percentage(indexed)
my_time = extract_fz_only(master_dict, 'timestamps')
keys = dataframe()
reduced_dict = reduce_master(auto_dict, my_time, keys)



#%%



# individual plotting

def day_type_and_title(info, condition):
    if info[0] == 'MD':
        day_type = ['D1', 'D2', 'D3', 'D4']
    else:  #if single day
        day_type = ['D1', 'D2']
    #for title
    tone = info[1]
    cycle = info[2]
    title = f'{info[0]}, {tone}, {cycle}-cycles ({condition})'
    return day_type, title


# segregate by days, dictionary output
def segregate_by_day(day_type, my_input):
    
    dictionary = {}
    #get daylist, setup dictionary
    for day in day_type:
        dictionary.update({day: {}})
    # separate by day
    for mouse in my_input:
        for by_day in my_input[mouse]:  #for each mouse, filter specific day
            fz_rate = my_input[mouse][by_day]['Freeze(%)'].tolist()  #extract only fz, convert to list
            dictionary[by_day].update({mouse: fz_rate})  #add to dictionary
            
    return dictionary


def my_max_length(by_day):
    temp = []
    for perc in by_day.values():  #for list of perc in day[mouse]
        temp.append(len(perc))
    temp2 = max(temp)
    # average by index
    iaverage = []
    for x in range(temp2):
        hi = []
        for mouse in by_day.values():
            try:    #bc loop max length, some list might throw idx out of range
                hi.append(mouse[x])  #add perc of mouse at x presentation
            except:
                pass
        iaverage.append(sum(hi)/len(hi))  #average for each presentation
    return temp2, iaverage


def plotting(day_type, dictionary, title):

    from matplotlib import pyplot as plt

    i = 0
    for day, by_day in dictionary.items():  #loop through D1, D2....
        max_length, average = my_max_length(by_day)  #max presentation, average for each presentation
        
        if day == day_type[-1]:  #if context B
            fig = plt.figure()
            over = 0
            for name, individual in by_day.items():    
                plt.plot(range(len(individual)),individual, label=name)
                if len(individual) < max_length:    
                    plt.vlines(x=len(individual),ymin=-3,ymax=105, colors='#bf80ff')
                    over += 1
            under = over
            over = len(by_day.values()) - over
            if under == 0:
                plt.title(f'{title}: context B',fontsize=15)
            else:
                plt.title(f'{title}: context B | {under} : {over}',fontsize=15)
            plt.ylim([-3,105])
            plt.xticks(range(0, max_length, 1))
            plt.xlabel('Presentation #',fontsize=13)
            plt.ylabel('Freezing Percentage',fontsize=13)
            plt.legend(bbox_to_anchor=(1.3, 1.0),fontsize=12)
            plt.tight_layout(pad=1.5)
        
        else:   #if context A
            pass
        i+=1
        


graphs = []
for con in reduced_dict:
    info = reduced_dict[con]['info']
    for condition in ['FS']:
        day_type, title = day_type_and_title(info, condition)
        my_con = reduced_dict[con][condition]  #mouse dict within same condition and (FS/ctr)
        if bool(my_con) == False:   #if we don't have data, dictionary empty
            pass
        else:
            graphs.append([con, condition])     #condition + fs/ctr that we have at least one data point
            dictionary = segregate_by_day(day_type, my_con)
            plotting(day_type, dictionary, title)
      
print('')
print(graphs)  #print data we have

