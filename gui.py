import tkinter as tk
from tkinter import ttk
from dstb import DSTB
from lstb import LSTB
from roster import Roster
from ticket import Tickets
from tw import TW
import glob
import os
from PIL import Image
from pathlib import Path
from datetime import datetime


# GUI
class GuiMain(tk.Tk):
    # GuiMain Class
    # Instantiates an instance of a GuiMain class. root tkinter GUI

    def __init__(self):
        super().__init__()
        self.geometry("400x220")
        self.title('SWGOH Report Generator')

        # Styles
        self.configure(bg='white')
        style = ttk.Style()
        style.theme_use('alt')
        style.configure('TLabel', foreground='#000066', background='white',
                        font=('Rockwell', 10), justify='center')
        style.configure('TMenubutton', foreground='white',
                        background='#1B73D3')
        style.configure('TButton', foreground='white',
                        background='#1B73D3', font=('Verdana', 10))
        style.configure('TCheckbutton', foreground='#000066', background='white',
                        font=('Rockwell', 10))
        style.configure('TRadiobutton', foreground='#000066', background='white',
                        font=('Rockwell', 10))
        style.map('TButton', background=[('active', '#1B73D3')])
        style.map('TMenubutton', background=[('active', '#1B73D3')])
        style.map('TCheckButton', background=[('active', 'white')])

        Path('assets/').mkdir(parents=True, exist_ok=True)
        Path('plots/').mkdir(parents=True, exist_ok=True)

        guild_options = []
        target = 'assets/*.*'

        files = glob.glob(target)
        for file in files:
            guild_options.append(file.replace('\\', '.').split('.')[1])

        self.guild = tk.StringVar()
        self.guild_select = tk.OptionMenu(self, self.guild, *guild_options)
        self.guild_select.pack(side='top')

        report_options = ['TB', 'TW', 'Roster', 'Tickets']

        self.clicked = tk.StringVar()
        report_select = ttk.OptionMenu(
            self, self.clicked, report_options[0], *report_options)
        report_select.pack(side='top')
        
        ttk.Button(self, text='Select',
                   command=self.select_report).pack(side='top')
        
        ttk.Button(text='Create/Edit Guild', command=lambda: New_Guild_Window(self,
                   self.create_guild)).pack(side='top')
        self.output = tk.StringVar()
        ttk.Label(self, textvariable=self.output).pack(side='top')

    def select_report(self):
        if self.clicked.get() == 'TB':
            TB_Window(self.guild.get())
        elif self.clicked.get() == 'TW':
            TW_Window(self.guild.get())
        elif self.clicked.get() == 'Roster':
            Roster_Window(self.guild.get())
        elif self.clicked.get() == 'Tickets':
            Tickets_Window(self.guild.get())
        else:
            self.output_string.set("You didn't select an option.")

    def create_guild(self, guild_name):
        Path(f'{guild_name}/').mkdir(parents=True, exist_ok=True)
        menu = self.guild_select.children['menu']
        menu.add_command(label=guild_name,
                         command=lambda: self.guild.set(guild_name))
        self.guild_select.configure(state='active')


class New_Guild_Window(tk.Toplevel):
    def __init__(self, parent, to_main):
        super().__init__()
        self.configure(bg='white')
        self.parent = parent
        self.title('New Guild')
        self.to_main = to_main

        ttk.Label(self, text='Enter Guild Name').pack(side='top')

        self.guild_name = tk.Entry(self, width=25)
        self.guild_name.pack(side='top')

        self.guild_image = tk.StringVar()
        img_files = (('JPG Files', '*.jpg'), ('PNG Files',
                     '*.png'), ('JPEG Files', '*.jpeg'))
        guild_image_btn = tk.StringVar()
        ttk.Button(self, text='Select Guild Logo', command=lambda: openFile(
            self, self.guild_image, img_files, guild_image_btn)).pack(side='top')

        ttk.Label(self, textvariable=guild_image_btn).pack(side='top')

        ttk.Button(self, text='Create Guild',
                   command=self.save_logo).pack(side='top')

    def save_logo(self):
        guild_name = self.guild_name.get()
        print(guild_name)
        print(self.guild_image.get())
        if not entryCheck(guild_name):
            self.parent.output.set('Please enter a name for the guild')
            self.destroy()
            return
        if not entryCheck(self.guild_image.get()):
            self.parent.output.set('Please upload a logo')
            self.destroy()
            return
        file = Image.open(self.guild_image.get())
        file.save('assets/'+guild_name+'.png', format='png')
        file.close()

        self.parent.output.set('Guild successfully created!')

        self.to_main(guild_name)

        self.destroy()


