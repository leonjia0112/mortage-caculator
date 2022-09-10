from calendar import month
import math
import pprint

month_detail_list = {}


def mortgate_calculater(principal, apr, length, is_year=False):
    """
    :params: length: length of loan time
    :params: apr: fixed apr rate
    :params: principal: loan amount
    :params: is_year: default to False, if given length is year, set to True
    """
    remain_principal = principal
    monthly_rate = apr / 12
    number_of_payment = length * 12 if is_year else length

    # This calculates the monthly payment
    monthly_payment = ((principal * monthly_rate) \
                       * math.pow(1 + monthly_rate, number_of_payment)) \
                      / (math.pow(1 + monthly_rate, number_of_payment) - 1)

    print("Monthly payment is {}".format(monthly_payment))

    print("There are {} month, which are {} years to get to the loan amount.".format(
        round(remain_principal / monthly_payment),
        round(round(remain_principal / monthly_payment) / 12)))

    # This calculates the total interest pay with this loan
    total_interest = (number_of_payment * remain_principal * monthly_rate * \
                      math.pow(1 + monthly_rate, number_of_payment)) \
                     / (math.pow(1 + monthly_rate, number_of_payment) - 1) - remain_principal
    print("Total interest paid: {}".format(total_interest))

    mortgate_details = []
    interest_pay_so_far = 0

    for i in range(number_of_payment):
        interest = remain_principal * monthly_rate
        remain_principal = remain_principal - (monthly_payment - interest)
        principal_paid = monthly_payment - interest
        interest_pay_so_far = interest_pay_so_far + interest

        mortgate_month_detail = {
            'payment': monthly_payment,
            'interest': interest,
            'principal_paid': principal_paid,
            'remaining_principal': remain_principal,
            'interest_pay_so_far': interest_pay_so_far,
        }

        mortgate_details.append(mortgate_month_detail)
        month_detail_list[i] = mortgate_month_detail

    return mortgate_details


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


def main():
    # a = 22250,

    # y = 0.09
    # r = y/ 12

    # n = 36

    # interest_range = 60


    mortgate_details = mortgate_calculater(600000, 0.05, 30, is_year=True)

    for i in range(10):
        print(f'month: {i + 1}')
        pprint.pprint(mortgate_details[i])


if __name__ == "__main__":
    main()
