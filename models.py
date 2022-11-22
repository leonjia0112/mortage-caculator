class MonthlyIncomeDetail(object):

    def __init__(self,
                 n,
                 payment,
                 income,
                 noi,
                 accumulated_noi,
                 yearly_noi):
        self._detail = {
            'nth_month': n,
            'monthly_payment': payment,
            'monthly_income': income,
            'monthly_noi': noi,
            'accumulated_noi': accumulated_noi,
            'yearly_noi': yearly_noi,
        }

    def get(self, key):
        return self._detail.get(key, None)

    def get_all(self):
        return self._detail


class MortgageLoanDetail(object):

    def __init__(self,
                 loan_amount,
                 loan_rate,
                 down_payment,
                 loan_length,
                 down_payment_in_percentage=False,
                 loan_term_in_year=True,
                 loan_rate_in_percentage=True,
                 loan_type="Fixed",
                 loan_bank=None,
                 extra_principal_paid=None):
        if extra_principal_paid is None:
            extra_principal_paid = {}

        self._detail = {
            'loan_amount': loan_amount,
            'loan_rate': loan_rate,
            'loan_length': loan_length,
            'loan_term_in_year': loan_term_in_year,
            'loan_rate_in_percentage': loan_rate_in_percentage,
            'loan_type': loan_type,
            'loan_bank': loan_bank,
            'extra_principal_paid': extra_principal_paid,
        }

    def get(self, key):
        return self._detail.get(key, None)

    def get_all(self):
        return self._detail


class MonthlyMortgageDetail(object):

    def __init__(self, n, month_left, payment, interest, principal,
               remaining_principal, accumulated_interest, interest_to_be_paid):
        self._detail = {
            'nth_month': n,
            'month_left': month_left,
            'payment': payment,
            'interest': interest,
            'principal': principal,
            'remaining_principal': remaining_principal,
            'accumulated_interest': accumulated_interest,
            'interest_to_be_paid': interest_to_be_paid,
        }

    def get(self, key):
        return self._detail.get(key, None)

    def get_all(self):
        return self._detail
