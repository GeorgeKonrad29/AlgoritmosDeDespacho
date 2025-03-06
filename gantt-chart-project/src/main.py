from tkinter import Tk, Canvas, Text, Scrollbar, VERTICAL, RIGHT, Y, END, Toplevel
import random

class GanttChart:
    def __init__(self, master, title):
        self.master = master
        self.master.title(title)
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
            self.canvas.create_line(100, y_position, 1100, y_position, fill='black')  # Adjusted end position
            self.canvas.create_text(50, y_position + 15, text=task['name'], anchor='e')

        # Draw vertical lines and labels
        for t in range(total_duration + 1):
            x_position = 100 + t * 20  # Keep the interval at 20
            self.canvas.create_line(x_position, 50, x_position, 50 + len(tasks) * 50, fill='black')
            self.canvas.create_text(x_position, 50 + len(tasks) * 50 + 10, text=str(t), anchor='n')

        # Draw tasks
        for i, task in enumerate(tasks):
            start_time = task['start']
            end_time = task['end']
            duration = end_time - start_time
            start_offset = start_time - min_start_time
            y_position = i * 50 + 50

            self.canvas.create_rectangle(
                100 + start_offset * 20, y_position, 100 + (start_offset + duration) * 20, y_position + 30,
                fill=task['color']
            )

        # Calculate waiting times and turnaround times
        waiting_times = []
        turnaround_times = []
        for i, task in enumerate(tasks):
            waiting_time = task['start'] - task['arrival']
            turnaround_time = task['end'] - task['arrival']
            waiting_times.append(waiting_time)
            turnaround_times.append(turnaround_time)

        # Calculate average waiting time and turnaround time
        avg_waiting_time = sum(waiting_times) / len(waiting_times)
        avg_turnaround_time = sum(turnaround_times) / len(turnaround_times)

        # Print the tables in the Text widget
        self.text.insert(END, "Procesos\tLlegada\tInicio\tFin\tT.Espera\tT.Sistema\n")
        for i, task in enumerate(tasks):
            self.text.insert(END, f"{task['name']}\t{task['arrival']}\t{task['start']}\t{task['end']}\t{waiting_times[i]}\t\t{turnaround_times[i]}\n")
        self.text.insert(END, f"\nPromedio\t\t\t\t{avg_waiting_time:.2f}\t\t{avg_turnaround_time:.2f}\n")

def ordenador(tasks):
    tiempoTotalSistema = sum([task['duration'] for task in tasks])
    newTasks = []
    sortedTasks = sorted(tasks, key=lambda x: x['arrival'])
    newTasks.append(sortedTasks[0])
    sortedTasks.pop(0)
    tiemposDeFinProceso = newTasks[0]['duration']
    candidatos = []
    for i in range(len(sortedTasks)):
        for j in range(len(sortedTasks)):
            if sortedTasks[j]['arrival'] <= tiemposDeFinProceso:
                candidatos.append(sortedTasks[j])
        if len(candidatos) > 0:
            candidatos = sorted(candidatos, key=lambda x: x['duration'])
            newTasks.append(candidatos[0])
            tiemposDeFinProceso += candidatos[0]['duration']
            sortedTasks.remove(candidatos[0])
            candidatos = []
        else:
            newTasks.append(sortedTasks[0])
            tiemposDeFinProceso += sortedTasks[0]['duration']
            sortedTasks.pop(0)
        if tiemposDeFinProceso >= tiempoTotalSistema:
            return newTasks
    return newTasks

def ordenadorPrioridad(tasks):
    tiempoTotalSistema = sum([task['duration'] for task in tasks])
    newTasks = []
    sortedTasks = sorted(tasks, key=lambda x: x['arrival'])
    newTasks.append(sortedTasks[0])
    sortedTasks.pop(0)
    tiemposDeFinProceso = newTasks[0]['duration']
    candidatos = []
    for i in range(len(sortedTasks)):
        for j in range(len(sortedTasks)):
            if sortedTasks[j]['arrival'] <= tiemposDeFinProceso:
                candidatos.append(sortedTasks[j])
        if len(candidatos) > 0:
            candidatos = sorted(candidatos, key=lambda x: x['priority'])
            newTasks.append(candidatos[0])
            tiemposDeFinProceso += candidatos[0]['duration']
            sortedTasks.remove(candidatos[0])
            candidatos = []
        else:
            newTasks.append(sortedTasks[0])
            tiemposDeFinProceso += sortedTasks[0]['duration']
            sortedTasks.pop(0)
        if tiemposDeFinProceso >= tiempoTotalSistema:
            return newTasks
    return newTasks

