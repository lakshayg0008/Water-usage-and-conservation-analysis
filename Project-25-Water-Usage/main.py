
# ==========================================
# PROJECT 25: WATER USAGE & CONSERVATION
# ==========================================

# Import required libraries
import pandas as pd
import numpy as np

# Load the dataset
df = pd.read_csv("data/25_water_consumption.csv")

# Display first five records
print("\n========== FIRST FIVE RECORDS ==========")
print(df.head())

# Display dataset dimensions
print("\n========== DATASET DIMENSIONS ==========")
print("Rows and Columns:", df.shape)

# Display column names
print("\n========== COLUMN NAMES ==========")
print(df.columns.tolist())

# Display data types
print("\n========== DATA TYPES ==========")
print(df.dtypes)

# Display dataset information
print("\n========== DATASET INFORMATION ==========")
df.info()

# Display missing values
print("\n========== MISSING VALUES ==========")
print(df.isnull().sum())

# ==========================================
# TASK 2: IDENTIFY DUPLICATES
# ==========================================

print("\n========== DUPLICATE RECORDS ==========")

# Count duplicate meter record IDs
duplicate_count = df["Meter_Record_ID"].duplicated().sum()

print("Duplicate Meter Record IDs:", duplicate_count)

# Display duplicate records
duplicates = df[df["Meter_Record_ID"].duplicated(keep=False)]

print("\nDuplicate Records:")
print(duplicates)


# ==========================================
# TASK 3: HANDLE MISSING VALUES
# ==========================================

print("\n========== HANDLING MISSING VALUES ==========")

# Calculate median water usage
median_usage = df["Water_Usage_Liters"].median()

print("Median Water Usage:", median_usage)

# Fill missing values with median
df["Water_Usage_Liters"] = df["Water_Usage_Liters"].fillna(median_usage)

# Check missing values after filling
print("\nMissing Values After Cleaning:")
print(df.isnull().sum())


# ==========================================
# TASK 4: DATE CONVERSION
# ==========================================

print("\n========== DATE CONVERSION ==========")

# Convert Reading_Date into datetime format
df["Reading_Date"] = pd.to_datetime(df["Reading_Date"], errors="coerce")

# Extract month name
df["Month"] = df["Reading_Date"].dt.month_name()

# Extract weekday name
df["Weekday"] = df["Reading_Date"].dt.day_name()

# Display selected columns
print("\nDate, Month and Weekday:")
print(df[["Reading_Date", "Month", "Weekday"]].head(10))

# Check the data type
print("\nReading_Date Data Type:")
print(df["Reading_Date"].dtype)

# Check invalid dates
print("\nInvalid Dates:", df["Reading_Date"].isnull().sum())


# ==========================================
# TASK 5: WATER CONSUMPTION CALCULATIONS
# ==========================================

print("\n========== WATER CONSUMPTION ANALYSIS ==========")

# Calculate total water consumption
total_consumption = df["Water_Usage_Liters"].sum()

print("Total Water Consumption:", total_consumption, "Litres")

# Calculate total consumption for each household
household_consumption = df.groupby("Household_ID")["Water_Usage_Liters"].sum()

print("\n========== HOUSEHOLD-WISE CONSUMPTION ==========")
print(household_consumption)

# Calculate average consumption per household
average_consumption = household_consumption.mean()

print("\nAverage Consumption Per Household:",
      round(average_consumption, 2), "Litres")

# Count unique households
total_households = df["Household_ID"].nunique()

print("Total Number of Households:", total_households)


# ==========================================
# TASK 6: MONTH-TO-MONTH CONSUMPTION CHANGE
# ==========================================

print("\n========== MONTHLY WATER CONSUMPTION ==========")

# Extract year and month from Reading_Date
df["Year_Month"] = df["Reading_Date"].dt.to_period("M")

# Calculate monthly consumption for each household
monthly_consumption = df.groupby(
    ["Household_ID", "Year_Month"]
)["Water_Usage_Liters"].sum().reset_index()

# Rename the consumption column
monthly_consumption.rename(
    columns={"Water_Usage_Liters": "Monthly_Consumption"},
    inplace=True
)

# Sort records by household and month
monthly_consumption = monthly_consumption.sort_values(
    ["Household_ID", "Year_Month"]
)

# Calculate percentage change from previous month
monthly_consumption["Monthly_Change_Percent"] = (
    monthly_consumption.groupby("Household_ID")[
        "Monthly_Consumption"
    ].pct_change(fill_method=None) * 100
)

# Display monthly consumption and changes
print("\n========== MONTH-TO-MONTH CHANGE ==========")
print(monthly_consumption.head(20).to_string(index=False))

