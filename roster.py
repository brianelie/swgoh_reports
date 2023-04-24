import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import pickle
from os.path import exists
from analyze import Analyze
from pdf import PDF


class Roster(Analyze):
    def __init__(self, date, guild, folder):
        self.dir = 'Roster_Data/'
        self.type = 'roster'
        self.folder = folder
        super().__init__(date, self._load_data, guild, folder)
        
    def _load_data(self):
        file_path = f'{self.folder}\\raw_data\\roster_{self.date}.csv'

        data = pd.read_csv(file_path)
        test_cols = ['G13Count','ZetaCount','ModScore','GearScore']
        if not all(elem in data.columns for elem in test_cols):
            return 'N/A'
        data = data.set_index('Name')
        data['Total GP'] = data['CharacterGP'] + data['ShipGP']
        return data
    
    def generate_report(self):
        height = 297
        width = 210
        guild = self.guild
        title = guild + ' Roster Report'
        roster_report = PDF(width, height, title, guild)
        roster_report.add_page()
        date = pd.to_datetime(self.date, format = '%m%d%Y').strftime('%b %d %Y')
        roster_report.cell(0, 32, title + ' ' + date, 0, 1, 'C')
        for plot in self.plots:
            roster_report.print_page(plot)
                  
        file_name = f'{self.folder}/reports/{guild} {self.type.capitalize()} Report {self.date}.pdf'
        roster_report.output(file_name, 'F').encode('latin-1')
        return file_name
        
if __name__ == '__main__':
    date = '02222022'
    file = 'Roster_Data\\Raw Data\\roster_02222022.csv'
    guild_name = 'GSF Sigma'
    roster = Roster(date, file, guild_name)
    mod_score = roster.count_col(50, 'ModScore')
    num_gls = roster.count_col(50, 'UltimateGLCount')

    tables = [('Mod Score', mod_score), ('Number of GL Ultimates', num_gls)]
    
    roster.dftopdf(tables)
    roster.plot_data('ModScore', 'Mod Score')
    roster.plot_data('GearScore', 'Gear Score')
    roster.plot_data('G13Count', 'G13 Count')
    roster.plot_data('UltimateGLCount', 'Number of GL Ultimates')
    
    report_file = 'Roster_Data\Reports'
    file_name = roster.generate_report(report_file)
