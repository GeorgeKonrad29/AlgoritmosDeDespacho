from tkinter import Tk, Canvas, Text, Scrollbar, VERTICAL, RIGHT, Y, END
import random

class GanttChart:
    def __init__(self, master):
        self.master = master
        self.master.title("Gantt Chart")
        self.canvas = Canvas(master, width=1200, height=500)  # Increased width for scalability
        self.canvas.pack()

        # Create a Text widget for the table
        self.text = Text(master, height=10, width=80)
        self.text.pack(side=RIGHT, fill=Y)

        # Add a scrollbar to the Text widget
        self.scrollbar = Scrollbar(master, orient=VERTICAL, command=self.text.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.text.config(yscrollcommand=self.scrollbar.set)

    def draw_chart(self, tasks):
        min_start_time = min(task['arrival'] for task in tasks)
        max_end_time = max(task['end'] for task in tasks)
        total_duration = max_end_time - min_start_time

        # Draw horizontal lines and labels
        for i, task in enumerate(tasks):
            y_position = i * 50 + 50
            self.canvas.create_line(100, y_position, 2000, y_position, fill='black')  # Adjusted end position
            self.canvas.create_text(50, y_position + 15, text=task['name'], anchor='e')

        # Draw vertical lines and labels
        for t in range(total_duration + 1):
            x_position = 100 + t * 20  # Keep the interval at 20
            self.canvas.create_line(x_position, 50, x_position, 50 + len(tasks) * 50, fill='black')
            self.canvas.create_text(x_position, 50 + len(tasks) * 50 + 10, text=str(t), anchor='n')

        # Draw tasks
        for i, task in enumerate(tasks):
            if i > 0:
                prev_end_time = tasks[i-1]['end']
                task['start'] = max(task['arrival'], prev_end_time)
                task['end'] = task['start'] + task['duration']
            else:
                task['start'] = task['arrival']
                task['end'] = task['start'] + task['duration']

            start_time = task['start']
            end_time = task['end']
            duration = end_time - start_time
            start_offset = start_time - min_start_time
            y_position = i * 50 + 50

            # Generate a random color
            color = "#{:06x}".format(random.randint(0, 0xFFFFFF))

            self.canvas.create_rectangle(
                100 + start_offset * 20, y_position, 100 + (start_offset + duration) * 20, y_position + 30,
                fill=color
            )

        # Calculate waiting times and turnaround times
        waiting_times = []
        turnaround_times = []
        for i, task in enumerate(tasks):
            waiting_time = task['start'] - task['arrival']
            turnaround_time = task['end'] - task['arrival']
            waiting_times.append(waiting_time)
            turnaround_times.append(turnaround_time)

        # Print the tables in the Text widget
        self.text.insert(END, "Task\tArrival\tStart\tEnd\tWaiting Time\tTurnaround Time\n")
        for i, task in enumerate(tasks):
            self.text.insert(END, f"{task['name']}\t{task['arrival']}\t{task['start']}\t{task['end']}\t{waiting_times[i]}\t\t{turnaround_times[i]}\n")

def main():
    root = Tk()
    chart = GanttChart(root)

    tasks = [
        {'name': 'Task 1', 'arrival': 0, 'duration': random.randint(4, 15)},
        {'name': 'Task 2', 'arrival': random.randint(1, 5), 'duration': random.randint(4, 15)},
        {'name': 'Task 3', 'arrival': random.randint(6, 10), 'duration': random.randint(4, 15)},
        {'name': 'Task 4', 'arrival': random.randint(11, 15), 'duration': random.randint(4, 15)},
        {'name': 'Task 5', 'arrival': random.randint(16, 20), 'duration': random.randint(4, 15)},
    ]

    # Sort tasks by arrival time to ensure correct order
    tasks.sort(key=lambda x: x['arrival'])

    # Add start and end attributes to tasks
    for i, task in enumerate(tasks):
        if i > 0:
            prev_end_time = tasks[i-1]['end']
            task['start'] = max(task['arrival'], prev_end_time)
            task['end'] = task['start'] + task['duration']
        else:
            task['start'] = task['arrival']
            task['end'] = task['start'] + task['duration']

    chart.draw_chart(tasks)
    root.mainloop()

if __name__ == "__main__":
    main()