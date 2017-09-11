import sys
import os
import time
import logging

sys.path.append(os.path.abspath(os.path.join(__file__, os.path.pardir, os.path.pardir)))

import ronny


class TrainTask(ronny.Task):
    name = 'train'

    def run(self):
        logging.info("I am training")

        file_path = self.cfg['record_path']

        with open(file_path, 'w') as f:
            f.write('TRAIN: HUI \n')

        time.sleep(1.5)


class PredictTask(ronny.Task):
    name = 'predict'

    def run(self):
        logging.info("I am predicting")

        record_path = self.cfg['record_path']

        with open(record_path, 'a') as f:
            f.write('PREDICT: YEI \n')

        temp_path = self.cache('temp.txt')

        with open(temp_path, 'w') as f:
            f.write('PREDICT: OOWW \n')

        time.sleep(2)


class EvaluateTask(ronny.Task):
    name = 'evaluate'

    def run(self):
        logging.info("I am evaluating")

        temp_path = self.cfg['temp_path']

        with open(temp_path, 'a') as f:
            f.write('EVAL: HEY \n')

        time.sleep(0.2)


class AnalyzeTask(ronny.Task):
    name = 'analyze'

    def run(self):
        time.sleep(3)
        logging.info("I am analyzing")


class MyRunner(ronny.Runner):
    tasks = [
        TrainTask,
        PredictTask,
        EvaluateTask,
        AnalyzeTask
    ]


if __name__ == '__main__':
    runner = MyRunner()
    runner.run()
