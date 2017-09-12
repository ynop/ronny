import os
import re
import collections

wc_path_pattern = re.compile(r'(<{2,3})(.*?)(>{2,3})')


class Workflow(object):
    def __init__(self, config, available_tasks={}, work_dir=None, output_path=None, cache_path=None):
        self.available_tasks = available_tasks

        if work_dir is None:
            self.work_dir = os.getcwd()
        else:
            self.work_dir = work_dir

        self.output_path = os.path.join(self.work_dir, output_path)
        self.cache_path = os.path.join(self.work_dir, cache_path)

        self.config = config
        self.tasks = self._load_tasks()

    def run(self, tasks_to_execute=[]):
        for task in sorted(self.tasks.values(), key=lambda x: x.execution_index):
            if len(tasks_to_execute) == 0 or task.execution_index in tasks_to_execute or task.identifier in tasks_to_execute:
                task.start()

    def _load_tasks(self):
        tasks = collections.OrderedDict()

        for index, task_config in enumerate(self.config['tasks']):
            identifier = task_config['identifier']
            name = task_config['name']

            if not name in self.available_tasks.keys():
                raise ValueError('No task found for with name {}'.format(name))

            task_class = self.available_tasks[name]
            task_output_path = None

            if self.output_path is not None:
                task_output_path = os.path.join(self.output_path, '{}_{}'.format(index, identifier))
                os.makedirs(task_output_path, exist_ok=True)

            task_cache_path = None

            if self.cache_path is not None:
                task_cache_path = os.path.join(self.cache_path, '{}_{}'.format(index, identifier))
                os.makedirs(task_cache_path, exist_ok=True)

            task_config = self._replace_rel_paths_in_config(task_config, task_output_path, task_cache_path, tasks)
            task = task_class(index, task_config, identifier=identifier, work_dir=self.work_dir, output_path=task_output_path, cache_path=task_cache_path)

            tasks[task.identifier] = task

        return tasks

    def _replace_rel_paths_in_config(self, task_config, task_output_path, task_cache_path, other_tasks):
        if type(task_config) == list:
            return [self._replace_rel_paths_in_config(x, task_output_path, task_cache_path, other_tasks) for x in task_config]
        elif type(task_config) == dict:
            return {k: self._replace_rel_paths_in_config(v, task_output_path, task_cache_path, other_tasks) for k, v in task_config.items()}
        elif type(task_config) == str:
            result = task_config
            for match in re.finditer(wc_path_pattern, task_config):
                to_replace = match.group(0)
                prefix = match.group(1)
                ref_task_id = match.group(2)
                suffix = match.group(3)

                cache_replace = prefix == '<<<' and suffix == '>>>'

                if ref_task_id == '':
                    replacement = task_cache_path if cache_replace else task_output_path
                else:
                    other_task = other_tasks[ref_task_id]
                    replacement = other_task.cache_path if cache_replace else other_task.output_path

                result = str(result).replace(to_replace, replacement)
            return result
        else:
            return task_config