class TB_Window(tk.Toplevel):
    def __init__(self, guild):
        super().__init__()
        self.folder = f'{os.getcwd()}\{guild}'
        self.configure(bg='white')
        self.title(guild + ' TB Report Parameters')
        self.guild = guild

        self.lstb_select = tk.IntVar()
        self.dstb_select = tk.IntVar()
        self.tb_select = tk.StringVar()

        ttk.Radiobutton(self, text='LSTB', variable=self.tb_select,
                        value='lstb').grid(row=1, column=1, columnspan=2)
        ttk.Radiobutton(self, text='DSTB', variable=self.tb_select,
                        value='dstb').grid(row=1, column=3, columnspan=2)

        ttk.Label(self, text='Enter Month and Year').grid(
            column=1, row=4, columnspan=2)
        months = ['January', 'February', 'March', 'April', 'May', 'June',
                  'July', 'August', 'September', 'October', 'November', 'December']
        self.month = tk.StringVar()
        self.month_select = ttk.OptionMenu(
            self, self.month, months[0], *months)
        self.month_select.grid(row=4, column=3)
        self.year = tk.Entry(self, width=10)
        self.year.grid(row=4, column=4)

        ttk.Label(self, text='Enter Character Shards').grid(
            row=5, column=1, columnspan=2)
        self.shards = tk.Entry(self, width=25)
        self.shards.grid(row=5, column=3)

        ttk.Label(self, text='Enter first phase that you want to track').grid(
            row=6, column=1, columnspan=2)
        self.phase = tk.Entry(self, width=25)
        self.phase.grid(row=6, column=3)

        # ttk.Label(self, text='Enter Sandbagged Zones').grid(
        #     column=1, row=7, columnspan=3)

        # self.sandbag = [[tk.IntVar(), tk.IntVar(), tk.IntVar()],
        #                 [tk.IntVar(), tk.IntVar(), tk.IntVar()],
        #                 [tk.IntVar(), tk.IntVar(), tk.IntVar()]]

        # ttk.Checkbutton(self, text='Phase 1 Top',
        #                 variable=self.sandbag[0][0]).grid(row=8, column=1)
        # ttk.Checkbutton(self, text='Phase 1 Mid',
        #                 variable=self.sandbag[0][1]).grid(row=9, column=1)
        # ttk.Checkbutton(
        #     self, text='Phase 1 Bottom', variable=self.sandbag[0][2]).grid(row=10, column=1)
        # ttk.Checkbutton(
        #     self, text='Phase 2 Top', variable=self.sandbag[1][0]).grid(row=8, column=2)
        # ttk.Checkbutton(self, text='Phase 2 Mid',
        #                 variable=self.sandbag[1][1]).grid(row=9, column=2)
        # ttk.Checkbutton(self, text='Phase 2 Bottom',
        #                 variable=self.sandbag[1][2]).grid(row=10, column=2)
        # ttk.Checkbutton(self, text='Phase 3 Top',
        #                 variable=self.sandbag[2][0]).grid(row=8, column=3)
        # ttk.Checkbutton(self, text='Phase 3 Mid',
        #                 variable=self.sandbag[2][1]).grid(row=9, column=3)
        # ttk.Checkbutton(
        #     self, text='Phase 3 Bottom', variable=self.sandbag[2][2]).grid(row=10, column=3)

        ttk.Button(self, text='Generate Report', command=self.report).grid(
            row=11, column=1, columnspan=2)

        self.output_string = tk.StringVar()
        output_label = ttk.Label(self, textvariable=self.output_string)
        output_label.grid(row=13, column=1, columnspan=4)

    def report(self):
        month = self.month.get()
        year = self.year.get()
        if not entryCheck(year):
            self.output_string.set('Please enter a year')
            return

        try:
            int(year)
        except:
            self.output_string.set('Please enter a valid year.')
            return

        date = month + ' ' + year
        # sandbag = [[None, None, None],
        #            [None, None, None],
        #            [None, None, None]]

        # for phase in range(3):
        #     for zone in range(3):
        #         sandbag[phase][zone] = self.sandbag[phase][zone].get()

        try:
            phase = int(self.phase.get())
            if phase < 1 or phase > 4:
                self.output_string.set(
                    'Please enter a phase number between 1 and 4')
                return
        except:
            self.output_string.set('Please enter a valid phase number')
            return

        if not entryCheck(self.tb_select.get()):
            self.output_string.set('Please select LSTB or DSTB')
            return

        if not entryCheck(self.shards.get()):
            self.output_string.set(
                'Please enter how many character shards you got')
            return
        try:
            shard_int = int(self.shards.get())
            if shard_int > 50 or shard_int < 0:
                self.output_string.set(
                    'Please enter a shard count between 0 and 50')
                return
        except:
            self.output_string.set('Please enter a number for shard count')
            return

        if self.tb_select.get() == 'lstb':
            tb = LSTB(date, phase, self.folder, self.guild)
        elif self.tb_select.get() == 'dstb':
            tb = DSTB(date, phase, self.folder, self.guild)

        error = tb.error_check()
        if error:
            self.output_string.set(error)
            return

        tables = []
        
        tb.plot_data('CM Waves','CM Waves Completed')
        tables.append(('Highest CM Waves', tb.count_col(5, 'CM Waves', ascending=False)))
        tables.append(('Lowest CM Waves', tb.count_col(5, 'CM Waves', ascending=True)))
        tables.append(('Highest TB Points', tb.count_col(5, 'TB Points', ascending=False)))
        tables.append(('Lowest TB Points', tb.count_col(5, 'TB Points', ascending=True)))
        # tables.append(('Highest Points per GP', tb.count_col(
        #     5, 'Points per GP', ascending=False)))
        # tables.append(('Lowest Points per GP', tb.count_col(
        #     5, 'Points per GP', ascending=True)))

        # avg_points_gp = tb.avg_points_per_gp()

        tables.append(('Percent of CM Points', tb.percent_cms()))
        tables.append(('Individual CM Percents', tb.percent_cms_player('All')))
        tables.append(('Player Summary', tb.player_summary()))

        tb.dftopdf(tables)

        tb.sort_plots()

        file_name = tb.generate_report(self.shards.get())
        self.output_string.set('Report is in ' + file_name)


