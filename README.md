# ronny

Simple declartive workflow management with python.


## Usage

### Define Tasks

First we have to define some tasks, which can be used within a workflow. 
A task at least has to implement the run method and define a name.
The name is used to reference the task from the workflow config later.

```python  
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
```

### Define main script
Next we have to write our main script which will be the file we execute when we want to run a workflow.
Here we have to define a Runner, which holds a list with all available Task classes.
When the file is executed as main file the run method of the Runner is called.

```python
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
```

### Workflow definition
Now we are ready to define some workflows. A workflow is defined in a YAML file. 
We can define a list of tasks which are executed in order. 
We define a task by giving a identifier and a name which corresponds to the task classes we defined earlier.
All other entries are part of the task config which can be used by the task class via the cfg attribute.

```yaml
tasks:

#########################
- identifier: 0
  name: train

  record_path: <<>>/record.txt

#########################
- identifier: 1
  name: predict

  record_path: <<0>>/record.txt

#########################
- identifier: 2
  name: evaluate

  temp_path: <<<1>>>/temp.txt
```

For example we can retrieve the record_path within the train task like:
```python
file_path = self.cfg['record_path']
```

### Output and Cache folders
A workflow can have an output or/and a cache folder (Defined by run arguments).
The output folder is thought for files that are going to be used later on, while cache folder is used for files that or going to be deleted soon.
If we want to share files/data between tasks, we can use wildcards.

<<X>> : Output folder of task with identifier X.   
<<<X>>> : Cache folder of task with identifier X.

If no identifier is given (<<>>, <<<>>>) the output resp. cache folder of the current folder is meant.

### Running the workflow

```sh
python main.py config_path [--out examples/data] [--cache examples/cache] [--range 1-2]
```

config_path:    Path to the workflow config.   
--out:          Path to the output folder (optional).   
--workdir:      Path to set the working directory (If not set the path where the script is executed is used.).   
--cache:        Path to the cache folder (optional).   
--range:        Run only the given range of tasks (zero based).
