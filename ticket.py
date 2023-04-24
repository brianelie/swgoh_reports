import pandas as pd
from os.path import exists
from analyze import Analyze
from pdf import PDF


class Tickets(Analyze):
    def __init__(self, date, folder, guild):
        self.dir = 'Ticket_Data/'
        self.type = 'ticket'
        self.folder = folder
        super().__init__(date, self._load_data, guild, folder)
        
    def _load_data(self):
        file_path = f'{self.folder}\\raw_data\\tickets_{self.date}.csv'
        data = pd.read_csv(file_path, index_col=0)
        test_cols = ['currentTickets','lifetimeTickets','averageTickets']
        if not all(elem in data.columns for elem in test_cols):
            return 'N/A'
        data.index = data.index.str.capitalize()
        return data
        
    def _dates_data(self):
        dates = self.data.iloc[:, 4:].replace('-', 600).astype('int64')
        return dates
    
    def avg_tickets(self):
        return round(self.data.iloc[:, 4:].stack().replace('-', 600).astype('int64').mean(), 0)
    
    def missed_ticket_days(self):
        ticket_goal = 600
        # Replacing with 600 so it doesn't count as a strike for getting 0s
        # '-' only occurs for someone who joined in the middle of the week
        # so no ticket data available prior to their join date
        dates = self._dates_data()
        dates['missed'] = dates[dates < ticket_goal].count(1)
        strike_days = dates[dates['missed'] >=
                            1]['missed'].sort_values(ascending=False)
        return pd.DataFrame(strike_days)
    
    def players_with_zeros(self):
        dates = self._dates_data()
        dates['zeros'] = dates[dates.iloc[:, :-1] == 0].count(1)
        strike_zero = self.data[dates['zeros'] >= 1].index
        return pd.DataFrame(strike_zero)

    def generate_report(self, avg_tickets):
        height = 297
        width = 210
        guild = self.guild
        title = guild + ' Ticket Report'
        ticket_report = PDF(width, height, title, guild)

        ticket_report.add_page()
        date = pd.to_datetime(self.date, format='%m%d%Y').strftime('%b %d %Y')
        ticket_report.cell(0, 32, title + ' ' + date, 0, 1, 'C')
        ticket_report.set_font('Times', size=14)
        ticket_report.cell(0, 12, 'Guild Average Tickets', 0, 1, 'C')
        ticket_report.cell(0, 6, str(avg_tickets), 0, 1, 'C')

        for plot in self.plots:
            ticket_report.print_page(plot)

        file_name = f'{self.folder}/reports/{guild} {self.type.capitalize()} Report {self.date}.pdf'
        ticket_report.output(file_name, 'F').encode('latin-1')
        return file_name
    
if __name__ == '__main__':
    date = '12202021'
    tickets = Tickets(date)
    avg_tickets = tickets.avg_tickets()
    low_tickets = tickets.count_col(5, 'averageTickets')
    missed_days = tickets.missed_ticket_days()
    zeros = tickets.players_with_zeros()
    all_tickets = tickets.count_col(50, 'averageTickets')
    tables = [('Lowest Ticket Average', low_tickets),
              ('Days with Less than 600 Tickets', missed_days),
              ('Players with Zero Tickets in a Day', zeros),
              ('Average Tickets', all_tickets)]
    tickets.dftopdf(tables)
    
    file_name = tickets.generate_report(avg_tickets)
