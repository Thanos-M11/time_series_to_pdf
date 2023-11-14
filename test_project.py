import itertools

from project import (
    MONTHS, 
    DAYS, 
    validate_years, 
    random_time_series, 
    sales_by_qrt, 
    sales_by_month, 
    sales_format_is_valid,
    get_seasons, 
    get_seasonal_index,
    get_delta,
    format_percent,
    get_change_on_base
)


def test_validate_years():
    years = {
        "0": False,
        "2": True,
        "3": True, 
        "5": True, 
        "8": True, 
        "9": False, 
        "t": False, 
        "&*": False,
        "AB890": False,
        "": False,
        " 123": False,
        "5 ": False,
    }
    for y in years:
        assert validate_years(y) == years[y]    


def test_random_time_series():
    assert len(random_time_series(2)) == 96
    assert len(random_time_series(8)) == 48 * 8
    assert isinstance(random_time_series(2), list)
    assert isinstance(random_time_series(2), object)
    
    for ds, m, d in itertools.product(list(range(2, 3)), range(len(list(MONTHS))), range(len(DAYS))):
        assert hasattr(random_time_series(ds)[m*d], "salesdate")
        assert hasattr(random_time_series(ds)[m*d], "sales")
        assert hasattr(random_time_series(ds)[m*d], "month")
        assert hasattr(random_time_series(ds)[m*d], "qrt")
        assert hasattr(random_time_series(ds)[m*d], "year")


def test_sales_by_qrt():
    data_sets: int = 2
    sales_ptrn = random_time_series(data_sets)
    assert isinstance(sales_by_qrt(sales_ptrn), dict)
    assert len(sales_by_qrt(sales_ptrn)) == data_sets
    q_len = []
    q_keys = set()
    for qrt in sales_by_qrt(sales_ptrn).values():
        q_len.append(len(qrt))
        for key in qrt.keys():
            q_keys.add(key)
    assert sum(q_len) / len(q_len) == 4
    
    for _ in q_keys:
        assert _ in range(1, 5)


def test_sales_by_month():
    data_sets: int = 2
    sales_ptrn = random_time_series(data_sets)
    assert isinstance(sales_by_month(sales_ptrn), dict)
    assert len(sales_by_month(sales_ptrn)) == data_sets
    m_len = []
    m_keys = set()
    for month in sales_by_month(sales_ptrn).values():
        m_len.append(len(month))
        for key in month.keys():
            m_keys.add(key)
    assert sum(m_len) / len(m_len) == 12
    
    for _ in m_keys:
        assert _ in range(1, 13)


def test_sales_format_is_valid():
    tests = {
        0 : [],
        1 : {2010: 5},
        2 : {2010: 5, "2011": 6, 2012: 7},
        3 : {2010: {1: 5, 3: 30}, 2020: [7, 15, 30, 50]},
        4 : {2010: {1: 5, 2: 20, 3: 30, 4: 50}, 2020: {"1": 5, "2": 20, "3": 30, "4": 50}},
        5 : {2010: {1: 5, 2: 20, 3: "30", 4: 50}, 2020: {1: "5", 2: 20, 3: 30, 4: 50}},
        6 : {2010: {1: 5, 2: 20, 3: 30, 4: 50}, 2020: {1: 5, 2: 20, 3: 30}},
        7 : {2020: {1: 100, 2: 200, 3: 300, 4: 400}, 2021: {1: 115, 2: 225, 3: 330, 4: 450}},
    }

    results = [False, False, False, False, False, False, False, True]

    for key in tests:
        assert sales_format_is_valid(tests[key]) == results[key]


def test_get_seasons():
    test_sets = [
        {2020: {}},
        {2020: {1: 10}},
        {2020: {1: 10, 2: 20}},
        {2020: {1: 10, 2: 20, 3: 30}},
        {2020: {1: 10, 2: 20, 3: 30, 4: 40}},
        {
            2020: {1: 10},
            2021: {1: 10, 2: 20},
            2022: {1: 10, 2: 20, 3: 30}
        },
        {
            2020: {1: 10, 2:20, 3: 30, 4: 40, 5: 50, 6: 60, 7: 70, 8: 80, 9: 90, 10: 100, 11: 110, 12:120},
            2021: {1: 10, 2:20, 3: 30, 4: 40, 5: 50, 6: 60, 7: 70, 8: 80, 9: 90, 10: 100, 11: 110, 12:120},
            2022: {1: 10, 2:20, 3: 30, 4: 40, 5: 50, 6: 60, 7: 70, 8: 80, 9: 90, 10: 100, 11: 110, 12:120}
        },
        {
            2020: {1: 10, 2:20, 3: 30, 4: 40},
            2021: {1: 10, 2:20, 3: 30, 4: 40}
        }
    ]
    test_results = [0, 0, 0, 0, 0, 0, 12, 4]

    for key, value in enumerate(test_sets):
        assert get_seasons(value) == test_results[key]

    
