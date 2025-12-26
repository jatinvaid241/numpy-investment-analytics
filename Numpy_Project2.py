import numpy as np
import pandas as pd
#Data Understanding & Loading

df = pd.read_excel(r'C:\Users\JATIN\Downloads\Historicalinvesttemp.xlsx',skiprows=6)
print(df.head())
#Removing Blank rows
#df = df.dropna(how="all")

#Convert columns to numeric
"""df.iloc[:,1] = pd.to_numeric(df.iloc[:,1], errors='coerce')
df.iloc[:,2] = pd.to_numeric(df.iloc[:,2], errors='coerce')
df.iloc[:,3] = pd.to_numeric(df.iloc[:,3], errors='coerce')"""

df = df.apply(pd.to_numeric, errors='coerce')

#pandas to numpy

data = df.to_numpy()

#check to data is working Properly

print("Type of Data", type(data))
print("Shape of Data", data.shape)
print("\nFirst 3 rows of Data")
print(data[:5])

#--------------------------------------------------------------------Descriptive Statistics--------------------------------------------------

#Calculate the mean annual return for Stocks, T.Bills, and T.Bonds

# Mean calculation
stocks = data[:,1]
stocks = stocks[~np.isnan(stocks)]

stocks_mean = np.mean(stocks)
print("Mean Annual Return of Stocks:", stocks_mean)


#Bills Mean Calculation
Bills = data[:,2]
Bills = Bills[~np.isnan(Bills)]

Bills_mean = np.mean(Bills)
print("Mean Anuual Return of Bills", Bills_mean)

#Bonds Mean Calculation
Bonds = data[:,3]
Bonds = Bonds[~np.isnan(Bonds)]

Bonds_mean = np.mean(Bonds)
print("Mean Anuual Return of Bonds", Bonds_mean)

#Find the maximum and minimum returns for each investment type.

print("Maximum Returns of Stocks", np.max(stocks))
print("Minimum Return of Stocks", np.min(stocks))

print("Maximum Returns of T.Bills", np.max(Bills))
print("Minimum Returns of T.Bills", np.min(Bills))

print("Maximum Return of Bonds", np.max(Bonds))
print("Minimum Return of Bonds", np.min(Bonds))

#Calculate the standard deviation of returns for all three investments.

print("Standard Deviation of Stocks",np.std(stocks))
print("Standard Deviation of Bills",np.std(Bills))
print("Standard Deviation of Bonds",np.std(Bonds))

#Identify which investment shows the highest volatility.
'''Stocks show the highest volatility as they have the highest standard deviation of annual returns compared to T.Bills and T.Bonds. '''

#For each year, determine: Which investment (Stocks, T.Bills, or T.Bonds) gave the highest return.
years = data[:,0]
returns = data[:,1:4]
print(np.isnan(returns).all(axis=1).sum())
valid_mask = ~np.isnan(returns).all(axis=1)
years = years[valid_mask]
returns = returns[valid_mask]

best_idx = np.nanargmax(returns, axis=1)
investment_name = np.array(["Stocks", "T.Bills", "T.Bonds"])
best_investment = investment_name[best_idx]
for y, inv in zip(years, best_investment):
    print(f"Year {int(y)} → Best Investment: {inv}")

#Count how many times each investment type was the best performer.

unique, counts = np.unique(best_investment, return_counts = True)
result = np.column_stack((unique,counts))
print(result)

worst_idx = np.nanargmin(returns, axis=1)
worst_investment = investment_name[worst_idx]
for y, inv in zip(years, worst_investment):
    print(f"Years {int(y)} worst investment: {inv}")

#Determine which investment provides the best risk–return tradeoff.

risk_return = np.array([
    (stocks_mean/np.std(stocks)),
    (Bills_mean/np.std(Bills)),
    (Bonds_mean/np.std(Bonds))
])
for inv_name, rr in zip(investment_name, risk_return):
    print(f"{inv_name} Risk–Return Ratio: {rr:.3f}")

#Long-Term Investment Insights

#Calculate the cumulative return for each investment over all years.

stocks_cum = np.prod(1 + stocks) - 1
Bills_cum = np.prod(1 + Bills) - 1
Bonds_cum = np.prod(1 + Bonds) - 1

print(f"Cumulative Return of Stocks: {stocks_cum:.2%}")
print(f"Cumulative Return of T.Bills: {Bills_cum:.2%}")
print(f"Cumulative Return of T.Bonds: {Bonds_cum:.2%}")

cumulative_returns = np.array([
    np.prod(1 + stocks) - 1,
    np.prod(1 + Bills) - 1,
    np.prod(1 + Bonds) - 1
])
print("Cumulative Returns:", cumulative_returns)
for name, cr in zip(investment_name,cumulative_returns):
    print(f'{name} cumulative Returns: {cr:2f}')


best_long_term = investment_name[np.argmax(cumulative_returns)]
print("Best Long-Term Investment:", best_long_term)


#Identify which investment would have been the best long-term choice.

investment_names = np.array(["Stocks", "T.Bills", "T.Bonds"])

cumulative_returns = np.array([
    np.prod(1 + stocks) - 1,
    np.prod(1 + Bills) - 1,
    np.prod(1 + Bonds) - 1
])

best_long_term = investment_names[np.argmax(cumulative_returns)]

print("Best Long-Term Investment:", best_long_term)

#Determine whether Stocks consistently outperform T.Bills and T.Bonds over time.

returns = data[:, 1:4]
best_each_year = investment_names[np.argmax(returns, axis=1)]

unique, counts = np.unique(best_each_year, return_counts=True)

for u, c in zip(unique, counts):
    print(f"{u} outperformed in {c} years")

#-----------------------------------------------------Decision-Based Questions, Identify years where:

#Stocks had negative returns but T.Bills had positive returns.

condition = (data[:,1]<0) & (data[:,2]>0)
years_stocks_neg_bill_pos = data[condition,0]
print("(Years, Stocks, T.bills)", years_stocks_neg_bill_pos)

#Years where all investments are positive

condition2 = (data[:,1]>0) & (data[:,2]>0) & (data[:,3]>0)
all_three_positive = data[condition2,0]
print("All Three Investments are Positive", all_three_positive)

#Years where Stocks were riskiest (highest absolute return
abs_returns = np.abs(data[:,1:4])
riskiest_idx = np.argmax(abs_returns, axis=1)

years_stock_riskiest = data[(riskiest_idx == 0), 0]

print("Years Stocks were riskiest:", years_stock_riskiest)


'''Output Generation

Create a NumPy-based summary array containing:

Mean return

Maximum return

Minimum return

Standard deviation
for each investment type. Export the summary results to a CSV file.'''

summary = np.array([
    [np.mean(stocks), np.max(stocks), np.min(stocks), np.std(stocks)],
    [np.mean(Bills), np.max(Bills), np.min(Bills), np.std(Bills)],
    [np.mean(Bonds), np.max(Bonds), np.min(Bonds), np.std(Bonds)]
])
print("summary Array:\n", summary)

#Export Summary to CSV

header = "Mean, Max, Min, Std"
np.savetxt("investment_summary.csv", summary, delimiter=',', header = header, comments="")
