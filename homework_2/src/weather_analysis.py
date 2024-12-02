"""Weather Analysis Exercise""" 
import pandas as pd 
import matplotlib.pyplot as plt 
 
def analyze_weather(df):
    """
    Exercise 3: Weather Data Analysis with Pandas
    ------------------------------------------
    Task: Analyze temperature and precipitation patterns.
    
    Required steps:
    1. Calculate basic statistics:
       - Monthly temperature averages
       - Total precipitation by month
       - Seasonal patterns
       - Temperature-precipitation correlation
    
    2. Create seasonal analysis:
       - Group data by seasons
       - Calculate seasonal averages
       - Identify extreme weather months
    
    3. Create visualizations:
       - Dual-axis plot for temperature and precipitation
       - Seasonal temperature averages
       - Temperature distribution
       - Temperature vs precipitation scatter plot
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame with columns:
        - Month: month names
        - Temperature: temperature values in Celsius
        - Precipitation: precipitation values in mm
    
    Expected Output:
    --------------
    1. Four-panel figure showing:
       - Temperature and precipitation trends
       - Seasonal averages
       - Temperature distribution
       - Correlation scatter plot
    2. Dictionary with weather statistics
    
    Hint: Use pd.cut for seasonal grouping
    """

    monthly_temp_avg = df.groupby('Month')['Temperature'].mean()  # Monthly temperature averages
    monthly_precip_total = df.groupby('Month')['Precipitation'].sum()  # Monthly precipitation
    temp_precip_corr = df['Temperature'].corr(df['Precipitation'])  # Temperature-precipitation correlation

    # Seasonal grouping
    month_mapping = {
        'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
        'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
    }
    df['Month_Num'] = df['Month'].map(month_mapping)

    seasons = pd.cut(df['Month_Num'],
                     bins=[-1, 2, 5, 8, 11],
                     labels=['Winter', 'Spring', 'Summer', 'Fall'],
                     include_lowest=True)
    df['Season'] = seasons

    seasonal_temp_avg = df.groupby('Season')['Temperature'].mean()
    seasonal_precip_total = df.groupby('Season')['Precipitation'].sum()

    # Extreme weather months
    extreme_weather_months = {
        'Highest Temperature': df['Month'][df['Temperature'].idxmax()],
        'Lowest Temperature': df['Month'][df['Temperature'].idxmin()],
        'Most Precipitation': df['Month'][df['Precipitation'].idxmax()],
        'Least Precipitation': df['Month'][df['Precipitation'].idxmin()]
    }

    # Dictionary with statistics
    stats = {
        'Monthly Temperature Averages': monthly_temp_avg.to_dict(),
        'Monthly Precipitation Totals': monthly_precip_total.to_dict(),
        'Seasonal Temperature Averages': seasonal_temp_avg.to_dict(),
        'Seasonal Precipitation Totals': seasonal_precip_total.to_dict(),
        'Temperature-Precipitation Correlation': temp_precip_corr,
        'Extreme Weather Months': extreme_weather_months
    }

    # Plots
    fig, axes = plt.subplots(2, 2, figsize=(16, 10))

    # Temperature and precipitation trends
    ax1 = axes[0, 0]
    ax2 = ax1.twinx()
    ax1.bar(df['Month'], df['Precipitation'], color='blue', alpha=0.5, label='Precipitation (mm)')
    ax2.plot(df['Month'], df['Temperature'], color='red', label='Temperature (°C)')
    ax1.set_title('Monthly Temperature and Precipitation')
    ax1.set_ylabel('Precipitation (mm)')
    ax2.set_ylabel('Temperature (°C)')
    ax1.set_xticks(range(len(df['Month'])))
    ax1.set_xticklabels(df['Month'], rotation=45)
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')

    # Seasonal averages
    axes[0, 1].bar(seasonal_temp_avg.index, seasonal_temp_avg.values, color='orange',alpha=0.5)
    axes[0, 1].set_title('Seasonal Average Temperature')
    axes[0, 1].set_ylabel('Temperature (°C)')

    # Temperature distribution
    axes[1, 0].hist(df['Temperature'], bins=10, color='green', alpha=0.7)
    axes[1, 0].set_title('Temperature Distribution')
    axes[1, 0].set_xlabel('Temperature (°C)')
    axes[1, 0].set_ylabel('Frequency')

    # Correlation scatter plot
    axes[1, 1].scatter(df['Temperature'], df['Precipitation'], color='purple', alpha=0.6)
    axes[1, 1].set_title('Temperature vs Precipitation')
    axes[1, 1].set_xlabel('Temperature (°C)')
    axes[1, 1].set_ylabel('Precipitation (mm)')

    plt.show()

    return stats