# Display average monthly consumption change
average_change = monthly_consumption[
    "Monthly_Change_Percent"
].mean()

print("\nAverage Monthly Change:",
      round(average_change, 2), "%")


# ==========================================
# TASK 7: RANK HOUSEHOLD TYPES
# ==========================================

print("\n========== HOUSEHOLD TYPE RANKING ==========")

# Calculate total water consumption by household type
type_consumption = df.groupby(
    "Household_Type"
)["Water_Usage_Liters"].sum().reset_index()

# Rename the consumption column
type_consumption.rename(
    columns={"Water_Usage_Liters": "Total_Consumption"},
    inplace=True
)

# Sort from highest to lowest consumption
type_consumption = type_consumption.sort_values(
    by="Total_Consumption",
    ascending=False
)

# Assign ranks
type_consumption["Rank"] = type_consumption[
    "Total_Consumption"
].rank(method="min", ascending=False).astype(int)

# Display ranking
type_consumption = type_consumption[
    ["Rank", "Household_Type", "Total_Consumption"]
]

print(type_consumption.to_string(index=False))


# ==========================================
# TASK 8: BUILDING TYPE AND ZONE ANALYSIS
# ==========================================

print("\n========== BUILDING TYPE ANALYSIS ==========")

# Calculate average consumption by building type
building_analysis = df.groupby(
    "Building_Type"
)["Water_Usage_Liters"].mean().reset_index()

# Rename the column
building_analysis.rename(
    columns={"Water_Usage_Liters": "Average_Consumption"},
    inplace=True
)

# Sort by average consumption
building_analysis = building_analysis.sort_values(
    by="Average_Consumption",
    ascending=False
)

print(building_analysis.to_string(index=False))


print("\n========== ZONE-WISE ANALYSIS ==========")

# Calculate average consumption by zone
zone_analysis = df.groupby(
    "Zone"
)["Water_Usage_Liters"].mean().reset_index()

# Rename the column
zone_analysis.rename(
    columns={"Water_Usage_Liters": "Average_Consumption"},
    inplace=True
)

# Sort by average consumption
zone_analysis = zone_analysis.sort_values(
    by="Average_Consumption",
    ascending=False
)

print(zone_analysis.to_string(index=False))


# ==========================================
# TASK 9: IDENTIFY HIGH WATER CONSUMPTION
# ==========================================

print("\n========== HIGH WATER CONSUMPTION ANALYSIS ==========")

# Calculate average water usage per household
household_average = df.groupby(
    "Household_ID"
)["Water_Usage_Liters"].mean().reset_index()

# Rename the column
household_average.rename(
    columns={"Water_Usage_Liters": "Average_Usage"},
    inplace=True
)

# Calculate the 75th percentile threshold
threshold = household_average["Average_Usage"].quantile(0.75)

print("75th Percentile Threshold:", round(threshold, 2), "Litres")

# Identify households above the threshold
high_consumption = household_average[
    household_average["Average_Usage"] > threshold
]

# Sort households from highest to lowest usage
high_consumption = high_consumption.sort_values(
    by="Average_Usage",
    ascending=False
)

# Display high consumption households
print("\n========== HIGH CONSUMPTION HOUSEHOLDS ==========")
print(high_consumption.to_string(index=False))

# Display the number of high consumption households
print("\nNumber of High Consumption Households:",
      len(high_consumption))


# ==========================================
# TASK 10: ZONE-WISE HOUSEHOLD TYPE ANALYSIS
# ==========================================

print("\n========== ZONE-WISE HOUSEHOLD ANALYSIS ==========")

# Calculate total water usage by zone and household type
zone_household_analysis = df.pivot_table(
    index="Zone",
    columns="Household_Type",
    values="Water_Usage_Liters",
    aggfunc="sum",
    fill_value=0
)

# Display the analysis
print(zone_household_analysis)

# Calculate total consumption in each zone
print("\n========== TOTAL CONSUMPTION BY ZONE ==========")

zone_totals = df.groupby("Zone")[
    "Water_Usage_Liters"
].sum().sort_values(ascending=False)

print(zone_totals)

# Identify the zone with the highest consumption
highest_zone = zone_totals.idxmax()

print("\nZone with Highest Water Consumption:", highest_zone)
print("Highest Zone Consumption:", round(zone_totals.max(), 2), "Litres")


# ==========================================
# TASK 11: MONTHLY WATER CONSUMPTION ANALYSIS
# ==========================================

print("\n========== MONTHLY CONSUMPTION ANALYSIS ==========")

