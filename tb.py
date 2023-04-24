import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import pickle
import glob
import os
from os.path import exists
from analyze import Analyze
from pdf import PDF


class TB(Analyze):
    def __init__(self, date, phase, folder, guild):
        self.folder = folder
        self.date = date
        super().__init__(date, self._load_data, guild, folder)
        self.ground_missions, self.ship_missions, self.max_ground, self.max_ships = self._calc_missions()
        self.all = self.data
        if not isinstance(self.error, str):
            self._needed_phases(phase)
            
    def _calc_missions(self):
        ground_missions = {1: [], 2: [], 3: [], 4: []}
        ship_missions = {1: [], 2: [], 3: [], 4: []}
        self.ground_cols = {1: [], 2: [], 3: [], 4: []}
        self.ship_cols = {1: [], 2: [], 3: [], 4: []}

        for col in self.data.columns:
            try:
                phase, zone, points, num = col.split(' ')
                phase = int(phase[1])
                zone = zone.lower()
                points = [int(x) for x in points.split('_')]
                points.insert(0, 0)
                num = num[1]
                if zone == 'ground':
                    ground_missions[phase].append(points)
                    self.ground_cols[phase].append(col)
                elif zone == 'fleet':
                    ship_missions[phase].append(points)
                    self.ship_cols[phase].append(col)
            except:
                pass

        max_ground = {1: 0, 2: 0, 3: 0, 4: 0}
        max_ships = {1: 0, 2: 0, 3: 0, 4: 0}

        for phase in ground_missions:
            for cm in ground_missions[phase]:
                max_ground[phase] += cm[-1]

        for phase in ship_missions:
            for cm in ship_missions[phase]:
                max_ships[phase] += cm[-1]
        
        return ground_missions, ship_missions, max_ground, max_ships
        
    def _load_data(self):
        file = f'{self.folder}\\raw_data\\{self.type.upper()} {self.date}\\phase_all.csv'
        data = pd.read_csv(file, index_col=0).drop_duplicates().replace(
            ' ?', 0).fillna(0)
        return data 
    
    def _needed_phases(self, needed_phase):
        self.data['TB Points'] = 0
        self.data['CM Waves'] = 0
        
        for col in self.data.columns[1+needed_phase:6]:
            self.data['TB Points'] += self.data[col]
            
        for col in self.data.columns[10+needed_phase:15]:
            self.data['CM Waves'] += self.data[col]
            
        self.data = self.data[['TB Points', 'CM Waves']]

    def _percents(self, df, phase):
        
        df['ground'] = 0
        df['ship'] = 0
        
        for num, col in enumerate(self.ground_cols[phase]):
            cm = self.ground_missions[phase][num]
            for name in df['ground'].index:
                df.loc[name, 'ground'] += cm[int(df.loc[name, col])]
                
        for num, col in enumerate(self.ship_cols[phase]):
            cm = self.ship_missions[phase][num]
            for name in df['ship'].index:
                df.loc[name, 'ship'] += cm[int(df.loc[name, col])]
        
        ground_perc_name = f'ground_perc_{phase}'
        ship_perc_name = f'ship_perc_{phase}'

        df[ground_perc_name] = round((df['ground']/self.max_ground[phase])*100, 0)

        df[ship_perc_name] = round((df['ship']/self.max_ships[phase])*100, 0)

        ground_perc = df[ground_perc_name].mean()
        ship_perc = df[ship_perc_name].mean()

        return (ground_perc, ship_perc)

    def percent_cms(self):
        perc = list()

        for i in range(1,5):
            (ground_perc, ship_perc) = self._percents(self.all, i)
            if math.isnan(ship_perc):
                ship_perc = 0
            if math.isnan(ground_perc):
                ground_perc = 0

            perc.append([str(ground_perc) + '%', str(ship_perc) + '%'])

        perc_points = pd.DataFrame(perc, index=['Phase 1', 'Phase 2', 'Phase 3', 'Phase 4'],
                                   columns=['Ground', 'Ships'])
        return perc_points.round(2)

    def percent_cms_player(self, player):
        player_perc = pd.DataFrame()

        for i in range(1,5):
            ground_name = 'P' + str(i) + 'G'
            ship_name = 'P' + str(i) + 'S'
            player_perc[ground_name] = self.all[f'ground_perc_{i}']
            player_perc[ship_name] = self.all[f'ship_perc_{i}']
        if player == 'All':
            return player_perc
        else:
            return player_perc.loc[player]
        
    def avg_cm_waves(self):
        return self.data['CM Waves'].mean()

    def player_summary(self):    
        soln =  self.data.sort_values(by=['TB Points'], ascending=False)
        return soln
    
    def generate_report(self, shards):
        height = 297
        width = 210
        guild = self.guild
        title = guild + ' ' + self.type.upper() + ' Report'

        if self.type == 'lstb':
            char_shards = 'KAM'
        else:
            char_shards = 'Wat'
            
        results_img = f'{self.folder}\\img\\*tb_results*'
        try:
            results = glob.glob(results_img)
            if len(results) > 1:
                results = None
            else:
                results = results[0]
        except:
            results = None

        tb_report = PDF(width, height, title, guild)
        
        tb_report.add_page()
        date = pd.to_datetime(self.date, format = '%B %Y').strftime('%b %Y')
        tb_report.cell(0, 32, title + ' ' + date, 0, 1, 'C')
        tb_report.cell(0, 12, char_shards + ' Shards: ' + str(shards), 0, 1, 'C')
        tb_report.cell(0, 12, 'Average CM Waves: ' +
                       str(self.avg_cm_waves()), 0, 1, 'C')
        if results:
            tb_report.image(results, 15, 100, tb_report.width - 30)
        else:
            tb_report.cell(0, 12, 'No results image available', 0, 1, 'C')
            
        for plot in self.plots:
            tb_report.print_page(plot)
        file_name = f'{self.folder}/reports/{guild} {self.type.upper()} Report {self.date}.pdf'
        tb_report.output(file_name, 'F').encode('latin-1')
        return file_name
