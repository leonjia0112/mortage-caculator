

from calendar import month
import math

a = 22250

y = 0.09
r = y/12

n = 36

interest_range = 60

month_detail_list = {}
def mortgate_calculater(a, r, n):
    """
    n: number of months
    r: APR
    a: principal
    """
    remain_principal = a
    r = r/12
    b = ( (a*r) * math.pow(1+r, n)) / (math.pow(1+r, n) - 1) 
    print("Monthly payment is {}".format(b))

    print("There are {} month, which are {} years to get to the loan amount.".format(round(a / b), round(round(a / b)/12)))
    y = ( n * a * r * math.pow(1+r, n)) / (math.pow(1+r, n) - 1) - a
    print("Total interest paid: {}".format(y))

    for i in range(n):
        month_interest = remain_principal * r 
        remain_principal = remain_principal - (b - month_interest)
        
        print("month {}. Payment: ${}. Interest: ${}. Principal: ${}.".format(i + 1, round(b, 2), round(month_interest, 2), round(b - month_interest, 2)))

        month_detail = {}
        month_detail["payment"] = b
        month_detail["interest"] = month_interest
        month_detail["principal"] = b - month_interest 
        month_detail_list[i] = month_detail

def sum_interest(start, end):
    """
    start: start at month
    end: end at month
    """
    payment_sum = 0
    sum = 0
    for i in range(start, end):
        payment_sum = payment_sum + month_detail_list[i]["payment"]
        sum = sum + month_detail_list[i]["interest"]

    print("Total payment of from month {} to month {} is ${}".format(start, end, round(payment_sum, 2)))
    print("Total interest of from month {} to month {} is ${}".format(start, end, round(sum, 2)))



#mortgate_calculater(22250, 0.075, 12)
#mortgate_calculater(22250, 0.08, 18)
mortgate_calculater(577500, 0.0299, 360)

# mortgate_calculater(700000, 0.05, 360)

sum_interest(25, 25+12)

mortgate_calculater(600000, 0.055, 360)

sum_interest(0, 12)