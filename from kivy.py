from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from datetime import datetime, timedelta
from kivy.clock import Clock
from kivy.metrics import dp

class Task:
    def __init__(self, name):
        self.name = name
        self.time = timedelta(seconds=0)
        self.start_time = None
        self.is_running = False
        
class TimeTrackerApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tasks = []
        self.active_task = None  
    def build(self):
     root = BoxLayout(orientation='vertical')
     main_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
     task_input_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=dp(50), spacing=dp(10))
     self.task_input = TextInput(hint_text='Enter task name')    
     add_task_button = Button(text='Add Task', on_release=self.add_task, size_hint=(None, 1), width=120)
     task_input_layout.add_widget(self.task_input)
     task_input_layout.add_widget(add_task_button)
     self.total_time_label = Label(
        text='Total Time: 00:00:00', size_hint=(1, None), height=dp(30),
        halign='center', valign='middle'
     )
     self.task_list = BoxLayout(orientation='vertical', spacing=dp(10))
     main_layout.add_widget(task_input_layout)
     main_layout.add_widget(self.task_list)
     main_layout.add_widget(self.total_time_label)
     root.add_widget(main_layout)
     return root

    def add_task(self, instance):
        task_name = self.task_input.text.strip()
        if task_name:
            task = Task(task_name)
            task_layout = BoxLayout(orientation='horizontal', size_hint=(0.8, None), height=dp(30))
            task_label = Label(text=task_name, size_hint=(0.6, None), height=dp(30), halign='left', valign='middle')
            time_label = Label(text='00:00:00', size_hint=(0.4, None), height=dp(30), halign='left', valign='middle')
            start_button = Button(text='Start', size_hint=(0.2, None), height=dp(40), halign='right', valign='middle')
            stop_button = Button(text='Stop', size_hint=(0.2, None), height=dp(40), halign='right', valign='middle')
            delete_button = Button(text='Delete', size_hint=(0.2, None), height=dp(40), halign='right', valign='middle')
            start_button.bind(on_release=lambda instance: self.start_timer(task, time_label))
            stop_button.bind(on_release=lambda instance: self.stop_timer(task))
            delete_button.bind(on_release=lambda instance: self.delete_task(task, task_layout))
            task_layout.add_widget(task_label)
            task_layout.add_widget(time_label)
            task_layout.add_widget(start_button)
            task_layout.add_widget(stop_button)
            task_layout.add_widget(delete_button)
            self.task_list.add_widget(task_layout)
            self.tasks.append(task)
            self.task_input.text = ''
    def start_timer(self, task, time_label):
        if self.active_task and self.active_task.is_running:
            return  
        task.start_time = datetime.now()
        task.is_running = True
        self.active_task = task  
        self.schedule = Clock.schedule_interval(lambda dt: self.update(task, time_label), 0.1)
    def stop_timer(self, task):
        if task.is_running:
            elapsed_time = datetime.now() - task.start_time
            task.time += elapsed_time
            task.start_time = None
            task.is_running = False

            if task == self.active_task:
                self.active_task = None  

            Clock.unschedule(self.update)
    def delete_task(self, task, task_layout):
        self.tasks.remove(task)
        self.task_list.remove_widget(task_layout)
        if len(self.tasks) == 0:
            self.total_time_label.text = "Total Time: 00:00:00"
    def update(self, task, time_label):
        if task.is_running:
            elapsed_time = datetime.now() - task.start_time
            task.time += elapsed_time
            task.start_time = datetime.now()
        seconds = task.time.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        time_label.text = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        total_time = sum((task.time for task in self.tasks), timedelta())
        hours = total_time.seconds // 3600
        minutes = (total_time.seconds % 3600) // 60
        seconds = total_time.seconds % 60
        self.total_time_label.text = f"Total Time: {hours:02d}:{minutes:02d}:{seconds:02d}"
    def on_stop(self):
        Clock.unschedule(self.update)
    def on_start(self):
        self.schedule = Clock.schedule_interval(lambda dt: self.update_total_time(), 1)
    def update_total_time(self):
        total_time = sum((task.time for task in self.tasks), timedelta())
        hours = total_time.seconds // 3600
        minutes = (total_time.seconds % 3600) // 60
        seconds = total_time.seconds % 60
        self.total_time_label.text = f"Total Time: {hours:02d}:{minutes:02d}:{seconds:02d}"

if __name__ == '__main__':
    TimeTrackerApp().run()
