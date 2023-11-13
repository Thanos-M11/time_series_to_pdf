# A TIME-SERIES SALES GENERATOR WITH BRIEF HIGH LEVEL ANALYSIS EXPORTED IN PDF
### Video Demo: https://youtu.be/chs7zVSay4w
## Description:
>The software creates a time series random sales demand pattern generating a 
data set of 48 values per year of which the number of years is specified initially by the user. It then calculates sales values grouping them by quarters and by months and displaying them along with seasonal indices and changes in a pdf file in a tabular format.
  

## Overview

### Main Concept
The main steps that we actually need from the software are the following:
1. The user enters an integer number between 2 - 8 which is the number of years to be analyzed and displayed.
2. The application to check if the user's input is valid.
3. The application generates a random data set of sales amounts 4 times a month at specific days for the specified number of years and produces a time series of 48 rows per year with two attributes of a date and an amount. 
   >*In another concept this data set source could be from a csv file or from a sql database. But for the sake of this project we are focusing on the high level analysis of the data and the output of it in a pdf file.*
4. The application to calculate the totals from the time series and group them both by month and by quarter.
5. The application to calculate the seasonal variation expressed as seasonal indices (SI) for both the quarter totals and the monthly totals.
6. The application to calculate the changes over the years having as a base the first year of the data set.
7. The application to create two pdf files displaying in tabular format the time series high level analysis


### Classes we use:
We are using the following classes for our project that is:
1. a class `Sales` which will be used to construct the random time series values
2. a class `PDF` which inherits attributes and properties from `FPDF` library and will be used to add headers and footers in the pdf file.


### Main functions we use:
Apart from the `main()` function which handles all the functions we have chosen to use the following 7 main functions as per below: 
1.  `validate_years()`: validates the user's input 
2.  `random_time_series()` : creates a list of random time series values  
3.  `sales_by_qrt()` : reads the time series and returns a dictionary with totals by <u>quarter</u> 
4.  `sales_by_month()`: reads the time series and returns a dictionary with totals by <u>month</u>. 
5.  `sales_format_is_valid()`: validates the sales report format that will be called by other functions. 
6.  `get_seasonal_index()`: calculates the seasonal index from sales patterns and returns a dictionary with the seasonal index.
7.  `get_change_on_base()`: calculates the changes between the seasons along the years and returns a dictionary with the changes per year having as a base the first year.
8.  `create_pdf()`: creates a pdf file with all the calculated data in tabular format.

### Helper functions we use
1. `get_seasons()`: returns the number of seasons from a sales report 
- `get_delta()`: returns the delta between two values applied to two lists of values
- `format_percent()`: formats a float value to a percent adding a sign in front and the '%' sign at the end.  

<br>

## Classes explained

### class Sales:

```python
1    class Sales:
2        def __init__(self, salesdate: str, sales: int):
3            self.salesdate = datetime.strptime(salesdate, "%d-%m-%Y").date()
4            self.sales = sales
5    
6        @property
7        def year(self):
8            return self.salesdate.year
9        
10       @property
11       def month(self):
12           return self.salesdate.month
13       
14       @property
15       def qrt(self):
16           return ((self.month - 1) // 3) + 1
17    
18       def __str__(self):
19           return f"{self.salesdate}\t{self.sales:>10}"

```

In `Sales` class we construct two attributes 
- `salesdate` of type `str` and 
- `sales` of type `int`. 
- We are casting the `salesdate` attribute from type `str` to type `datetime` using the `datetime` library.
- On lines (6), (10) we set two class properties to return the year and the month of the `salesdate` using the `datetime`'s methods `.year` and `.month` accordingly. 
- In line (14) we set a property to calculate the quarter of the month using the following formula: `(( month - 1 ) // 3) + 1`

  - > The formula returns the closest integer value which is less than or equal to `(month - 1) / 3`
and add one. 

- In line 18 we have declared a `__str__` dunder method so as to be able to print our class object.


### class PDF

