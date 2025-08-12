# Define a method to add a payment to the list
def add_payment(self, amount):
    self.payments.append(amount)

# Define a method to calculate the total payment for the employee
def total_payment(self):
    # Sum up the payments in the list
    total = sum(self.payments)
    # Add 225 if the employee worked 15 days or more
    if len(self.payments) >= 15:
        total += 225
    # Return the total payment
    return total

# Define a method to count the number of days the employee worked
def days_worked(self):
    return len(self.payments)

# Define a method to check if the employee got a monthly free
def got_monthly_free(self):
    return len(self.payments) >= 15

# Define a method to count the number of days the employee was eligible for travel payment
def travel_eligible_days(self):
    # Filter the payments that are not zero and not marked as "no"
    travel_payments = [p for p in self.payments if p != 0 and p != "no"]
    # Return the number of such payments
    return len(travel_payments)

# Define a method to count the number of days the employee was not eligible for travel payment
def travel_not_eligible_days(self):
    # Filter the payments that are zero or marked as "no"
    no_travel_payments = [p for p in self.payments if p == 0 or p == "no"]
    # Return the number of such payments
    return len(no_travel_payments)
