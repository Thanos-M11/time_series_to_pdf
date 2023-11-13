import random
from datetime import date, datetime
from fpdf import FPDF
from fpdf.enums import XPos, YPos
from statistics import median, mean


MONTHS = range(1, 13)
DAYS: list = [7, 14, 21, 28]

class Sales:
    def __init__(self, salesdate, sales):
        self.salesdate = datetime.strptime(salesdate, "%d-%m-%Y").date()
        self.sales = sales

    @property
    def year(self):
        return self.salesdate.year
    
    @property
    def month(self):
        return self.salesdate.month
    
    @property
    def qrt(self):
        return ((self.month - 1) // 3) + 1
 
    def __str__(self):
        return f"{self.salesdate}\t{self.sales:>10}"


class PDF(FPDF):
    def header(self):
        self.image('logo-harvard.png', 10, 8, 30)
        self.set_font('helvetica', 'B', 16)
        self.cell(0, 10, self.title, border=False, new_x='LMARGIN', new_y='NEXT',  align='C')

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 10)
        self.alias_nb_pages()
        self.cell(0, 10, "Final Python Project on EDX CS50P - Thanos-M11 - 2023", align='L')
        self.cell(0, 10, f"Page {self.page_no()} / {{nb}}", align='R')


    def draw_line(self):
        self.cell(0,0, border="B", new_x=XPos.LMARGIN, new_y=YPos.NEXT)


def main():
    
    years = input("Enter the number of years between 2 - 8 for analysis: ")
    if validate_years(years):
        YEARS: int = int(years)
        sales: list[Sales] = random_time_series(YEARS)
        sales_m: dict = sales_by_month(sales)
        sales_q: dict = sales_by_qrt(sales)
        change_m: dict = get_change_on_base(sales_m)
        change_q: dict = get_change_on_base(sales_q)
        si_m: dict = get_seasonal_index(sales_m)
        si_q: dict = get_seasonal_index(sales_q)
        create_pdf(sales_q, si_q, change_q, "sales_q.pdf")
        create_pdf(sales_m, si_m, change_m, "sales_m.pdf")


def validate_years(years) -> bool:
    """Validates the input of the year to be an integer and between 2 - 8"""    
    try:
        assert years.isnumeric(), "Year value must be numeric"
        assert int(years) in range(2, 9), "Year number must be between 2 - 8"
        return True
    except AssertionError as msg:
        print(msg)
        return False


def random_time_series(n_years: int=5) -> list[Sales]:
    """Creates a random 4 times per month sales demand for n years"""    
    random.seed(100)
    journal: list[Sales] =  []
    start_year = datetime.now().year - n_years
    for year in list(range(start_year, n_years + start_year)):
        for month in MONTHS:
            for day in DAYS:
                journal.append(
                        Sales(
                            salesdate=f"{day:02}-{month}-{year}", 
                            sales=random.randrange(20, 100)
                        )
                    )
    return journal


def sales_by_qrt(sales_ptrn: list[Sales]) -> dict[int, dict[int, int | float]]:
    """creates a dict with qrt totals per year"""
    sales: dict = dict()
    for line in sales_ptrn:
        if line.year not in sales:
            sales[line.year] = {}
        if line.qrt not in sales[line.year]:
            sales[line.year][line.qrt] = 0
        sales[line.year][line.qrt] += line.sales 
    return sales


def sales_by_month(sales_ptrn: list[Sales]) -> dict[int, dict[int, int | float]]:
    """Creates a dict with monthly totals per year"""
    sales: dict = dict()
    for line in sales_ptrn:
        if line.year not in sales:
            sales[line.year] = {}
        if line.month not in sales[line.year]:
            sales[line.year][line.month] = 0
        sales[line.year][line.month] += line.sales 
    return sales


