import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(__file__, os.path.pardir, os.path.pardir)))

import ronny


class TrainTask(ronny.Task):
    name = 'train'

    def run(self):
        time.sleep(1.5)
        print("I am training")


class PredictTask(ronny.Task):
    name = 'predict'

    def run(self):
        time.sleep(2)
        print("I am predicting")


class EvaluateTask(ronny.Task):
    name = 'evaluate'

    def run(self):
        time.sleep(0.2)
        print("I am evaluating")


class AnalyzeTask(ronny.Task):
    name = 'analyze'

    def run(self):
        time.sleep(3)
        print("I am analyzing")


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