# Group water consumption by month
monthly_totals = df.groupby(
    "Month"
)["Water_Usage_Liters"].sum()

# Arrange months in calendar order
month_order = [
    "January", "February", "March", "April",
    "May", "June", "July", "August",
    "September", "October", "November", "December"
]

monthly_totals = monthly_totals.reindex(
    month_order
).dropna()

# Display monthly consumption
print(monthly_totals)

# Find the month with the highest consumption
highest_month = monthly_totals.idxmax()
highest_month_usage = monthly_totals.max()

print("\nMonth with Highest Consumption:", highest_month)
print("Highest Monthly Consumption:",
      round(highest_month_usage, 2), "Litres")

# Find the month with the lowest consumption
lowest_month = monthly_totals.idxmin()

print("Month with Lowest Consumption:", lowest_month)
print("Lowest Monthly Consumption:",
      round(monthly_totals.min(), 2), "Litres")


# ==========================================
# TASK 12: WATER CONSUMPTION SUMMARY REPORT
# ==========================================

print("\n========== WATER CONSUMPTION SUMMARY REPORT ==========")

# Calculate important statistics
total_records = len(df)
total_households = df["Household_ID"].nunique()
total_usage = df["Water_Usage_Liters"].sum()
average_usage = df["Water_Usage_Liters"].mean()
maximum_usage = df["Water_Usage_Liters"].max()
minimum_usage = df["Water_Usage_Liters"].min()

# Display summary report
print("Total Meter Records:", total_records)
print("Total Households:", total_households)
print("Total Water Consumption:", round(total_usage, 2), "Litres")
print("Average Water Usage:", round(average_usage, 2), "Litres")
print("Maximum Water Usage:", maximum_usage, "Litres")
print("Minimum Water Usage:", minimum_usage, "Litres")

print("\n========== REPORT COMPLETED ==========")


# ==========================================
# TASK 13: EXPORT ANALYSIS RESULTS
# ==========================================

print("\n========== EXPORTING ANALYSIS RESULTS ==========")

# Export cleaned dataset
df.to_csv("outputs/cleaned_water_data.csv", index=False)

# Export household type analysis
type_consumption.to_csv(
    "outputs/household_type_analysis.csv",
    index=False
)

# Export building analysis
building_analysis.to_csv(
    "outputs/building_type_analysis.csv",
    index=False
)

# Export zone analysis
zone_analysis.to_csv(
    "outputs/zone_analysis.csv",
    index=False
)

# Export high consumption households
high_consumption.to_csv(
    "outputs/high_consumption_households.csv",
    index=False
)

# Export monthly consumption
monthly_totals.rename(
    "Total_Consumption"
).to_csv("outputs/monthly_consumption.csv")

print("All analysis files exported successfully!")


# ==========================================
# TASK 14: MONTHLY WATER CONSUMPTION CHART
# ==========================================

import matplotlib.pyplot as plt

print("\n========== CREATING MONTHLY CHART ==========")

plt.figure(figsize=(10, 5))

monthly_totals.plot(
    kind="bar",
    color="skyblue",
    edgecolor="black"
)

plt.title("Monthly Water Consumption")
plt.xlabel("Month")
plt.ylabel("Water Consumption (Litres)")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig("outputs/monthly_consumption_chart.png")

plt.show()

print("Monthly chart saved successfully!")


# ==========================================
# TASK 15: HOUSEHOLD TYPE CONSUMPTION CHART
# ==========================================

print("\n========== CREATING HOUSEHOLD TYPE CHART ==========")

plt.figure(figsize=(9, 5))

plt.bar(
    type_consumption["Household_Type"],
    type_consumption["Total_Consumption"],
    color="orange",
    edgecolor="black"
)

plt.title("Water Consumption by Household Type")
plt.xlabel("Household Type")
plt.ylabel("Total Water Consumption (Litres)")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig("outputs/household_type_chart.png")

plt.show()

print("Household type chart saved successfully!")


# ==========================================
# TASK 16: ZONE-WISE CONSUMPTION CHART
# ==========================================

print("\n========== CREATING ZONE-WISE CHART ==========")

plt.figure(figsize=(9, 5))

plt.bar(
    zone_analysis["Zone"],
    zone_analysis["Average_Consumption"],
    color="lightgreen",
    edgecolor="black"
)

plt.title("Average Water Consumption by Zone")
plt.xlabel("Zone")
plt.ylabel("Average Water Consumption (Litres)")
plt.tight_layout()

plt.savefig("outputs/zone_consumption_chart.png")

plt.show()

print("Zone-wise chart saved successfully!")
