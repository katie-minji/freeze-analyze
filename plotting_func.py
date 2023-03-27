


# plot graphs, contextB as separate plot
def plotting(day_type, dictionary, title):
    
    from matplotlib import pyplot as plt
    
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
    
    
    
    
if (__name__ == '__main__'):
    print('Executing plotting_func.py\n')
    
    
    