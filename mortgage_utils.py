import math
import typing
import unittest


def calculate_mortgage_monthly_payment(principal, monthly_rate, number_of_payment):
    assert principal != 0

    monthly_payment = ((principal * monthly_rate)
                       * math.pow(1 + monthly_rate, number_of_payment)) \
                      / (math.pow(1 + monthly_rate, number_of_payment) - 1)
    return round(monthly_payment, 2)


def table_output(content_object_list: typing.List[typing.Dict]):
    assert len(content_object_list) > 0
    title_list = content_object_list[0].keys()
    n_col = len(title_list)

    size = 16
    format_str = "{:>" + str(size) + "}"
    row_format = format_str * n_col
    print(row_format.format(*title_list))
    for c in content_object_list:
        print(row_format.format(*c.values()))


class MortgageDetail(object):
    ESCROW_PERCENTAGE = 10

    def __init__(self,
                 loan_id: int,
                 loan_amount: float,
                 loan_length: int,
                 insurance: float,
                 property_tax: float,
                 interest_rate: float,
                 extra_principal_paid_schedule: dict = None,
                 length_in_month=False):

        if extra_principal_paid_schedule is None:
            self.extra_principal_paid_schedule = {}
        else:
            self.extra_principal_paid_schedule = extra_principal_paid_schedule

        self.loan_id = loan_id
        self.loan_amount = loan_amount
        self.loan_length = loan_length if length_in_month else loan_length * 12
        self.insurance = insurance
        self.property_tax = property_tax
        self.interest_rate = (interest_rate / 100) / 12
        self.mortgage_payment_details = [dict()] * self.loan_length
        self._get_mortgage_payment_details()
        self.mortgage_payment_details_title = self.mortgage_payment_details[0].keys()

    def _get_mortgage_payment_details(self):
        """
        Calculate mortgage detail based on mortgage term.
        """
        remain_principal = self.loan_amount
        interest_pay_so_far = 0
        total_mortgage_paid_so_far = 0

        for i in range(self.loan_length):
            mortgage_payment = calculate_mortgage_monthly_payment(
                remain_principal, self.interest_rate, self.loan_length - i)
            interest_paid = round(remain_principal * self.interest_rate, 2)
            principal_paid = round(mortgage_payment - interest_paid, 2)
            escrow_payment = round(mortgage_payment * (self.ESCROW_PERCENTAGE / 100), 2)
            insurance_payment = round(self.insurance / 12, 2)
            property_tax_payment = round(self.property_tax / 12, 2)
            monthly_payment = mortgage_payment + escrow_payment + insurance_payment + property_tax_payment
            remain_principal = round(remain_principal - principal_paid - self.extra_principal_paid_schedule.get(i, 0), 2)
            interest_pay_so_far = round(interest_pay_so_far + interest_paid, 2)
            total_mortgage_paid_so_far = round(total_mortgage_paid_so_far + mortgage_payment, 2)

            self.mortgage_payment_details[i] = {
                'id': self.loan_id,
                'n': str(i + 1),
                'monthly_payment': monthly_payment,
                'interest': interest_paid,
                'principal': principal_paid,
                'escrow': escrow_payment,
                'insurance': insurance_payment,
                'property_tax': property_tax_payment,
                'remaining_principal': remain_principal,
                'interest_so_far': interest_pay_so_far,
                'total_mortgage_so_far': total_mortgage_paid_so_far,
            }

        return self.mortgage_payment_details


class TestMortgageDetails(unittest.TestCase):

    def test_mortgage_detail(self):
        new_mortgage = MortgageDetail(1, 660000, 30, 1600, 7007, 4.875)
        table_output(new_mortgage.mortgage_payment_details)


if __name__ == '__main__':
    unittest.main()
