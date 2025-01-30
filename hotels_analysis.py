# AtliQ Hotels Data Analysis Project
# Author: Vinit Desai
# Description: Data cleaning, transformation, and insights generation for hotel bookings

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set visualization style
sns.set_style("whitegrid")

# ------------------
# 1. Data Import & Exploration
# ------------------

# Load datasets
df_bookings = pd.read_csv('datasets/fact_bookings.csv')
df_date = pd.read_csv('datasets/dim_date.csv')
df_hotels = pd.read_csv('datasets/dim_hotels.csv')
df_rooms = pd.read_csv('datasets/dim_rooms.csv')
df_agg_bookings = pd.read_csv('datasets/fact_aggregated_bookings.csv')

# Explore Data
print("Bookings Data Sample:")
print(df_bookings.head())
print("\nUnique Room Categories:", df_bookings.room_category.unique())
print("\nBooking Platform Distribution:")
print(df_bookings.booking_platform.value_counts())

# Visualize booking platform distribution
df_bookings.booking_platform.value_counts().plot(kind="bar", title="Bookings per Platform")
plt.show()

# ------------------
# 2. Data Cleaning
# ------------------

# Remove invalid guest entries
df_bookings = df_bookings[df_bookings.no_guests > 0]

# Remove revenue outliers using mean + 3*std threshold
revenue_limit = df_bookings.revenue_generated.mean() + 3 * df_bookings.revenue_generated.std()
df_bookings = df_bookings[df_bookings.revenue_generated <= revenue_limit]

# Handle missing values in df_bookings
df_bookings.fillna({'rating': df_bookings.rating.median()}, inplace=True)

# ------------------
# 3. Data Transformation
# ------------------

# Create occupancy percentage column
df_agg_bookings['occ_pct'] = round((df_agg_bookings.successful_bookings / df_agg_bookings.capacity) * 100, 2)

# Merge with room data for better clarity
df_agg_bookings = df_agg_bookings.merge(df_rooms, left_on="room_category", right_on="room_id")
df_agg_bookings.drop(columns=['room_id'], inplace=True)

# ------------------
# 4. Insights Generation
# ------------------

# Average occupancy rate per room category
room_occupancy = df_agg_bookings.groupby("room_class")['occ_pct'].mean().sort_values()
room_occupancy.plot(kind='bar', title="Average Occupancy by Room Type")
plt.show()

# Average occupancy per city
city_occupancy = df_hotels.merge(df_agg_bookings, on='property_id').groupby("city")["occ_pct"].mean()
print("\nAverage Occupancy per City:\n", city_occupancy)

# Revenue realized per city
df_bookings_all = df_bookings.merge(df_hotels, on="property_id")
revenue_by_city = df_bookings_all.groupby("city")["revenue_realized"].sum()
print("\nTotal Revenue by City:\n", revenue_by_city)

# Visualize revenue distribution
revenue_by_city.sort_values(ascending=False).plot(kind="bar", title="Revenue Realized per City")
plt.show()

# ------------------
# Final Export for GitHub
# ------------------

df_bookings.to_csv("cleaned_bookings.csv", index=False)
df_agg_bookings.to_csv("aggregated_bookings_cleaned.csv", index=False)
print("\nData processing complete. Ready for GitHub upload!")