def sales_format_is_valid(sales_report: dict) -> bool:
    """Validates the dictionary format. Returns True if only all 7 checks will pass"""

    #1. check if sales report is a dictionary
    if not isinstance(sales_report, dict): return False
        
    #2. check if the number of keys are more than one
    if not len(sales_report) > 1: return False
    
    #3. check if all 1st level keys are integers
    temp3: list = [isinstance(key, int) for key in sales_report]
    if not len(set(temp3)) == 1: return False

    #4. check if the first level values are of type dict
    temp4: list = [isinstance(value, dict) for value in sales_report.values()]
    if not len(set(temp4)) == 1: return False

    # 5. check if the keys of the 2nd level are int
    temp5: list = []
    for values in sales_report.values():
        for key in values:
            temp5.append(isinstance(key, int))
    if not len(set(temp5)) == 1: return False

    # 6. check if the values of the 2nd level are int or floats
    temp6: list = []
    for values in sales_report.values():
        for value in values.values():
            temp6.append(isinstance(value, float | int))
    if not len(set(temp6)) == 1: return False

    #7. checks if the values of the 2nd level are of equal length
    temp7 = list(map(lambda x: len(x), sales_report.values()))
    if not len(set(temp7)) == 1: return False

    return True



def get_seasons(sales: dict) -> int:
    """Returns the number of seasons within a sales dictionary, usually qrts or months"""
    if sales_format_is_valid(sales):
        seasons = []
        for s in sales.values():
            seasons.append(len(s)) 
        return set(seasons).pop()
    return 0


def get_seasonal_index(sales: dict) -> dict[int, float]:
    """returns the seasonal index of sales"""
    if sales_format_is_valid(sales):
        si = dict()
        for s in range(1, get_seasons(sales) + 1):
            temp = []
            for y in sales:
                temp.append(sales[y][s] / mean(sales[y].values()))
            si[s] = round(sum(temp) / len(temp), 4)
        return si
    return {}


def get_delta(list1: list, list2: list) -> dict[int, float]:
    """returns the change between two float elements of a list"""
    if len(list1) != len(list2):
        return {}
    change_list = list(map(lambda x, y: (y - x) / x, list1, list2))
    return {key: round(value, 2) for key, value in enumerate(change_list, 1)}
    

def format_percent(val: float) -> str:
    """formats a float value as a percent with two decimals and adds a '+ / -' sign in front"""
    if not isinstance(val, float | int):
        return "Value is not a float or integer"
    if val > 0:
        sign = '+'
    elif val == 0:
        sign = ''
    else:
        sign = '-'
    return f"{sign}{abs(val*100):.1f}%"


def get_change_on_base(report: dict) -> dict:
    """returns a dictionary with the changes between periods per year"""
    if sales_format_is_valid(report):
        periods = sorted(list({period for period in report}))
        delta: dict = {}
        for period in range(1, len(periods)):
            base_year = report[periods[0]].values()
            delta[periods[period]] = get_delta(base_year, report[periods[period]].values())
        return delta
    return {}


