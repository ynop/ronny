import sys
import argparse
import os

import yaml

from . import workflow


class Runner(object):
    tasks = [

    ]

    out_and_cache_subfolder_with_sumatra_label = True

    def run(self):
        parser = argparse.ArgumentParser(description='Run workflow')
        parser.add_argument('config_path', type=str)
        parser.add_argument('--out', type=str, default=None)
        parser.add_argument('--cache', type=str, default=None)
        parser.add_argument('--from-stage', type=int, default=None)
        parser.add_argument('--to-stage', type=int, default=None)

        args = parser.parse_args()

        config = self._load_config(args.config_path)
        out_path = args.out
        cache_path = args.cache

        if self.out_and_cache_subfolder_with_sumatra_label:
            if out_path:
                out_path = os.path.join(out_path, config['sumatra_label'])
            if cache_path:
                cache_path = os.path.join(cache_path, config['sumatra_label'])

        wf = workflow.Workflow(config, available_tasks=self._get_task_dictionary(), output_path=out_path, cache_path=cache_path)
        wf.run()

    def _get_task_dictionary(self):
        return {k.name: k for k in self.tasks}

    def _load_config(self, path):
        with open(path, 'r') as yml_file:
            cfg = yaml.load(yml_file)

        return cfg
