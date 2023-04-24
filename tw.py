import pandas as pd
from analyze import Analyze
from pdf import PDF
import glob
import numpy as np

class TW(Analyze):
    def __init__(self, date, folder, guild):
        self.folder = folder
        self.type = 'tw'
        super().__init__(date, self._load_data, guild, folder)
        
    def _load_data(self):
        file_path = f'{self.folder}\\raw_data\\tw_{self.date}.csv'
        
        data = pd.read_csv(file_path)
        # print(data.iloc[:,0])
        # data[data.columns[0].split(',')] = data.iloc[:, 0].str.split(
        #     ',', expand=True)
        # data.drop(data.columns[0,1], axis=1, inplace=True)
        test_cols = ['CurrentRoundEndTime','Instance','MapStatId','Score']
        if not all(elem in data.columns for elem in test_cols):
            return 'N/A'
        data = data.drop(['Instance', 'AllyCode', 'DiscordTag',
                          'CurrentRoundEndTime'], axis=1)
        data = data.set_index('Name')

        categories = data['MapStatId'].unique()

        df = []
        for category in categories:
            df.append(data[data['MapStatId'] == category].drop(
                'MapStatId', axis=1))
            df[-1]['Score'] = pd.to_numeric(df[-1]['Score'])
            df[-1].rename({'Score': category}, axis=1, inplace=True)

        df = pd.concat(df, axis=1).fillna(0)
        df['banner_efficiency'] = round(df['attack_stars']/df['disobey'],2).fillna(0)
        df['banner_efficiency'] = df['banner_efficiency'].replace([np.inf, -np.inf], 20)
    
        col_to_round = ['attack_stars','disobey','set_defense_stars']
        df[col_to_round] = df[col_to_round].round().astype(int)
        return df
        
    def guild_performance(self):
        return self.data
        
    def top_scores(self, category, n, ascending = True):
        print(self.data[category].sort_values(ascending = ascending).head(n))

    def generate_report(self, op_name):
        height = 297
        width = 210
        guild = self.guild
        title = guild + ' TW Report'
        tw_report = PDF(width, height, title, guild)
        tw_report.add_page()
        date = pd.to_datetime(self.date, format = '%m%d%Y').strftime('%b %d %Y')
        main_title = guild + ' vs ' + op_name + ' ' + date
        tw_report.cell(0, 32, main_title, 0, 1, 'C')
        
        files = f'{self.folder}\\img\\*tw_results*'
        try:
            results = glob.glob(files)
            if len(results) > 1:
                results = None
            else:
                results = results[0]
        except:
            results = None
        if results:
            tw_report.image(results, 15,
                            70, tw_report.width - 30)
        else:
            tw_report.cell(0, 12, 'No results image available', 0, 1, 'C')
            
        
        files = f'{self.folder}\\img\\*tw_compare*'
        try:
            compare = glob.glob(files)
            if len(compare) > 1:
                compare = None
            else:  
                compare = compare[0]
        except: 
            compare = None
        if compare:
            tw_report.add_page()
            tw_report.image(compare, 60,
                            25, h = tw_report.height - 45)
        for plot in self.plots:
            tw_report.print_page(plot)
            
        folder = f'{self.folder}\\reports'
            
        file_name = folder + '/' + guild + ' ' + self.type.upper() + ' Report ' + \
            self.date + '.pdf'
        tw_report.output(file_name, 'F').encode('latin-1')
        return file_name
        
if __name__ == '__main__':
    date = '06092022'
    tw = TW(date)
    guild_performance = tw.guild_performance()
    banner_efficiency = tw.count_col(10, 'banner_efficiency')
    defense_stars = tw.count_col(10, 'set_defense_stars')
    
    tables = [('Guild Performance', guild_performance),
              ('Lowest Banner Effiicency', banner_efficiency),
              ('Lowest Defensive Banners', defense_stars)]
    tw.dftopdf(tables)
    
    tw.plot_data('set_defense_stars', 'Defensive Banners')
    tw.plot_data('banner_efficiency', 'Banner Efficiency')
    file_name = tw.generate_report()
    
