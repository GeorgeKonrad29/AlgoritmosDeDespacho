def create_gantt_chart(tasks):
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    from datetime import datetime

    fig, ax = plt.subplots(figsize=(10, 6))

    for i, task in enumerate(tasks):
        start_date = datetime.strptime(task['start'], '%Y-%m-%d')
        end_date = datetime.strptime(task['end'], '%Y-%m-%d')
        ax.barh(task['name'], (end_date - start_date).days, left=start_date.toordinal(), color='skyblue')

    ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.xticks(rotation=45)
    plt.xlabel('Date')
    plt.ylabel('Tasks')
    plt.title('Gantt Chart')
    plt.grid(True)
    plt.tight_layout()
    plt.show()