class TW_Window(tk.Toplevel):
    def __init__(self, guild):
        super().__init__()
        self.configure(bg='white')
        self.title(guild + ' TW Report Parameters')
        self.folder = f'{os.getcwd()}\{guild}'
        self.guild = guild

        ttk.Label(self, text='Enter Date in MMDDYYYY').grid(
            row=1, column=1, columnspan=2)
        self.date = tk.Entry(self, width=25)
        self.date.grid(row=1, column=3)

        ttk.Label(self, text='Enter Opposing Guild Name').grid(
            row=2, column=1, columnspan=2)
        self.op_name = tk.Entry(self, width=25)
        self.op_name.grid(row=2, column=3)

        ttk.Button(self, text='Generate Report',
                   command=self.report).grid(row=3, column=3)

        self.output_string = tk.StringVar()
        output_label = ttk.Label(self, textvariable=self.output_string)
        output_label.grid(row=7, column=1, columnspan=3)

    def report(self):
        if not entryCheck(self.date.get()):
            self.output_string.set('Please enter a date')
            return

        try:
            datetime.strptime(self.date.get(), '%m%d%Y')
        except ValueError:
            self.output_string.set('Please enter date in [MMDDYYYY] format')
            return

        if not entryCheck(self.op_name.get()):
            self.output_string.set('Please enter an opposing guild name')
            return

        tw = TW(self.date.get(), self.folder, self.guild)

        error = tw.error_check()
        if error:
            self.output_string.set(error)
            return

        tables = []

        tw.plot_data('banner_efficiency','Banner Efficiency')
        tables.append(('Highest Banner Efficiency', tw.count_col(5, 'banner_efficiency', ascending=False)))
        tables.append(('Lowest Banner Efficiency', tw.count_col(5, 'banner_efficiency', ascending=True)))
        tw.plot_data('set_defense_stars','Defense Banners')
        tables.append(('Highest Defense Banners', tw.count_col(5, 'set_defense_stars', ascending=False)))
        tables.append(('Lowest Defense Banners', tw.count_col(5, 'set_defense_stars', ascending=True)))
        tables.append(('Highest Rogue Actions', tw.count_col(
            5, 'disobey', ascending=False)))
        tables.append(('Lowest Rogue Actions', tw.count_col(
            5, 'disobey', ascending=True)))

        tables.append(('Guild Performance', tw.guild_performance()))

        tw.dftopdf(tables)

        tw.sort_plots()

        file_name = tw.generate_report(self.op_name.get())
        self.output_string.set('Report is in ' + file_name)


