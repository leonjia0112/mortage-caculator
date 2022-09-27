from calendar import month
import math
import pprint
from collections import namedtuple

month_detail_list = {}

MortgageDetailSchema = [
    "month",
    "payment",
    "interest",
    "principal",
    "remaining_principal",
    "accumulated_interest"
]

MortgageDetail = namedtuple("MortgageDetail", MortgageDetailSchema)


def get_mortgate_detail_nt(detail_dict: dict) -> MortgageDetail:
    args = []
    for k in MortgageDetailSchema:
        args.append(detail_dict[k])
    return MortgageDetail(*args)


def calculate_mortage_monthly_payment(principal, monthly_rate, number_of_payment):
    monthly_payment = ((principal * monthly_rate) \
                       * math.pow(1 + monthly_rate, number_of_payment)) \
                      / (math.pow(1 + monthly_rate, number_of_payment) - 1)
    return round(monthly_payment, 2)


def calculate_total_interest_predict(principal, number_of_payment, monthly_rate):
    # This calculates the total interest pay with this loan
    total_interest = (number_of_payment * principal * monthly_rate * \
                      math.pow(1 + monthly_rate, number_of_payment)) \
                     / (math.pow(1 + monthly_rate, number_of_payment) - 1) - principal


def mortgate_calculater(price, down_payment_amount, apr, length, is_year=False, extra_principal_paid: dict = {}):
    """
    :params: length: length of loan time
    :params: apr: fixed apr rate
    :params: principal: loan amount
    :params: is_year: default to False, if given length is year, set to True
    """
    remain_principal = price - down_payment_amount
    print(f'Down Payment: {price - remain_principal}')
    monthly_rate = (apr / 100) / 12
    number_of_payment = length * 12 if is_year else length

    mortgate_details = []
    interest_pay_so_far = 0
    the_nth_month = 1

    while number_of_payment > 0:
        monthly_payment = calculate_mortage_monthly_payment(remain_principal, monthly_rate, number_of_payment)
        interest_paid = round(remain_principal * monthly_rate, 2)
        principal_paid = round(monthly_payment - interest_paid, 2)
        remain_principal = remain_principal - principal_paid - extra_principal_paid.get(the_nth_month, 0)
        principal_paid = monthly_payment - interest_paid
        interest_pay_so_far = interest_pay_so_far + interest_paid

        mortgate_month_detail = {
            'payment': monthly_payment,
            'interest_paid': interest_paid,
            'principal_paid': principal_paid,
            'remaining_principal': remain_principal,
            'interest_pay_so_far': interest_pay_so_far,
        }

        mortgate_details.append(mortgate_month_detail)
        month_detail_list[the_nth_month] = mortgate_month_detail

        number_of_payment = number_of_payment - 1
        the_nth_month = the_nth_month + 1

    return mortgate_details


def range_interest_sum(start, end):
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


def net_operating_income(liability: dict, income: int):
    """
    :params income: monthly income
    :params liability:
    """

    assert 'monthly_mortgage_payment' in liability
    assert 'property_tax' in liability
    assert 'insurance' in liability

    monthly_income = income

    total_expense = 0
    total_expense += liability['monthly_mortgage_payment']
    total_expense += liability['hoa']
    total_expense += liability['property_tax'] / 12
    total_expense += liability['insurance'] / 12

    return monthly_income - total_expense


#
# def table_output(content: list[dict]):
#     if len(content) == 0:
#         return
#
#     n_col = len(content[0].keys())
#
#     row_format = "{:>15}" * (n_col + 1)
#     print(row_format.format("", *teams_list))
#     for team, row in zip(teams_list, data):
#         print(row_format.format(team, *row))

def table_output(content_list, title_list):
    n_col = len(title_list)
    row_format = "{:>16}" * n_col
    print(row_format.format(*title_list))
    for c in content_list:
        print(row_format.format(*c))


def cal_income(house_info, loan_info, extra_principal_paid=None, month=25):
    if extra_principal_paid is None:
        extra_principal_paid = {}

    price = house_info['price']
    property_tax = house_info['property_tax']
    insurance = house_info['insurance']
    monthly_income = house_info['monthly_income']
    hoa = house_info['hoa']

    down_payment_type = loan_info['down_payment_type']
    interest_rate = loan_info['interest_rate']
    down_payment_percent = loan_info['down_payment_percent']
    down_payment_amount = loan_info['down_payment_amout']
    loan_time = loan_info['loan_time']

    if down_payment_type == 'percent':
        down_payment_amount = price * (1 - down_payment_percent / 0.01)

    mortgate_details = mortgate_calculater(
        price, down_payment_amount, interest_rate, loan_time,
        is_year=True, extra_principal_paid=extra_principal_paid)

    accumulated_NOI = 0
    res_list = []
    yearly_NOI = 0

    for i in range(1, month):

        # print(f'month: {i}')
        md = mortgate_details[i]
        monthly_payment = md.get('payment')

        liability = dict()
        liability['monthly_mortgage_payment'] = monthly_payment
        liability['property_tax'] = property_tax / 12
        liability['insurance'] = insurance / 12
        liability['hoa'] = 0

        monthly_NOI = round(net_operating_income(liability, monthly_income), 2)
        accumulated_NOI = round(accumulated_NOI + monthly_NOI, 2)

        # print(f'monthly_NOI: {monthly_NOI}')
        # print(f'accumulated_NOI: {accumulated_NOI}')
        if i % 12 == 0:
            yearly_NOI_output = round(accumulated_NOI - yearly_NOI, 2)
            yearly_NOI = accumulated_NOI
            res_element = [i, monthly_NOI, accumulated_NOI, md['payment'], yearly_NOI_output]
        else:
            res_element = [i, monthly_NOI, accumulated_NOI, md['payment'], 0]

        res_list.append(res_element)

    return res_list


def main():
    house_info = {
        "price": 900000.0,
        "property_tax": 8713,
        "insurance": 2400,
        "monthly_income": 5300,
        "hoa": 0,
    }

    loan_info = {
        "interest_rate": 5.75,
        "down_payment_amout": 30000,
        "loan_time": 30,
        "down_payment_type": 'amount',
        "down_payment_percent": 0,
    }

    extra_principal_paid = {
        2: 50000,
        3: 50000,
        4: 50000,
        5: 50000,
        9: 50000,
        10: 50000,
        11: 50000,
    }

    res_list = cal_income(
        house_info,
        loan_info,
        extra_principal_paid=extra_principal_paid,
        month=49)

    col_list = [
        'month',
        'monthly NOI',
        'accumulated NOI',
        'monthly_payment',
        'yearly NOI'
    ]

    table_output(res_list, col_list)


if __name__ == "__main__":
    main()
