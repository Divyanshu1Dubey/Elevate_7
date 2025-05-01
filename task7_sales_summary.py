import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser(description="Analyze sales data from SQLite.")
parser.add_argument('--db', default='sales_data.db', help='Path to SQLite database')
parser.add_argument('--save', action='store_true', help='Save the chart as PNG')
args = parser.parse_args()

conn = sqlite3.connect(args.db)

query = '''
SELECT 
    product, 
    SUM(quantity) AS total_qty, 
    SUM(quantity * price) AS revenue
FROM sales
GROUP BY product
'''

df = pd.read_sql_query(query, conn)
print("Sales Summary:")
print(df.to_string(index=False))

plt.style.use('seaborn-vibrant')
fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(df['product'], df['revenue'], color='cornflowerblue')
ax.set_title("Revenue by Product", fontsize=14)
ax.set_xlabel("Product")
ax.set_ylabel("Revenue")
ax.bar_label(bars, fmt='%.2f', padding=3)
plt.tight_layout()

if args.save:
    plt.savefig("sales_chart.png")
    print("Chart saved as 'sales_chart.png'")
else:
    plt.show()

conn.close()
