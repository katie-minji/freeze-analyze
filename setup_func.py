

def dataframe():
    
    import pandas as pd
    
    data = {'day_type': ['MD','MD','MD','MD','SD','SD','SD','SD'],
            'tone_duration': ['1s','1s','10s','10s','1s','1s','10s','10s'],
            'num_of_cycles': ['8','15','8','15','8','15','8','15']}
    
    conditions = pd.DataFrame(data, index = ['condition 1','condition 2','condition 3','condition 4',
                                             'condition 5','condition 6','condition 7','condition 8'])
    return conditions



def choice(total_condition):
    
    import tkinter as tk
    total_condition = 8
    
    m = tk.Tk()
    m.geometry("250x400")
    m.title('Condition Select')
    
    tk.Label(m, text='Batch?').pack(anchor=tk.W, pady=1.5)
    Batch = tk.IntVar(m)
    tk.Radiobutton(m, text='yes', variable=Batch, value=1).pack(anchor=tk.W)
    tk.Radiobutton(m, text='no', variable=Batch, value=2).pack(anchor=tk.W)
    
    tk.Label(m, text='choose condition').pack(anchor=tk.W, pady=1.5)
    Condition = tk.IntVar(m)
    for i in range(1,total_condition+1):
        tk.Radiobutton(m, text=f'condition {str(i)}', variable=Condition, value=i).pack(anchor=tk.W)
    
    def submit():
        global batch,condition
        batch = Batch.get()
        batch = 'y' if batch==1 else 'n' 
        condition = Condition.get()
        m.quit()
        m.destroy()
        
    tk.Button(m, text="Done", command=submit).pack(anchor=tk.W, pady=8)
    m.mainloop()


    return batch, condition
    



def open_pickle(condition, pickle_loc, func_loc):
    
    import pickle
    import os
    os.chdir(pickle_loc)
    
    filename = f'condition_{condition}'
    
    # open pickle
    with open(filename, "rb") as f:
        rawdata = f.read()
    data = pickle.loads(rawdata)
    
    os.chdir(func_loc)
    
    return data




if (__name__ == '__main__'):
    print('Executing setup_func.py\n')


