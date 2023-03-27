

# separate by condition, look for ctr or FS in name
# special for condition 1 and 5
def ctr_fs_separate(my_dict, condition):
    
    if condition == 1:
        my_fs = {key: value for key,value in my_dict.items() if not ('833_N' in key or '833_RL' in key or '868_N' in key)}
        my_ctr = {key: value for key,value in my_dict.items() if ('833_N' in key or '833_RL' in key or '868_N' in key)}
    
    elif condition == 5:
        my_fs = {key: value for key,value in my_dict.items() if not ('833_R' in key)}
        my_ctr = {key: value for key,value in my_dict.items() if ('833_R' in key)}
    
    else:
        my_fs = {key: value for key,value in my_dict.items() if not ('ctr' in key)}
        my_ctr = {key: value for key,value in my_dict.items() if ('ctr' in key)}
        
    return my_fs, my_ctr





# plotting set up (based on condition)
def set_up(conditions_df, condition, type_input, fs_or_ctr):
    
    a = conditions_df.loc['condition '+str(condition)]
    
    # day type
    if a['day_type'] == 'MD':
        day_type = ['D1', 'D2', 'D3', 'D4']
        day = 'Multi-day'
    elif a['day_type'] == 'SD':
        day_type = ['D1', 'D2']
        day = 'Single-day'

    # for title
    tone = a['tone_duration']
    cycle = a['num_of_cycles']
    title = f'{day}, {tone}, {cycle} cycles ({fs_or_ctr})'

    # segregate by days, dictionary output
    dictionary = {}
    for x in day_type:
        temp = {key:value for key,value in type_input.items() if x in key}
        dictionary[x] = temp

    return day_type, dictionary, title





if (__name__ == '__main__'):
    print('Executing pl_setup_func.py\n')
    
    
    
    
