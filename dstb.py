from tb import TB
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import pickle
from os.path import exists

class DSTB(TB):
    def __init__(self, date, phase, folder, guild):
        self.type = 'dstb'
        super().__init__(date, phase, folder, guild)

if __name__ == '__main__':
    
    date = 'April 2022'
    
    shards = 46

    first_phase = 4
    guild = 'GSF Sigma'
    folder = 'C:\\Users\\shrim\\OneDrive\\Documents\\SWGOH Data\\GSF Sigma'
    
    tb = DSTB(date, first_phase, folder, guild)
    
    tables = []

    tb.plot_data('CM Waves', 'CM Waves Completed')
    tables.append(('Highest CM Waves', tb.count_col(
        5, 'CM Waves', ascending=False)))
    tables.append(('Lowest CM Waves', tb.count_col(
        5, 'CM Waves', ascending=True)))
    tables.append(('Highest TB Points', tb.count_col(
        5, 'TB Points', ascending=False)))
    tables.append(('Lowest TB Points', tb.count_col(
        5, 'TB Points', ascending=True)))

    tables.append(('Percent of CM Points', tb.percent_cms()))
    tables.append(('Individual CM Percents', tb.percent_cms_player('All')))
    tables.append(('Player Summary', tb.player_summary()))

    tb.dftopdf(tables)

    tb.sort_plots()

    file_name = tb.generate_report(shards)
    print('Report is in ' + file_name)