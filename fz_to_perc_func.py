

# extract one of (freeze_only,area_list, timestamps) from final_dict
def extract_fz_only(my_input, my_type):
    
    mouse_list = []
    auto_dict = {}
    for mouse in my_input:
        mouse_list.append(mouse)
    for mouse in mouse_list:
        auto_dict[mouse] = my_input[mouse][my_type]
        
    return auto_dict




# convert into percentage, half second , 1/3
def to_percentage(auto_dict):
    
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




if (__name__ == '__main__'):
    print('Executing fz_to_perc_func.py\n')
    


