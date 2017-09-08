import os
import re


class Workflow(object):
    def __init__(self, config, available_tasks={}, output_path=None, cache_path=None):
        self.available_tasks = available_tasks

        self.output_path = output_path
        self.cache_path = cache_path

        self.config = config
        self.tasks = self._load_tasks()

    def run(self, tasks_to_execute=[]):
        for task in sorted(self.tasks, key=lambda x: x.execution_index):
            if len(tasks_to_execute) == 0 or task.execution_index in tasks_to_execute or task.identifier in tasks_to_execute:
                task.start()

    def add_task(self, task):
        self.tasks.append(task)

    def _load_tasks(self):
        tasks = []

        for index, task_config in enumerate(self.config['tasks']):
            identifier = task_config['identifier']
            name = task_config['name']

            if not name in self.available_tasks.keys():
                raise ValueError('No task found for with name {}'.format(name))

            task_class = self.available_tasks[name]
            task_output_path = None

            if self.output_path is not None:
                task_output_path = os.path.join(self.output_path, '{}_{}'.format(index, identifier))
                os.makedirs(task_output_path)

            task_cache_path = None

            if self.cache_path is not None:
                task_cache_path = os.path.join(self.cache_path, '{}_{}'.format(index, identifier))
                os.makedirs(task_cache_path)

            task = task_class(index, task_config, identifier=identifier, output_path=task_output_path, cache_path=task_cache_path)

            tasks.append(task)

        return tasks
