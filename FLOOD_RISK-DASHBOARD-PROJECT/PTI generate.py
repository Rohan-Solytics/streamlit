import random

# Generate 50 PTIs for businesses based on a DSCR range of 1.25 to 1.5
# Assuming a loan payment is monthly and fixed business income
dscr_range = (1.25, 1.5)
loan_values = [829, 993, 1495]  # Example loan values from your dataset
fixed_business_income = 10000  # Example fixed income

# Function to calculate PTI based on loan value and a fixed income
def calculate_pti(loan_value, fixed_income, dscr_range):
    dscr = random.uniform(*dscr_range)
    monthly_income_needed = loan_value * dscr
    pti = monthly_income_needed / fixed_income
    return round(pti, 4)

# Generate a list of 50 PTIs
ptis = [calculate_pti(random.choice(loan_values), fixed_business_income, dscr_range) for _ in range(50)]

print(ptis)