def main():
    root = Tk()

    # Generate tasks
    tasks = [
        {'name': 'Task 1', 'arrival': 0, 'duration': random.randint(4, 12), 'priority': random.randint(1, 5)},
        {'name': 'Task 2', 'arrival': random.randint(1, 5), 'duration': random.randint(4, 12), 'priority': random.randint(1, 5)},
        {'name': 'Task 3', 'arrival': random.randint(1, 5), 'duration': random.randint(4, 12), 'priority': random.randint(1, 5)},
        {'name': 'Task 4', 'arrival': random.randint(1, 5), 'duration': random.randint(4, 12), 'priority': random.randint(1, 5)},
        {'name': 'Task 5', 'arrival': random.randint(1, 5), 'duration': random.randint(4, 12), 'priority': random.randint(1, 5)},
    ]

    # Assign random colors to tasks
    for task in tasks:
        task['color'] = "#{:06x}".format(random.randint(0, 0xFFFFFF))

    # First Come First Serve (FCFS) Algorithm
    fcfs_tasks = sorted(tasks, key=lambda x: x['arrival'])

    # Add start and end attributes to tasks
    for i, task in enumerate(fcfs_tasks):
        if i > 0:
            prev_end_time = fcfs_tasks[i-1]['end']
            task['start'] = max(task['arrival'], prev_end_time)
            task['end'] = task['start'] + task['duration']
        else:
            task['start'] = task['arrival']
            task['end'] = task['start'] + task['duration']

    fcfs_chart = GanttChart(root, "FCFS Gantt Chart")
    fcfs_chart.draw_chart(fcfs_tasks)

    # Shortest Job First (SJF) Algorithm
    sjf_tasks = ordenador(tasks)

    # Add start and end attributes to tasks
    current_time = 0
    for i, task in enumerate(sjf_tasks):
        if i > 0:
            prev_end_time = sjf_tasks[i-1]['end']
            task['start'] = max(task['arrival'], prev_end_time)
            task['end'] = task['start'] + task['duration']
        else:
            task['start'] = task['arrival']
            task['end'] = task['start'] + task['duration']
        current_time = task['end']

        # Sort remaining tasks by duration, considering only those that have arrived
        remaining_tasks = sjf_tasks[i+1:]
        remaining_tasks = [t for t in remaining_tasks if t['arrival'] <= current_time]
        remaining_tasks.sort(key=lambda x: x['duration'])
        sjf_tasks[i+1:i+1+len(remaining_tasks)] = remaining_tasks

    # Create a new window for SJF Gantt Chart
    sjf_window = Toplevel(root)
    sjf_window.geometry("+1300+0")  # Position the window to the right of the main window
    sjf_chart = GanttChart(sjf_window, "SJF Gantt Chart")
    sjf_chart.draw_chart(sjf_tasks)

    # Priority Algorithm
    priority_tasks = ordenadorPrioridad(tasks)

    # Add start and end attributes to tasks
    for i, task in enumerate(priority_tasks):
        if i > 0:
            prev_end_time = priority_tasks[i-1]['end']
            task['start'] = max(task['arrival'], prev_end_time)
            task['end'] = task['start'] + task['duration']
        else:
            task['start'] = task['arrival']
            task['end'] = task['start'] + task['duration']

    # Create a new window for Priority Gantt Chart
    priority_window = Toplevel(root)
    priority_window.geometry("+1100+0")  # Position the window to the right of the SJF window
    priority_chart = GanttChart(priority_window, "Priority Gantt Chart")
    priority_chart.draw_chart(priority_tasks)

    root.mainloop()

if __name__ == "__main__":
    main()