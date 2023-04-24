import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.transforms
from os.path import exists
import os
import shutil

class Analyze():
    def __init__(self, date, load_data, guild, folder):
        self.error = None
        self.date = date
        self.guild = guild
        self.data = load_data()
        if isinstance(self.data, str):
            self.error = 'Please input a valid ' + self.type + ' dataset.'
        self.plots_dir = f'{folder}\plots'
        self.plots = []
        self._plots_folder()
        
    def _plots_folder(self):
        # Delete folder if exists and create it again
        try:
            shutil.rmtree(self.plots_dir)
            os.mkdir(self.plots_dir)
        except FileNotFoundError:
            os.mkdir(self.plots_dir)
        
    def get_cols(self):
        return self.data.columns
    
    def count_col(self, n, category, ascending = True):
        return self.data[category].sort_values(ascending = ascending).head(n)

    def dftopdf(self,tables):
        for table in tables:
            name, df = table
            
            df = pd.DataFrame(df)
            
            table = plt.table(cellText=df.values,
                            colLabels=df.columns,
                            rowLabels=df.index,
                            loc='center')

            plt.axis('off')
            plt.grid('off')

            #prepare for saving:
            # draw canvas once
            plt.gcf().canvas.draw()
            # get bounding box of table
            points = table.get_window_extent(plt.gcf()._cachedRenderer).get_points()
            # add 10 pixel spacing
            points[0, :] -= 10
            points[1, :] += 10
            # get new bounding box in inches
            nbbox = matplotlib.transforms.Bbox.from_extents(points/plt.gcf().dpi)
            # save and clip by new bounding box
            fname = self.plots_dir + '/' + name + '_table.png'
            plt.savefig(fname, bbox_inches=nbbox, )
            self.plots.append(fname)
            plt.close()

    def _save_data(self, category):
        roster = bool(self.type == 'roster')
        
        file = f'{self.folder}/data/' + self.guild + self.type + category + '.pkl'
            
        # if tw or tickets:
        #     local = self.data[[category]]
        # else:
        #     local = self.data[['Total GP', category]]
            
        if roster:
            local = self.data[['Total GP', category]]
        else:
            local = self.data[[category]]
    
        if not exists(file):
            with open(file, 'wb') as f:
                all = {}
                all[self.date] = local
                soln = all
                pickle.dump(all, f)

        else:
            with open(file, 'rb') as f:
                all = pickle.load(f)

            all[self.date] = local

            soln = all

            with open(file, 'wb') as f:
                pickle.dump(all, f)

        return soln
    
    def plot_data(self, name_category, main_title):
        all_data = self._save_data(name_category)
        tb = bool(self.type == 'dstb' or self.type == 'lstb')
        roster = bool(self.type == 'roster')

        keys = all_data[self.date].index

        df = pd.DataFrame([], index=keys, columns=all_data.keys())
        for date in all_data:
            df[date] = all_data[date][all_data[date].index.isin(
                keys)][name_category]

        if tb:
            df = df[sorted(
            df.columns, key=lambda x: pd.to_datetime(x, format='%B %Y'))]
        else:
            df = df[sorted(
            df.columns, key=lambda x: pd.to_datetime(x, format='%m%d%Y'))]
        
        y_limits = (df.min().min(), df.max().max())
        avg = df[self.date].mean(axis=0)

        if roster:
            df['GP'] = all_data[self.date]['Total GP']
            df = df.sort_values(by=['GP'])
            n = 12
            df = np.array_split(df, n)
            gp_ranges = []
            for group in df:
                low = group['GP'].iloc[0]
                high = group['GP'].iloc[-1]
                gp_ranges.append((low, high))
                group.drop('GP', axis=1, inplace=True)
        else:
            n = 12
            df = np.array_split(df, n)

        n = 0
        x_axis = 4
        y_axis = 3
        fig, axs = plt.subplots(x_axis, y_axis, figsize=(30,30))
        
        plt.setp(axs, ylim=y_limits)
        for group in df:
            i = int(n/y_axis)
            j = n % y_axis
            for name in group.index:
                axs[i, j].plot(group.columns, group.loc[name], label=name)
            axs[i, j].axhline(y=avg, color='k', linestyle='dotted')
            if roster:
                title = 'GP Range ' + str(gp_ranges[n][0]) + '-'+ str(gp_ranges[n][1])
                axs[i, j].set_title(title)
            axs[i, j].tick_params(axis='x', rotation=45)
            axs[i, j].legend()
            n += 1
            
        fig.tight_layout()
            
        fname = self.plots_dir + '/' + name_category + '_graph.jpg' 
        plt.suptitle(main_title, fontsize = 36)
        plt.savefig(fname, bbox_inches='tight', pad_inches=1)
        self.plots.append(fname)
        plt.close()

    def _sortCols(self, element):
        # sorts by the last 5 characters before the file type
        # last 5 will always be either "table" or "graph"
        return element.split('.')[0][-5:]
    
    def sort_plots(self):
        self.plots.sort(key=self._sortCols, reverse=True)

    def error_check(self):
        if self.error:
            return self.error