class Roster_Window(tk.Toplevel):
    def __init__(self, guild):
        super().__init__()
        self.configure(bg='white')
        self.title(guild + ' Roster Report Parameters')
        self.guild = guild
        self.folder = f'{os.getcwd()}\{guild}'

        ttk.Label(self, text='Enter date in MMDDYYYY').grid(
            row=1, column=1, columnspan=2)
        self.date = tk.Entry(self, width=25)
        self.date.grid(row=1, column=3)

        ttk.Button(self, text='Generate Report',
                   command=self.report).grid(row=4, column=3)
        self.output_string = tk.StringVar()
        output_label = ttk.Label(self, textvariable=self.output_string)
        output_label.grid(row=6, column=1, columnspan=3)

    def report(self):
        if not entryCheck(self.date.get()):
            self.output_string.set('Please enter a date')
            return

        try:
            datetime.strptime(self.date.get(), '%m%d%Y')
        except ValueError:
            self.output_string.set('Please enter date in [MMDDYYYY] format')
            return

        roster = Roster(self.date.get(), self.guild, self.folder)
        error = roster.error_check()
        if error:
            self.output_string.set(error)
            return

        tables = []
        
        # include: g13, GLs, mod score, gear score
        
        roster.plot_data('G13Count', 'G13 Count')
        tables.append(('Highest G13', roster.count_col(
            5, 'G13Count', ascending=False)))
        tables.append(('Lowest G13', roster.count_col(
            5, 'G13Count', ascending=True)))
        
        roster.plot_data('UltimateGLCount', 'GLs with Ult')
        tables.append(('Highest GLs with Ult', roster.count_col(
            5, 'UltimateGLCount', ascending=False)))
        tables.append(('Lowest GLs with Ult', roster.count_col(
            5, 'UltimateGLCount', ascending=True)))
        
        roster.plot_data('ModScore', 'Mod Score')
        tables.append(('Highest Mod Score', roster.count_col(
            5, 'ModScore', ascending=False)))
        tables.append(('Lowest Mod Score', roster.count_col(
            5, 'ModScore', ascending=True)))
        
        roster.plot_data('GearScore', 'Gear Score')
        tables.append(('Highest Gear Score', roster.count_col(
            5, 'GearScore', ascending=False)))
        tables.append(('Lowest Gear Score', roster.count_col(
            5, 'GearScore', ascending=True)))

        roster.dftopdf(tables)

        roster.sort_plots()

        file_name = roster.generate_report()
        self.output_string.set('Report is in ' + file_name)


class Tickets_Window(tk.Toplevel):
    def __init__(self, guild):
        super().__init__()
        self.configure(bg='white')
        self.title(guild + ' Ticket Report Parameters')
        self.guild = guild
        self.folder = f'{os.getcwd()}\{guild}'

        ttk.Label(self, text='Enter date in MMDDYYYY').grid(
            row=1, column=1, columnspan=2)
        self.date = tk.Entry(self, width=25)
        self.date.grid(row=1, column=3)

        ttk.Button(self, text='Generate Report',
                   command=self.report).grid(row=4, column=3)
        self.output_string = tk.StringVar()
        output_label = ttk.Label(self, textvariable=self.output_string)
        output_label.grid(row=6, column=1, columnspan=3)

    def report(self):
        if not entryCheck(self.date.get()):
            self.output_string.set('Please enter a date')
            return

        try:
            datetime.strptime(self.date.get(), '%m%d%Y')
        except ValueError:
            self.output_string.set('Please enter date in [MMDDYYYY] format')
            return

        tickets = Tickets(self.date.get(), self.folder, self.guild)

        error = tickets.error_check()
        if error:
            self.output_string.set(error)
            return

        tables = []

        tables.append(('Lowest Average Tickets', tickets.count_col(
            5, 'averageTickets', ascending=True)))

        avg_tickets = tickets.avg_tickets()

        tables.append(('Days with Less than 600 Tickets',
                      tickets.missed_ticket_days()))
        tables.append(('Players with Zero Tickets in a Day',
                      tickets.players_with_zeros()))
        
        tables.append(('Average Tickets',
                      tickets.count_col(50, 'averageTickets')))

        tickets.dftopdf(tables)

        tickets.sort_plots()

        file_name = tickets.generate_report(avg_tickets)
        self.output_string.set('Report is in ' + file_name)

    def get_vals(self):
        sel_cols = []
        for i in range(len(self.selected_cols)):
            sel_cols.append([self.selected_cols[i][0], 0, 0, 0, 0])
            for j in range(4):
                sel_cols[i][j+1] = self.selected_cols[i][j+1].get()

        self.to_main(self.tb_obj, sel_cols)

        self.destroy()


def openFile(parent, file_name, filetypes, label):
    file_name.set(tk.filedialog.askopenfilename(parent=parent,
                                                title="Open file", filetypes=filetypes))
    name = file_name.get().replace('\\', '/')
    name = name.split('/')[-1]
    label.set(name)


def openFolder(parent, file_name, label):
    file_name.set(tk.filedialog.askdirectory(parent=parent,
                                             title="Select Folder"))
    name = file_name.get().replace('\\', '/')
    name = name.split('/')[-1]
    label.set(name)


def entryCheck(entry):
    if entry and entry != '':
        return True
    return False


if __name__ == '__main__':
    GuiMain().mainloop()
