
# =============================================================================
#
#              	day_type	tone_duration	num_of_cycles
# condition 1	    MD	         1s	             8
# condition 2	    MD	         1s	             15
# condition 3	    MD	         10s	         8
# condition 4	    MD	         10s	         15
# condition 5	    SD	         1s	             8
# condition 6	    SD	         1s	             15
# condition 7	    SD	         10s	         8
# condition 8	    SD	         10s	         15
#
#
# =============================================================================


# =============================================================================

# change directory to where codes are for freezing data analyzing
import os
func_loc = r'Z:\Soo B\Katie\codes\mine\complete\fz_analyze\functions'
pickle_loc = r'Z:\Soo B\Katie\projects\freezing_score\pickle_files'
os.chdir(func_loc)

total_condition = 8

# =============================================================================
# =============================================================================

import setup_func as se

# data frame of the conditions (1-8) and their attributes
conditions_df = se.dataframe()  #returns condition specifics

# choose if want to batch, and choose condition
batch, condition = se.choice(total_condition)  #returns batch and condition

# open pickle files (access data)
main_data = se.open_pickle(condition, pickle_loc, func_loc)


# =============================================================================
# =============================================================================

import fz_to_perc_func as fp

# extract one of (freeze_only,area_list, timestamps) from main_data
# use freeze_only for the fz_analyzing purpose (can run other lines as well)
fz_only = fp.extract_fz_only(main_data, 'freeze_list')

# fz_only to percentages
fz_only = fp.to_percentage(fz_only)

# =============================================================================
# =============================================================================

import pl_setup_func as su
import plotting_func as pl

# separate by condition, look for ctr or FS in name
# special for condition 1 and 5, manual add (syntax wasn't fixed)
my_fs, my_ctr = su.ctr_fs_separate(fz_only, condition)

# Plotting FS first:    
# plotting set up (based on condition)
day_type, dictionary, title = su.set_up(conditions_df, condition, my_fs, 'FS')
# executing graphs
pl.plotting(day_type, dictionary, title)

# Plotting ctr next:    
# plotting set up (based on condition)
day_type, dictionary, title = su.set_up(conditions_df, condition, my_ctr, 'ctr')
# executing graphs
pl.plotting(day_type, dictionary, title)

# =============================================================================



