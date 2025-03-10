from tkinter import Tk, Canvas, Text, Scrollbar, VERTICAL, HORIZONTAL, RIGHT, Y, END, Frame, BOTH, LEFT, BOTTOM, X, simpledialog
import random

class GanttChart:
    def __init__(self, master):
        self.master = master

        # Create a frame for the Gantt charts
        self.chart_frame = Frame(master)
        self.chart_frame.pack(side=RIGHT, fill=BOTH, expand=True)

        # Create a canvas for the Gantt charts
        self.chart_canvas = Canvas(self.chart_frame, width=10000, height=5000)  # Increased height for scalability
        self.chart_canvas.pack(side=RIGHT, fill=BOTH, expand=True)

        # Add a vertical scrollbar to the Gantt chart canvas
        self.v_scrollbar = Scrollbar(self.chart_frame, orient=VERTICAL, command=self.chart_canvas.yview)
        self.v_scrollbar.pack(side=LEFT, fill=Y)
        self.chart_canvas.config(yscrollcommand=self.v_scrollbar.set)

        # Add a horizontal scrollbar to the Gantt chart canvas
        self.h_scrollbar = Scrollbar(self.chart_frame, orient=HORIZONTAL, command=self.chart_canvas.xview)
        self.h_scrollbar.pack(side=BOTTOM, fill=X)
        self.chart_canvas.config(xscrollcommand=self.h_scrollbar.set)

        # Create a frame for the tables
        self.table_frame = Frame(master)
        self.table_frame.pack(side=RIGHT, fill=Y)

        # Create a Text widget for the table
        self.text = Text(self.table_frame, height=50, width=60)
        self.text.pack(side=RIGHT, fill=Y)

        # Add a scrollbar to the Text widget
        self.text_scrollbar = Scrollbar(self.table_frame, orient=VERTICAL, command=self.text.yview)
        self.text_scrollbar.pack(side=RIGHT, fill=Y)
        self.text.config(yscrollcommand=self.text_scrollbar.set)

    def draw_chart(self, tasks, title, y_offset):
        min_start_time = min(task['arrival'] for task in tasks)
        max_end_time = max(task['end'] for task in tasks)
        total_duration = max_end_time - min_start_time

        # Draw title
        self.chart_canvas.create_text(600, y_offset - 30, text=title, font=('Arial', 16, 'bold'))

        # Draw horizontal lines and labels
        for i, task in enumerate(tasks):
            y_position = y_offset + i * 50 + 50
            self.chart_canvas.create_line(100, y_position, 100 + total_duration * 20, y_position, fill='black')  # Adjusted end position
            self.chart_canvas.create_text(50, y_position + 15, text=task['name'], anchor='e')

        # Draw vertical lines and labels
        for t in range(total_duration + 1):
            x_position = 100 + t * 20  # Keep the interval at 20
            self.chart_canvas.create_line(x_position, y_offset + 50, x_position, y_offset + 50 + len(tasks) * 50, fill='black')
            self.chart_canvas.create_text(x_position, y_offset + 50 + len(tasks) * 50 + 10, text=str(t), anchor='n')

        # Draw tasks
        for i, task in enumerate(tasks):
            start_time = task['start']
            end_time = task['end']
            duration = end_time - start_time
            start_offset = start_time - min_start_time
            y_position = y_offset + i * 50 + 50

            self.chart_canvas.create_rectangle(
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
        self.text.insert(END, f"{title}\n")
        self.text.insert(END, "Proceso\tDuración\tLlegada\tPrioridad\tT.Espera\tT.Sistema\n")
        for i, task in enumerate(tasks):
            self.text.insert(END, f"{task['name']}\t{task['duration']}\t{task['arrival']}\t{task['priority']}\t   {waiting_times[i]}\t    {turnaround_times[i]}\n")
        self.text.insert(END, f"\nPromedio\t\t\t\t   {avg_waiting_time:.2f}\t   {avg_turnaround_time:.2f}\n\n")
        # Return the new y_offset for the next chart
        return y_offset + len(tasks) * 50 + 200

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
            print(newTasks)
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

def on_mouse_wheel(event, canvas):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

def on_arrow_key(event, canvas):
    if event.keysym == 'Up':
        canvas.yview_scroll(-1, "units")
    elif event.keysym == 'Down':
        canvas.yview_scroll(1, "units")
    elif event.keysym == 'Left':
        canvas.xview_scroll(-1, "units")
    elif event.keysym == 'Right':
        canvas.xview_scroll(1, "units")

def generate_gantt_charts(num_tasks, gantt_chart):
    # Generate tasks
    tasks = []
    for i in range(num_tasks):
        tasks.append({
            'name': f'Task {i+1}',
            'arrival': random.randint(0, 10),
            'duration': random.randint(4, 12),
            'priority': random.randint(1, 5),
            'color': "#{:06x}".format(random.randint(0, 0xFFFFFF))
        })

    y_offset = 50

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

    y_offset = gantt_chart.draw_chart(fcfs_tasks, "FCFS Gantt Chart", y_offset)

    # Shortest Job First (SJF) Algorithm
    sjf_tasks = ordenador(fcfs_tasks)

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

    y_offset = gantt_chart.draw_chart(sjf_tasks, "SJF Gantt Chart", y_offset)

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

    gantt_chart.draw_chart(priority_tasks, "Priority Gantt Chart", y_offset)

def main():
    root = Tk()
    root.geometry("1800x1500")

    # Ask the user for the number of tasks
    num_tasks = simpledialog.askinteger("Input", "How many tasks do you want to generate?", minvalue=1, maxvalue=100)

    # Create a frame for the Gantt charts
    chart_frame = Frame(root)
    chart_frame.pack(side=LEFT, fill=BOTH, expand=True)

    # Create a canvas with a scrollbar for the Gantt charts
    main_canvas = Canvas(chart_frame)
    main_canvas.pack(side=LEFT, fill=BOTH, expand=True)

    v_scrollbar = Scrollbar(chart_frame, orient=VERTICAL, command=main_canvas.yview)
    v_scrollbar.pack(side=RIGHT, fill=Y)

    h_scrollbar = Scrollbar(chart_frame, orient=HORIZONTAL, command=main_canvas.xview)
    h_scrollbar.pack(side=BOTTOM, fill=X)

    main_canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
    main_canvas.bind('<Configure>', lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all")))

    frame = Frame(main_canvas)
    main_canvas.create_window((0, 0), window=frame, anchor="nw")

    # Bind the mouse wheel event to the canvas
    main_canvas.bind_all("<MouseWheel>", lambda event: on_mouse_wheel(event, main_canvas))

    # Bind the arrow keys to the canvas
    main_canvas.bind_all("<KeyPress-Up>", lambda event: on_arrow_key(event, main_canvas))
    main_canvas.bind_all("<KeyPress-Down>", lambda event: on_arrow_key(event, main_canvas))
    main_canvas.bind_all("<KeyPress-Left>", lambda event: on_arrow_key(event, main_canvas))
    main_canvas.bind_all("<KeyPress-Right>", lambda event: on_arrow_key(event, main_canvas))

    gantt_chart = GanttChart(frame)

    # Generate Gantt charts
    generate_gantt_charts(num_tasks, gantt_chart)
    root.attributes('-topmost', True)
    root.mainloop()

if __name__ == "__main__":
    main()