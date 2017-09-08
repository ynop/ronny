import os
import logging
import time

import yaml


class Task(object):
    name = "undefined"

    def __init__(self, execution_index, config, identifier=None, output_path=None, cache_path=None):
        self.execution_index = execution_index

        if identifier is None:
            self.identifier = str(execution_index)
        else:
            self.identifier = str(identifier)

        self.cfg = config
        self.output_path = output_path
        self.cache_path = cache_path

        self._start_time = None
        self._end_time = None

    def start(self):
        self._setup_logging()

        self._log_start()
        self._start_time = time.time()

        self.run()

        self._end_time = time.time()
        self._log_end()

    def run(self):
        pass

    #
    #   PATH ACCESS
    #

    def output(self, path_components):
        return self._abs(path_components, self.output_path)

    def cache(self, path_components):
        return self._abs(path_components, self.cache_path)

    def _abs(self, path_components, base_path):
        if base_path is None:
            return

        if type(path_components) != list:
            path_components = [path_components]

        path_components.insert(0, base_path)

        return os.path.abspath(os.path.join(*path_components))

    #
    #   CONFIG ACCESS
    #

    def cfg_output(self, key_path):
        return self.output(self.cfg_entry(key_path))

    def cfg_cache(self, key_path):
        return self.cache(self.cfg_entry(key_path))

    def cfg_entry(self, key_path):
        if type(key_path) != list:
            key_path = [key_path]

        entry = self.cfg

        for key in key_path:
            entry = entry[key]

        return entry

    #
    #   HELPER
    #

    def _log_start(self):
        logging.info('#' * 50)
        logging.info('# {}: {} ({}) starting ...'.format(self.execution_index, self.identifier, self.name))
        logging.info('#')
        logging.info('# Output: {}'.format(self.output_path))
        logging.info('# Cache: {}'.format(self.cache_path))
        logging.info('#')
        logging.info('# Config:')

        for line in yaml.dump(self.cfg, default_flow_style=False).split('\n'):
            logging.info("#  {}".format(line))

        logging.info('#' * 50)

    def _log_end(self):
        logging.info('#' * 50)
        logging.info('# {}: {} ({}) finished ...'.format(self.execution_index, self.identifier, self.name))
        logging.info('#')
        logging.info('# Duration: {} s'.format(self._end_time - self._start_time))
        logging.info('#' * 50)

    def _setup_logging(self):
        logging.getLogger().handlers = []
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(message)s',
                            datefmt='%Y/%m/%d %H:%M:%S')

        log_path = self.output("log.txt")

        if log_path is not None:
            if os.path.isfile(log_path):
                os.remove(log_path)

            fh = logging.FileHandler(log_path)
            fh.setFormatter(logging.Formatter(fmt='%(asctime)s %(message)s', datefmt='%Y/%m/%d %H:%M:%S'))
            logging.getLogger().addHandler(fh)