def create_pdf(sales: dict, seasonal_index: dict, changes: dict, filename: str):
    """Creates a pdf report on sales and changes in table format"""
    
    # counts number of years from the report
    n_years = len([years for years in sales])
    if n_years not in range(2, 9):
        return "The report can display data between 2 and 8 years only"

    # changes pdf orientation if the number of years is > 5
    if n_years > 5:
        pdf = PDF('L', 'mm', 'A4')
    else:
        pdf = PDF('P', 'mm', 'A4')
    
    # add page
    pdf.title = "Sales - Data Analysis"
    pdf.set_auto_page_break(auto=True, margin = 15)
    pdf.add_page()

    # set default width of cells, height
    width:int = 16
    height:int = 8
    gap: int = 3

    # calculate cell width of sales and change
    sales_w = len([years for years in sales]) * width
    change_w = len([years for years in changes]) * width
    seasonal_index_w = width
    
    # calculate left and right margin according to number of years to display
    calc_margin = (pdf.w - sales_w - change_w - seasonal_index_w - gap * 2 - width) / 2
    pdf.set_left_margin(calc_margin)
    pdf.set_right_margin(calc_margin) 

    def print_table_head():
        pdf.set_font('helvetica', 'B', 11)
        pdf.set_xy(pdf.get_x() + width, pdf.get_y())
        pdf.cell(sales_w, height + 3, 'Sales', border="B", align='C')
        pdf.set_x(pdf.get_x() + gap)
        pdf.cell(seasonal_index_w, height + 3, 'SI', border="B", align='C')
        pdf.set_x(pdf.get_x() + gap)
        pdf.cell(change_w, height + 3, 'Change on Base', border="B", new_x=XPos.LEFT, new_y=YPos.NEXT, align='C')
        pdf.set_font('helvetica', 'BI', 10)
        pdf.cell(change_w, height, f'Base is Year {list(sales.keys())[0]}', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='R')
    
    def print_year_headings():
        pdf.set_y(pdf.get_y() + 2)
        pdf.set_font('helvetica', 'B', 11)
        pdf.cell(width, height + 3, 'Period', align='L')
        for year in sales:
            pdf.cell(width, height + 3, str(year), align='C')
        pdf.set_x(pdf.get_x() + gap + width + gap)

    def print_change_headings():
        for ch in changes:
            pdf.cell(width, height + 3, str(ch), align='C')
        pdf.ln(10)

    def print_table_data():
        # get the number of seasons
        seasons = get_seasons(sales)
        if seasons == 4:
            periods = ['Qrt1', 'Qrt2', 'Qrt3', 'Qrt4']
        else:
            periods = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

        pdf.set_font('helvetica', '', 11)
        for period in range(1, seasons + 1):
            pdf.set_text_color(0, 0, 0)
            pdf.set_font('helvetica', 'B', 11)
            pdf.cell(width, height, str(periods[period - 1]), border=0, align="L")
            # insert a lightgray backcolor font
            if period % 2 == 0:
                pdf.set_fill_color(237, 237, 237)
            else:
                pdf.set_fill_color(252, 252, 252)
            for year in sales:
                pdf.set_font('helvetica', '', 11)
                pdf.cell(width, height, str(sales[year][period]), border=0, align='R', fill=True)
            
            # seasonal index column settings
            pdf.set_text_color(255, 0, 0)
            pdf.set_font('helvetica', 'BI', 10)
            pdf.set_x(pdf.get_x() + gap)
            pdf.cell(width, height, f"{seasonal_index[period]:.3f}", border=0, align='C', fill=True)
            pdf.set_x(pdf.get_x() + gap)

            pdf.set_text_color(0, 0, 255)
            pdf.set_font('helvetica', '', 11)
            for ch in changes:
                pdf.cell(width, height, format_percent(changes[ch][period]), border=0, align='R', fill=True)
            pdf.ln()
        
    def print_totals_line():
        pdf.set_text_color(0, 0, 0)
        pdf.set_font('helvetica', 'B', 12)
        pdf.set_y(pdf.get_y() + 2)
        pdf.set_font('helvetica', 'B', 11)
        pdf.cell(width, height + 3, 'Totals', align='L')
        
        # print sum of months
        year_change = []
        for year in sales:
            pdf.cell(width, height + 3, f"{sum(sales[year].values())}", align='R')
            year_change.append(sum(sales[year].values()))
        
        pdf.set_x(pdf.get_x() + gap + width + gap)
        
        # print change on sums
        pdf.set_text_color(0, 0, 255)
        for year in range(1, len(year_change)):
            ch = f"{format_percent((year_change[year] - year_change[year - 1]) / year_change[year - 1])}"
            pdf.cell(width, height + 3, ch, align='R')

    def print_mean():
        pdf.ln()
        pdf.set_text_color(0, 0, 0)
        pdf.set_font('helvetica', 'B', 11)
        pdf.draw_line()
        pdf.cell(width, height + 3, 'Mean', align='L')

        for year in sales:
            pdf.cell(width, height + 3, f"{mean(sales[year].values()):.1f}", align='R')

    def print_median():
        pdf.ln()
        pdf.set_font('helvetica', 'B', 11)
        pdf.cell(width, height, 'Median', align='L')

        pdf.set_fill_color(218, 237, 244)
        for year in sales:
            pdf.cell(width, height, f"{median(sales[year].values()):.1f}", align='R', fill=True)


    print_table_head()
    print_year_headings()
    print_change_headings()
    print_table_data()
    print_totals_line()
    print_mean()
    print_median()

    pdf.output(filename)




if __name__ == '__main__':
    main()