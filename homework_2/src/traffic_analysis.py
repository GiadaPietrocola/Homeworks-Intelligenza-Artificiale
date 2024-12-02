"""Traffic Analysis Exercise""" 
import pandas as pd 
import matplotlib.pyplot as plt 


def analyze_traffic(df):
    """
    Exercise 4: Website Traffic Analysis with Pandas
    --------------------------------------------
    Task: Analyze website traffic patterns and bounce rates.
    
    Required steps:
    1. Time series analysis:
       - Calculate daily traffic patterns
       - Compute moving averages (3-day and 7-day)
       - Identify weekly patterns
    
    2. Bounce rate analysis:
       - Calculate average bounce rates
       - Correlate bounce rates with traffic
       - Identify high/low bounce rate periods
    
    3. Create visualizations:
       - Traffic trends with moving averages
       - Daily traffic patterns
       - Bounce rate trends
       - Traffic vs bounce rate correlation
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame with columns:
        - Date: datetime index
        - Visitors: daily visitor count
        - Bounce_Rate: daily bounce rate percentage
    
    Expected Output:
    --------------
    1. Four-panel figure showing:
       - Traffic trends with moving averages
       - Average daily traffic patterns
       - Bounce rate trend
       - Correlation scatter plot
    2. Dictionary with traffic statistics
    
    Hint: Use df.rolling for moving averages
    """

    df['Date'] = pd.to_datetime(df['Date'])
    df = df.set_index('Date')

    # Daily traffic patterns
    daily_pattern = df.groupby(df.index.day_name())['Visitors'].mean().reindex(
        ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    )

    # Moving averages
    df['3_day_MA'] = df['Visitors'].rolling(window=3).mean()
    df['7_day_MA'] = df['Visitors'].rolling(window=7).mean()

    # Weekly patterns
    weekly_pattern = df.resample('W')['Visitors'].mean()

    # Bounce rate analysis
    avg_bounce_rate = df['Bounce_Rate'].mean()
    traffic_bounce_corr = df['Visitors'].corr(df['Bounce_Rate'])

    # Identify high and low bounce rate periods
    high_bounce_threshold = 50
    low_bounce_threshold = 30

    high_bounce = df[df['Bounce_Rate'] > high_bounce_threshold]
    low_bounce = df[df['Bounce_Rate'] < low_bounce_threshold]

    # Dictionary with statistics
    stats = {
        'Daily Traffic Pattern': daily_pattern.to_dict(),
        'Weekly Traffic Pattern': weekly_pattern.to_dict(),
        'Average Bounce Rate': avg_bounce_rate,
        'Traffic-Bounce Correlation': traffic_bounce_corr,
        'High Bounce Periods': high_bounce.index.tolist(),
        'Low Bounce Periods': low_bounce.index.tolist()
    }

    # Plots
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # Traffic trends with moving averages
    axes[0, 0].plot(df.index, df['Visitors'], label='Visitors', color='blue')
    axes[0, 0].plot(df.index, df['3_day_MA'], label='3-Day MA', color='orange')
    axes[0, 0].plot(df.index, df['7_day_MA'], label='7-Day MA', color='green')
    axes[0, 0].set_title('Traffic Trends with Moving Averages')
    axes[0, 0].legend()
    reduced_ticks = df.index[::7]
    axes[0, 0].set_xticks(reduced_ticks)
    formatted_ticks = [date.strftime('%Y-%m-%d') for date in reduced_ticks]
    axes[0, 0].set_xticklabels(formatted_ticks, rotation=45)

    # Daily traffic patterns
    axes[0, 1].bar(daily_pattern.index, daily_pattern.values, color='skyblue')
    axes[0, 1].set_title('Daily Traffic Patterns')
    axes[0, 1].set_ylabel('Average Visitors')
    axes[0, 1].set_xticks(daily_pattern.index)
    axes[0, 1].set_xticklabels(daily_pattern.index,rotation=45)

    # Bounce rate trends
    axes[1, 0].plot(df.index, df['Bounce_Rate'], color='red')
    axes[1, 0].set_title('Bounce Rate Trends')
    axes[1, 0].set_ylabel('Bounce Rate (%)')
    axes[1, 0].set_xticks(df.index)
    reduced_ticks = df.index[::7]
    axes[1, 0].set_xticks(reduced_ticks)
    formatted_ticks = [date.strftime('%Y-%m-%d') for date in reduced_ticks]
    axes[1, 0].set_xticklabels(formatted_ticks, rotation=45)

    # Traffic vs Bounce Rate
    axes[1, 1].scatter(df['Visitors'], df['Bounce_Rate'], alpha=0.7, color='purple')
    axes[1, 1].set_title('Traffic vs Bounce Rate Correlation')
    axes[1, 1].set_xlabel('Visitors')
    axes[1, 1].set_ylabel('Bounce Rate (%)')

    plt.tight_layout()
    plt.show()

    return stats