def test_get_seasonal_index():
    ds1 = {
        2010: {1: 100, 2: 200, 3: 300, 4: 400},
        2011: {1: 150, 2: 180, 3: 110, 4: 250},
        2012: {1: 110, 2: 300, 3: 250, 4: 800},
        2013: {1: 1000, 2: 500, 3: 800, 4: 100}
    }
    ds2 = {
        2018: {1: 34, 2: 37, 3: 50, 4: 38, 5: 94, 6: 71, 7: 86, 8: 85, 9: 40, 10: 21, 11: 55, 12: 13},
        2019: {1: 70, 2: 65, 3: 97, 4: 66, 5: 69, 6: 92, 7: 18, 8: 98, 9: 76, 10: 48, 11: 61, 12: 12},
        2020: {1: 7, 2: 48, 3: 52, 4: 44, 5: 55, 6: 46, 7: 55, 8: 23, 9: 91, 10: 61, 11: 17, 12: 18},
    }
    
    assert get_seasonal_index(ds1) == {1: .8094, 2: .8747, 3: 0.964, 4: 1.3519}
    assert get_seasonal_index(ds2) == {1: 0.6348, 2: 0.9453, 3: 1.2254, 4: 0.926, 5: 1.3856, 6: 1.2877, 7: 1.0701, 8: 1.2306, 9: 1.3543, 10: 0.8553, 11: 0.8002, 12: 0.2848}
    

def test_get_delta():
    l1 = [10, 20, 30, 40]
    l2 = [30, 60, 90, 120]
    assert get_delta(l1, l2) ==  {1: 2.0, 2: 2.0, 3: 2.0, 4: 2.0}
    l1 = [10,20,30,40]
    l2 = [5,10,15,20]
    assert get_delta(l1, l2) ==  {1: -0.5, 2: -0.5, 3: -0.5, 4: -0.5}
    l1 = [10,20,30,40]
    l2 = [0,20,0,400]
    assert get_delta(l1, l2) ==  {1: -1.0, 2: 0.0, 3: -1.0, 4: 9.0}


def test_format_percent():
    assert format_percent(0.45) == "+45.0%"
    assert format_percent(0.0) == "0.0%"
    assert format_percent(-0.08) == "-8.0%"
    assert format_percent(-5) == "-500.0%"
    assert format_percent("io") == "Value is not a float or integer"


def test_get_change_on_base():
    tests = [
        {
            2018: {1: 10, 2: 100, 3: 200, 4: 300, 5: 400, 6: 500},
            2019: {1: 20, 2: 200, 3: 400, 4: 600, 5: 800, 6: 1000},
            2020: {1: 5, 2: 50, 3: 100, 4: 150, 5: 200, 6: 250},
            2021: {1: 10, 2: 100, 3: 200, 4: 300, 5: 400, 6: 500},
        },
        {
            2018: {1: 34, 2: 37, 3: 50, 4: 38, 5: 94, 6: 71}
        },
        {
            2018: {1: 10, 2: 100, 3: 200, 4: 300, 5: 400, 6: 500},
            2019: {1: 20, 2: 200, 3: 400, 4: 600, 5: 800, 6: 1000},
            "2020": {1: 5, 2: 50, 3: 100, 4: 150, 5: 200, 6: 250},
            2021: {1: 10, 2: 100, 3: 200, 4: 300, 5: 400, 6: 500},
        },
        {
            2018: {1: 10, 2: 100, 3: 200, 4: 300, 5: 400, 6: 500},
            2019: {1: "20", 2: 200, 3: 400, 4: 600, 5: 800, 6: 1000},
            2020: {1: 5, 2: 50, 3: 100, 4: 150, 5: 200, 6: 250},
            2021: {1: 10, 2: 100, 3: 200, 4: 300, 5: 400, 6: 500},
        },
        {
            2018: {1: 10, 2: 100, 3: 200, 4: 300, 5: 400, 6: 500},
            2019: {1: 20, 2: 200, "3": 400, 4: 600, 5: 800, 6: 1000},
            2020: {1: 5, 2: 50, 3: 100, 4: 150, 5: 200, 6: 250},
            2021: {1: 10, 2: 100, 3: 200, 4: 300, 5: 400, 6: 500},
        },
        {
            2018: {1: 10, 2: 100, 3: 200, 4: 300, 5: 400, 6: 500},
            2019: {1: 20, 2: 200, 3: 400, 4: 600},
            2020: {1: 5, 2: 50, 3: 100, 4: 150, 5: 200, 6: 250},
            2021: {1: 10, 2: 100, 3: 200, 4: 300, 5: 400, 6: 500},
        },
        [],
        15,
        "text",
        10.2,
        {}
    ]

    results = [
         {
            2019: {1: 1.0, 2: 1.0, 3: 1.0, 4: 1.0, 5: 1.0, 6: 1.0}, 
            2020: {1: -0.5, 2: -0.5, 3: -0.5, 4: -0.5, 5: -0.5, 6: -0.5}, 
            2021: {1: 0.0, 2: 0.0, 3: 0.0, 4: 0.0, 5: 0.0, 6: 0.0}
        },
        {},{},{},{},{},{},{},{},{},{}
     ]

    for key, value in enumerate(tests):
        assert get_change_on_base(tests[key]) == results[key]