import sys
import argparse
import os
import re

import yaml

from . import workflow


class Runner(object):
    tasks = [

    ]

    out_and_cache_subfolder_with_sumatra_label = True

    def run(self):
        parser = argparse.ArgumentParser(description='Run workflow')
        parser.add_argument('config_path', type=str)
        parser.add_argument('--workdir', type=str, default=None)
        parser.add_argument('--out', type=str, default=None)
        parser.add_argument('--cache', type=str, default=None)
        parser.add_argument('--range', type=str, default=None)

        args = parser.parse_args()

        config = self._load_config(args.config_path)
        out_path = args.out
        cache_path = args.cache

        if self.out_and_cache_subfolder_with_sumatra_label and 'sumatra_label' in config:
            if out_path:
                out_path = os.path.join(out_path, config['sumatra_label'])
            if cache_path:
                cache_path = os.path.join(cache_path, config['sumatra_label'])

        tasks = []

        if args.range:
            single_id_match = re.match(r'^(\d*)$', args.range)
            start_end_match = re.match(r'^(\d*)-(\d*)$', args.range)

            if single_id_match is not None:
                tasks = [int(single_id_match.group(1))]
            elif start_end_match is not None:
                start = int(start_end_match.group(1))
                end = int(start_end_match.group(2))

                if end >= start:
                    tasks = [x for x in range(start, end + 1)]

        wf = workflow.Workflow(config, available_tasks=self._get_task_dictionary(), work_dir=args.workdir, output_path=out_path,
                               cache_path=cache_path)
        wf.run(tasks_to_execute=tasks)

    def _get_task_dictionary(self):
        return {k.name: k for k in self.tasks}

    def _load_config(self, path):
        with open(path, 'r') as yml_file:
            cfg = yaml.load(yml_file)

        return cfg