```python   

1   class PDF(FPDF):
2       def header(self):
3           self.image('logo-harvard.png', 10, 8, 30)
4           self.set_font('helvetica', 'B', 16)
5           self.cell(0, 10, self.title, border=False, new_x='LMARGIN', new_y='NEXT',  align='C')   
       
6       def footer(self):
7           self.set_y(-15)
8           self.set_font('helvetica', 'I', 10)
9           self.alias_nb_pages()
10          self.cell(0, 10, "Final Python Project on EDX CS50P - Thanos-M11 - 2023", align='L')
11          self.cell(0, 10, f"Page {self.page_no()} / {{nb}}", align='R')
12   
13      def draw_line(self):
14          self.cell(0,0, border="B", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

```
#### [PyFPDF](https://py-pdf.github.io/fpdf2/index.html) documentation source 

In `PDF` class we alter the inherited `header` and `footer` methods to fit our purpose.
- in line (3) we are printing an image with the ['Harvard University'](https://www.harvard.edu/)'s logo using the `image` method. The logo was downloaded from [here](https://scholar.harvard.edu/you/file/695030)
- we then set our font style to 'helvetica', font strength to bold and font size to 16 using the `set_font` method
- in line (5) we use the `cell` method to print the title of our pdf without any borders aligned in the center.  
- The `cell()`'s method syntax can be found in the [PyFPFD](https://pyfpdf.readthedocs.io/en/latest/reference/cell/index.html) documentation.

- in line (6) with the `footer()` function we set our cursor -15mm from the bottom of our paper, we set the font style, we use [alias_nb_pages()](https://pyfpdf.readthedocs.io/en/latest/reference/alias_nb_pages/index.html) to be able to print the total number of pages in a pdf file with the syntax as per line (14) `{nb}`
- in line (13) we add a `draw_line()` method which uses the `cell` method to print a line using the `border="B"` parameter that means to print a border line at the bottom of the cell.


<br>

## Functions explained

### validate_years()
```python
1   def validate_years(years: str) -> bool:
2       """Validates the input of the year to be an integer and between 2 - 8"""    
3       try:
4           assert years.isnumeric(), "Year value must be numeric"
5           assert int(years) in range(2, 9), "Year number must be between 2 - 8"
6           return True
7       except AssertionError as msg:
8           print(msg)
9           return False

```

This function receives a variable `years` of type `str`
- checks if this input is numeric 
- checks if the casted to `int`  variable is within the range of 2 and 9. We want the user to enter only a number between 2 and 8 and this constraint depends on the size of our paper (A4  in our case) either in portrait or landscape orientation. 

> The function returns `True` if the year passes the checks or `False` if not

### random_time_series()

```python
1    def random_time_series(n_years: int=5) -> list[Sales]:
2        """Creates a random 4 times per month sales demand for n years"""    
3        random.seed(100)
4        journal: list[Sales] =  []
5        start_year = datetime.now().year - n_years
6        for year in list(range(start_year, n_years + start_year)):
7            for month in MONTHS:
8                for day in DAYS:
9                    journal.append(
10                           Sales(
11                               salesdate=f"{day:02}-{month}-{year}", 
12                               sales=random.randrange(20, 100)
13                           )
14                       )
15       return journal

```
This function receives a variable `n_years` of type `int`, creates objects of class `Sales` with time series data for `n_years` from random integer numbers between 20 and 100 and returns a list of objects of class `Sales`.
- Uses the `random` library and in line (3) it initializes a [pseudorandom number](https://en.wikipedia.org/wiki/Random_seed#:~:text=A%20random%20seed%20(or%20seed,not%20need%20to%20be%20random)) generator with the method `random.seed()`  
- In line (4) it initializes a list with the name of `journal`.  The list will be used as a stack of objects.
- It sets as the starting year of the time series to be the year of today minus `n_years` in line (5)
- It uses two constant variables `MONTHS` and `DAYS` that is
  - > `MONTHS = range(1, 13)`
  - > `DAYS: list = [7, 14, 21, 28]`   
- The function must generate 'sales' observations 4 times a month and more specifically on the 7th, 14th, 21st and 28th day of each month for 12 months for `n_years`.  This generates 48 sales amounts per year * `n_years`.
- Using three `for` loops in line (6) the function instanciates `Sales` objects with the attributes of `salesdate` and `sales` and stores them in a list of objects under the name `journal`.
- in line (12) the `sales` attribute takes values from random integers between 20 and 100 using the `random.randrange()` method.
>The function returns the `journal` which is a list of class `Sales` objects. 



### sales_by_qrt()

```python
1   def sales_by_qrt(sales_ptrn: list[Sales]) -> dict[int, dict[int, int | float]]:
2       """creates a dict with qrt totals per year"""
3       sales: dict = dict()
4       for line in sales_ptrn:
5           if line.year not in sales:
6               sales[line.year] = {}
7           if line.qrt not in sales[line.year]:
8               sales[line.year][line.qrt] = 0
9           sales[line.year][line.qrt] += line.sales 
10      return sales
```
The function receives a list of objects under the name `sales_ptrn`.  It actually receives the `journal` which is the output of the item_series generator and its main purpose is to calculate totals and group them by quarter.
- in line (3) it initializes a dictionary with the name `sales`
- it iterates through the **time_series object** which in our case is the `sales_ptrn` and constructs the `sales` dictionary keys and values during the loop.  When the dictionary is ready in line (9) it sums up the sales values under the `sales[line.year][line.qrt]` key.
> The function returns a `dict`

The outcome of this function for a random set of 5 years is shown below:
```python
sales_ptrn: list[Sales] = random_time_series(5)
print(type(sales_by_qrt(sales_ptrn)))

for key, value in sales_by_qrt(sales_ptrn).items():
    print(key, value)
```

Output:
```
<class 'dict'>
2018 {1: 716, 2: 607, 3: 687, 4: 677}
2019 {1: 911, 2: 761, 3: 632, 4: 788}
2020 {1: 724, 2: 610, 3: 592, 4: 821}
2021 {1: 597, 2: 584, 3: 632, 4: 678}
2022 {1: 778, 2: 754, 3: 639, 4: 706}
```
- The output is of type `dict`.
- It creates 5 keys and within each key there are 4 total values one for each quarter


### sales_by_month()

```python
1   def sales_by_month(sales_ptrn: list[Sales]) -> dict[int, dict[int, int | float]]:
2       """Creates a dict with monthly totals per year"""
3       sales: dict = dict()
4       for line in sales_ptrn:
5           if line.year not in sales:
6               sales[line.year] = {}
7           if line.month not in sales[line.year]:
8               sales[line.year][line.month] = 0
9           sales[line.year][line.month] += line.sales 
10      return sales
```
Same as the `sales_by_qrt` but for months.

The function receives a list of objects under the name `sales_ptrn`.  It actually receives the `journal` which is the output of the item_series generator and its main purpose is to calculate totals and group them by month.
- in line (3) it initializes a dictionary with the name `sales`
- it iterates through the **time_series object** which in our case is the `sales_ptrn` and constructs the `sales` dictionary keys and values during the loop.  When the dictionary is ready in line (9) it sums up the sales values under the `sales[line.year][line.month]` key.
> The function returns a `dict`

Equally 
The outcome of this function for a random set of 5 years is shown below:
```python
sales_ptrn: list[Sales] = random_time_series(5)
print(type(sales_by_month(sales_ptrn)))

for key, value in sales_by_month(sales_ptrn).items():
    print(key, value)
```

Output
```
<class 'dict'>
2018 {1: 236, 2: 293, 3: 187, 4: 203, 5: 216, 6: 188, 7: 256, 8: 293, 9: 138, 10: 297, 11: 148, 12: 232}
2019 {1: 312, 2: 291, 3: 308, 4: 307, 5: 192, 6: 262, 7: 267, 8: 223, 9: 142, 10: 290, 11: 303, 12: 195}
2020 {1: 246, 2: 236, 3: 242, 4: 270, 5: 172, 6: 168, 7: 139, 8: 186, 9: 267, 10: 305, 11: 287, 12: 229}
2021 {1: 250, 2: 178, 3: 169, 4: 159, 5: 268, 6: 157, 7: 212, 8: 204, 9: 216, 10: 188, 11: 235, 12: 255}
2022 {1: 228, 2: 266, 3: 284, 4: 270, 5: 262, 6: 222, 7: 198, 8: 196, 9: 245, 10: 211, 11: 257, 12: 238}
```
The output is of type `dict`.
- It creates 5 keys and within each key there are 12 total values one for each month


### sales_format_is_valid()

```python
1   def sales_format_is_valid(sales_report: dict) -> bool:
2       """Validates the dictionary format. Returns True if only all 7 checks will pass"""
3   
4       #1. check if sales report is a dictionary
5       if not isinstance(sales_report, dict): return False
6           
7       #2. check if the number of keys are more than one
8       if not len(sales_report) > 1: return False
9       
10       #3. check if all 1st level keys are integers
11       temp3: list = [isinstance(key, int) for key in sales_report]
12       if not len(set(temp3)) == 1: return False
13   
14       #4. check if the first level values are of type dict
15       temp4: list = [isinstance(value, dict) for value in sales_report.values()]
16       if not len(set(temp4)) == 1: return False
17   
18       # 5. check if the keys of the 2nd level are int
19       temp5: list = []
20       for values in sales_report.values():
21           for key in values:
22               temp5.append(isinstance(key, int))
23       if not len(set(temp5)) == 1: return False
24   
25       # 6. check if the values of the 2nd level are int or floats
26       temp6: list = []
27       for values in sales_report.values():
28           for value in values.values():
29               temp6.append(isinstance(value, float | int))
30       if not len(set(temp6)) == 1: return False
31   
32       #7. checks if the length of the values are equal
33       temp7 = list(map(lambda x: len(x), sales_report.values()))
34       if not len(set(temp7)) == 1: return False
35   
36       return True
```

This function receives the output of either the `sales_by_month()` or the `sales_by_qrt()` function which must be a dictionary.
- The function checks if what enters matches a data type pattern and this of a specific format.
- There are 7 check points that need to be passed for a sales report to be valid for analysis and these are:
- We use `isinstance()` method line(4) to check if the report type is a dictionary. 
- We use the `len()` method in line(7) to check if the number of keys within the dictionary are more than 1. 
- In line (10) we use a list comprehension combined with the `isinstance()` method to check if the dictionary keys are integers. Using a `temp` list which we then cast to a type of `set` to measure the distinct values and check if these values are more than one.
- In line (14) following the same idea we use a list comprehension in combination with the `isinstance()` method to check if the dictionary values are of type dictionary.
- In lines (18 - 30) under the same principal we combine two loops to iterate through the dict values and use the `isinstance()` method to check if the keys of the dict values are integers or of the values of the dict values are either floats or integers accordingly. 
- Finally in line 32 we use a `lambda` function combined with a `map` one to collect the length of each dict value into the `temp` variable and check if they are equal by casting the list to a set and measure the length of it.

> The function returns `True` if all the 7 checks pass, otherwise it returns `False` as soon as one of the checks is wrong.

### get_seasons()

```python
1   def get_seasons(sales: dict) -> int:
2       """Returns the number of seasons within a sales dictionary, usually qrts or months"""
3       if sales_format_is_valid(sales):
4           seasons = []
5           for s in sales.values():
6               seasons.append(len(s)) 
7           return set(seasons).pop()
8       return 0

```
This function receives a sales report `dict`, checks in line (3) if the sales report is valid by calling the `sales_format_is_valid()` function and if the function returns `True` it iterates through the dict values line(5), collects its lengths, stores them into the variable `seasons` of type `list` in line (6) and pops the last element of the casted list to set in line (7). We use the technique to cast a type of `list` to a `set` so as to eliminate duplicate elements from a list because a [set](https://docs.python.org/3/tutorial/datastructures.html#sets) can only have unique elements. 

In line 7 we pop the last element from the set since it is only one because we have validated the `sales` dictionary in line (3) assuring that the lengths of each of the dictionary's values are equal.

> The function returns an integer value that is the number of seasons.  In our case this could be either 4 or 12.

### get_seasonal_index()

```python
1   def get_seasonal_index(sales: dict) -> dict[int, float]:
2       """returns the seasonal index of sales"""
3       if sales_format_is_valid(sales):
4           si = dict()
5           for s in range(1, get_seasons(sales) + 1):
6               temp = []
7               for y in sales:
8                   temp.append(sales[y][s] / mean(sales[y].values()))
9               si[s] = round(sum(temp) / len(temp), 4)
10          return si
11      return {}

```

This function receives a `sales` dictionary
- in line (3) it validates this dictionary by calling the `sales_format_is_valid()` function.  
- Initializes a dictionary `si` in line (4) to collect the seasonal index of each season.
- The first loop iterates through the number of seasons, calls the `get_seasons()` function to get the number of seasons that exist in the `sales` dictionary
- initializes a temporary list variable `temp` and 
- uses a nested `for` loop to iterate through the `sales` dictionary in order to collect the value per year per season and divide it with the mean of the sales per year. 
- In line(9) it updates the `si` dictionary with the total amount stored in the `temp` list divided by the length of the list and rounds the result into 4 decimals.

> It returns a dictionary as per below:
```python
{1: 1.0678, 2: 0.9525, 3: 0.9211, 4: 1.0586}
```


### get_delta()

```python
1   def get_delta(list1: list, list2: list) -> dict[int, float]:
2       """returns the change between two float elements of a list"""
3       if len(list1) != len(list2):
4           return {}
5       change_list = list(map(lambda x, y: (y - x) / x, list1, list2))
6       return {key: round(value, 2) for key, value in enumerate(change_list, 1)}

```

This function **returns the change between two float values within a list**. It uses the formula (y2 - y1) / y1. The constraint here is that both of the lists must have the same length.
- It receives two lists
- In line (3) it checks if the lengths of the two lists are equal
- In line (5) it uses a `lambda` function combined with a `map` function to apply the formula to the elements of each list.
- In line (6) it uses a `dict` comprehension to return a dictionary.
  

### format_percent()

```python
1   def format_percent(val: float) -> str:
2       """formats a float value as a percent with two decimals and adds a '+ / -' sign in front"""
3       if not isinstance(val, float | int):
4           return "Value is not a float or integer"
5       if val > 0:
6           sign = '+'
7       elif val == 0:
8           sign = ''
9       else:
10          sign = '-'
11      return f"{sign}{abs(val*100):.1f}%"

```
This function formats a value to a percent with one decimal by adding the plus and minus sign in front of the value.
- It receives a float value
- In line (3) checks if the value is either float or integer
- In lines (5 - 10) checks if the value is greater, equal or less than zero and assigns the '+', "" or '-' sign to the `sign` variable.
> It returns a `str`    


### get_change_on_base()

```python
1   def get_change_on_base(report: dict) -> dict:
2       """returns a dictionary with the changes between periods per year"""
3       if sales_format_is_valid(report):
4           periods = sorted(list({period for period in report}))
5           delta: dict = {}
6           for period in range(1, len(periods)):
7               base_year = report[periods[0]].values()
8               delta[periods[period]] = get_delta(base_year, report[periods[period]].values())
9           return delta
10      return {}

```
#### This function receives a sales `report` of type `dict`
- in line (3) checks if the `report` is valid by calling the `sales_format_is_valid()` function.
- In line (4) it collects all the periods from the `report` dictionary and stores them in the `periods` variable.
- Initializes a dictionary `delta`.
- in line (6) it iterates through the periods starting from the second period in the list.
- In line (7) it sets as a change base the first period of the list and uses the `base_year` to assign the base values.
- In line (8) it stores the change between the `base_year` and the loop value by calling the `get_delta()` function into the `delta` dictionary.

>It returns a `dictionary` with the changes per season - period


### create_pdf()

```python
1    def create_pdf(sales: dict, seasonal_index: dict, changes: dict, filename: str):
2        """Creates a pdf report on sales and changes in table format"""
3        
4        # counts number of years from the report
5        n_years = len([years for years in sales])
6        if n_years not in range(2, 9):
7            return "The report can display data between 2 and 8 years only"
8    
9        # changes pdf orientation if the number of years is > 5
10       if n_years > 5:
11           pdf = PDF('L', 'mm', 'A4')
12       else:
13           pdf = PDF('P', 'mm', 'A4')
14       
15       # add page
16       pdf.title = "Sales - Report"
17       pdf.set_auto_page_break(auto=True, margin = 15)
18       pdf.add_page()
19       
20       # set default width of cells, height
21       width:int = 16
22       height:int = 8
23       gap: int = 3
24   
25       # calculate cell's width for sales and changes
26       sales_w = len([years for years in sales]) * width
27       change_w = len([years for years in changes]) * width
28       seasonal_index_w = width
29       
20       # calculate left and right margin according to number of years to display
31       calc_margin = (pdf.w - sales_w - change_w - seasonal_index_w - gap * 2 - width) / 2
32       pdf.set_left_margin(calc_margin)
33       pdf.set_right_margin(calc_margin) 
34   
```
#### The function creates a pdf report and displays a brief high level sales analysis in tabular format.
- It receives 4 parameters that is 
  - the `sales` dictionary, (this is the main sales report that has the data grouped by quarter or by month)
  - `seasonal_index` dictionary,
  - the `changes` dictionary (where all the changes have been calculated) and 
  - a `filename` of type `str` (the name of the pdf file to be created)
- In line(5) it counts the number of years from the report.
- In line (6) checks if the number of years is between 2 and 8 to run the analysis or not.
- It initializes the pdf object, sets the paper orientation according to the number of years to be displayed. The orientation is landscape if the number of years is > 5 and portrait if <= 5. This is strictly for displaying purposes maintaining a standard column width and a standard font size. 
- It configures the cell's width, height and gaps in between the columns.
- It calculates the left and the right margins to center the whole table in the middle of the page.

<br>

```python
35       def print_table_head():
36           pdf.set_font('helvetica', 'B', 11)
37           pdf.set_xy(pdf.get_x() + width, pdf.get_y())
38           pdf.cell(sales_w, height + 3, 'Sales', border=True, align='C')
39           pdf.set_x(pdf.get_x() + gap)
40           pdf.cell(seasonal_index_w, height + 3, 'SI', border=True, align='C')
41           pdf.set_x(pdf.get_x() + gap)
42           pdf.cell(change_w, height + 3, 'Change on Base', border=True, new_x=XPos.LEFT, new_y=YPos.NEXT, align='C')
             pdf.set_font('helvetica', 'BI', 10)
43           pdf.cell(change_w, height, f'Base is Year {list(sales.keys())[0]}', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='R')
44       
45       def print_year_headings():
46           pdf.set_y(pdf.get_y() + 2)
47           pdf.set_font('helvetica', 'B', 11)
48           pdf.cell(width, height + 3, 'Period', align='L')
49           for year in sales:
50               pdf.cell(width, height + 3, str(year), align='C')
51           pdf.set_x(pdf.get_x() + gap + width + gap)
52   
53       def print_change_headings():
54           for ch in changes:
55               pdf.cell(width, height + 3, str(ch), align='C')
56           pdf.ln(10)
57   
```

- The `print_table_head()` is a nested function that:
  -  sets the font family, weight and size, 
  -  sets the xy cursor's position
  -  prints 
     -  the sales heading
     -  the seasonal index heading as 'SI'
     -  the changes heading
     -  the 'Base of the year' heading

- The `print_year_heading()` is a nested function that 
  - iterates through the `sales` report, 
  - prints the years at the top of the table and 
  - adds a gap at the end.


- The `print_change_headings()` is a nested function that:
  - iterates through the `changes` report
  - prints the years and
  - adds 10mm of space vertically (Y axis)


<br>

```python
58       def print_table_data():
59           # get the number of seasons
60           seasons: int = get_seasons(sales)
61           if seasons == 4:
62               periods: list = ['Qrt1', 'Qrt2', 'Qrt3', 'Qrt4']
63           else:
64               periods: list = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
65           # years settings 
66           pdf.set_font('helvetica', '', 11)
67           for period in range(1, seasons + 1):
68               pdf.set_text_color(0, 0, 0)
69               pdf.set_font('helvetica', 'B', 11)
70               pdf.cell(width, height, str(periods[period - 1]), border=0, align="L")
71               # insert a lightgray backcolor font
72               if period % 2 == 0:
73                   pdf.set_fill_color(237, 237, 237)
74               else:
75                   pdf.set_fill_color(252, 252, 252)
76               for year in sales:
77                   pdf.set_font('helvetica', '', 11)
78                   pdf.cell(width, height, str(sales[year][period]), border=0, align='R', fill=True)
79               
80               # seasonal index column settings
81               pdf.set_text_color(255, 0, 0)
82               pdf.set_font('helvetica', 'BI', 10)
83               pdf.set_x(pdf.get_x() + gap)
84               pdf.cell(width, height, f"{seasonal_index[period]:.3f}", border=0, align='C', fill=True)
85               pdf.set_x(pdf.get_x() + gap)
86               # changes column settings
87               pdf.set_text_color(0, 0, 255)
88               pdf.set_font('helvetica', '', 11)
89               for ch in changes:
90                   pdf.cell(width, height, format_percent(changes[ch][period]), border=0, align='R', fill=True)
91               pdf.ln()
92     
```
- The `print_table_data()` is a nested function that:
  - gets the number of seasons with `get_seasons()` from `sales` report and if the number is 4 it assigns a list of quarter elements to a variable `periods` otherwise it assigns a list of months to the same variable.  This list will be printed according to the sales report type (either by quarter or by month).
  - sets the year data settings. It uses two loops, one to iterate through the `period` to get the period name either quarter or month and the second one to iterate through the `sales` report to get the actual sales value per year per period.
  - Inserts a light-gray background color line by line
  - configures the seasonal index column settings (line 80)
  - configures the changes column settings (line 86)
  - iterates through the `changes` dictionary to get the changes per year per period and calls the `format_percent()` function to format the dictionary values.


```python
93       def print_totals_line():
94           pdf.set_text_color(0, 0, 0)
95           pdf.set_font('helvetica', 'B', 12)
96           pdf.set_y(pdf.get_y() + 2)
97           pdf.set_font('helvetica', 'B', 11)
98           pdf.cell(width, height + 3, 'Totals', align='L')
99           
100          # print sum of months
101          year_change = []
102          for year in sales:
103              pdf.cell(width, height + 3, f"{sum(sales[year].values())}", align='R')
104              year_change.append(sum(sales[year].values()))
105          
106          pdf.set_x(pdf.get_x() + gap + width + gap)
107          
108          # print change on sums
109          pdf.set_text_color(0, 0, 255)
110          for year in range(1, len(year_change)):
111              ch = f"{format_percent((year_change[year] - year_change[year - 1]) / year_change[year - 1])}"
112              pdf.cell(width, height + 3, ch, align='R')
113  
114      def print_mean():
115          pdf.ln()
116          pdf.set_text_color(0, 0, 0)
117          pdf.set_font('helvetica', 'B', 11)
118          pdf.draw_line()
119          pdf.cell(width, height + 3, 'Mean', align='L')
120  
121          for year in sales:
122              pdf.cell(width, height + 3, f"{mean(sales[year].values()):.1f}", align='R')
123  
124      def print_median():
125          pdf.ln()
126          pdf.set_font('helvetica', 'B', 11)
127          pdf.cell(width, height, 'Median', align='L')
128  
129          pdf.set_fill_color(218, 237, 244)
130          for year in sales:
131              pdf.cell(width, height, f"{median(sales[year].values()):.1f}", align='R', fill=True)
132  
133 
134      print_table_head()
135      print_year_headings()
136      print_change_headings()
137      print_table_data()
138      print_totals_line()
139      print_mean()
140      print_median()
141  
142      pdf.output(filename)
```
- The `print_totals_line()` is a nested function that:
- configures the font style of the total's line
- iterates through the `sales` report 
  - gets the `sum` of sales by year
  - prints the `sum`
  - collects its value to the `year_change` list that will be used in the next lines to calculate the change in totals.
- iterates through the `year_change` list
  - calculates the change on totals
  - prints the change on totals

- The `print_mean()` is a nested function that:
  - configures font style
  - iterates through the `sales` report
  - uses the `mean` function from `statistics` library
  - prints the mean value of periods from sales per year.

- The `print_median()` is a nested function that:
  - configures font style
  - iterates through the `sales` report
  - uses the `median` function from `statistics` library
  - prints the median value of periods from sales per year.

- In Lines (134 - 140) all the nested functions are called
- Line (142) creates the pdf file using the `output()` method.


### main()

```python
1    def main():
2        
3        years = input("Enter the number of years between 2 - 8 for analysis: ")
4        if validate_years(years):
5            years: int = int(years)
6            sales: list[object] = random_time_series(years)
7            sales_m: dict = sales_by_month(sales)
8            sales_q: dict = sales_by_qrt(sales)
9            change_m: dict = get_change_on_base(sales_m)
10           change_q: dict = get_change_on_base(sales_q)
11           si_m: dict = get_seasonal_index(sales_m)
12           si_q: dict = get_seasonal_index(sales_q)
13           create_pdf(sales_q, si_q, change_q, "sales_q.pdf")
14           create_pdf(sales_m, si_m, change_m, "sales_m.pdf")

```


The `main()` function:
- Executes the whole application as per below:
  - Asks the user to enter a number between 2 and 8.  This is the number of years to be analyzed.
  - Validates the user's input
  - Casts the user's input from `str` to `int` and assigns the casted value to the variable `years`
  - calls `random_time_series(years)` to generate a random time series data set for `years` years and assigns its output to the variable `sales` of type `list[object]`.
  - Calls the `sales_by_month(sales)` function to calculate the totals by month and assigns the dictionary output to the variable `sales_m` of type `dict`.
  - Calls the `sales_by_qrt(sales)` function to calculate the totals by quarter and assigns the dictionary output to the variable `sales_q` of type `dict`.
  - Calls the `get_change_on_base(sales_m)` function to calculate the monthly changes from the `sales_m` report and assigns the dictionary output to the variable `change_m`.
  - Calls the `get_change_on_base(sales_q)` function to calculate the quarterly changes from the `sales_q` report and assigns the dictionary output to the variable `change_q`.
  - Calls the `get_seasonal_index(sales_m)` function to calculate the monthly seasonal indices from the `sales_m` report and assigns the dictionary output to the variable `si_m`.
  - Calls the `get_seasonal_index(sales_q)` function to calculate the quarterly seasonal indices from the `sales_q` report and assigns the dictionary output to the variable `si_q`.
  - Calls the `create_pdf(sales_q, si_q, change_q, "sales_q.pdf")`to create a pdf file with the name "sales_q.pdf" that reads the quarterly data from `sales_q`, quarterly seasonal indices from `si_q` and quarterly changes from `change_q`.
  - Calls the `create_pdf(sales_m, si_m, change_m, "sales_m.pdf")`to create a pdf file with the name "sales_m.pdf" that reads the monthly data from `sales_m`, monthly seasonal indices from `si_m` and monthly changes from `change_m`.



