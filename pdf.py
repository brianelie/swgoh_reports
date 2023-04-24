from fpdf import FPDF

class PDF(FPDF):
    def __init__(self, width, height, title, guild):
        super().__init__()
        self.width = width
        self.height = height
        self.title = title
        self.guild = guild
        
    def header(self):
        # Custom logo and positioning
        img_file = 'assets/'+self.guild+'.png'
        self.image(img_file, 10, 8, 10)
        self.set_font('Arial', 'B', 11)
        self.cell(self.width - 80)
        self.cell(60, 1, self.title, 0, 0, 'R')
        self.ln(20)
        
    def footer(self):
        # Page numbers in the footer
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')
        
    def page_body(self, plot):
        title = plot.split('/')[-1].split('.')[0][0:-6]
        category = plot.split('.')[0][-5:]
        h = 35
        if category == 'table':
            self.cell(0, 16, title, 0, 1,'C')
            h = 50
        self.image(plot, 15, h, self.width - 30)
        
    def print_page(self, plots):
        self.add_page()
        self.set_font('Times',size = 14)
        self.page_body(plots)

        
        
