# investments/utils.py
import matplotlib
matplotlib.use("Agg")         # no GUI
import matplotlib.pyplot as plt
from io import BytesIO


def calculate_interest(duration, initial_balance, interest_rate, withdrawals, additional_investments, interest_rate_changes, recurring_investment):
    yearly_balance = [initial_balance]  # list updated yearly for plotting
    total_invested = initial_balance
    net_profit = 0

    for year in range(1, duration + 1):
        # Update interest rate if there is a change for the current year
        if year in interest_rate_changes:
            interest_rate = interest_rate_changes[year]
        
        # Add the recurring yearly investment sum
        if recurring_investment:
            total_invested += recurring_investment
            yearly_balance[-1] += recurring_investment
        
        # Add any one-time additional investment for this year
        if year in additional_investments:
            total_invested += additional_investments[year]
            yearly_balance[-1] += additional_investments[year]
        
        # Apply compound interest for the year
        yearly_balance[-1] *= (1 + interest_rate / 100)
        
        # Process any withdrawals
        if year in withdrawals:
            net_profit += withdrawals[year]
            yearly_balance[-1] -= withdrawals[year]
        
        # Save the current balance for plotting and next year's calculation
        yearly_balance.append(yearly_balance[-1])
        # Increment search counter if you use it elsewhere (or additional processing)
    
    final_balance = yearly_balance[-1]
    net_profit += final_balance - total_invested  # Withdrawals are included in net profit calculation

    return int(final_balance), int(net_profit), int(total_invested), yearly_balance[:-1]


# def main():
#     duration = int(input("Enter the duration of investment (in years): "))
#     initial_balance = int(input("Enter the initial investment (initial balance): "))
#     interest_rate = float(input("Enter the interest rate (ex: 5 == 5% yearly compound interest rate): "))
    
#     # Prompt for recurring yearly investment sum
#     recurring_investment = int(input("Enter the recurring yearly investment sum: "))

#     withdrawals = {}                # Dictionary to store withdrawals
#     additional_investments = {}     # Dictionary to store one-time additional investments
#     interest_rate_changes = {}      # Dictionary to store interest rate changes

#     while True:
#         print("\nDo you want to add an early withdrawal, additional investment, or change interest rate?")
#         action = input("Input: n - no, w - withdrawal, a - additional investment, c - interest rate change: ").lower()
#         if action == 'w':
#             year = int(input("Enter the year of withdrawal: "))
#             amount = int(input("Enter the amount withdrawn: "))
#             withdrawals[year] = amount
#         elif action == 'a':
#             year = int(input("Enter the year of additional investment: "))
#             amount = int(input("Enter the amount added: "))
#             additional_investments[year] = amount
#         elif action == 'c':
#             year = int(input("Enter the year of change in interest rate: "))
#             new_rate = float(input("Enter the new interest rate: "))
#             interest_rate_changes[year] = new_rate
#         elif action == 'n':
#             break

#     # Call calculate_interest with all the parameters
#     final_balance, net_profit, total_invested, yearly_balance = calculate_interest(
#         duration,
#         initial_balance,
#         interest_rate,
#         withdrawals,
#         additional_investments,
#         interest_rate_changes,
#         recurring_investment
#     )

#     print(f"\nFinal balance at maturation: {final_balance}")
#     print(f"Net profit: {net_profit}")
#     print(f"Total sum invested: {total_invested}")
#     print(f"Actual compound interest rate: {(final_balance / total_invested) ** (1 / duration) - 1:.4f}")



def plot_yearly_balance(yearly_balance):
    """Returns a PNG image buffer of the plot."""
    fig, ax = plt.subplots(figsize=(6,4))
    ax.plot(range(len(yearly_balance)), yearly_balance, marker="*")
    ax.set_xlabel("Year")
    ax.set_ylabel("Balance")
    ax.set_title("Yearly Balance of Investment")
    ax.grid(True)

    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    return buf
