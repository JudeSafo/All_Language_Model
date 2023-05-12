import optuna
import subprocess
import json
import logging

# Get the root logger.
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Create a handler that outputs log messages to stdout.
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)

# Create a formatter that specifies the layout of the log messages.
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Add the formatter to the handler.
handler.setFormatter(formatter)

# Add the handler to the logger.
logger.addHandler(handler)

def objective(trial):
    learning_rate = trial.suggest_float('learning_rate', 1e-5, 1e-4, log=True)
    num_train_epochs = trial.suggest_int('num_train_epochs', 3, 30)
    per_device_train_batch_size = trial.suggest_categorical('per_device_train_batch_size', [8, 16, 32])
    per_device_eval_batch_size = trial.suggest_categorical('per_device_eval_batch_size', [64, 128])
    warmup_steps = trial.suggest_int('warmup_steps', 500, 1000)
    weight_decay = trial.suggest_float('weight_decay', 0.01, 0.03)

    # call your train.py script with these hyperparameters
    process = subprocess.Popen(['python', 'train.py', 
                                '--learning_rate', str(learning_rate), 
                                '--num_train_epochs', str(num_train_epochs),
                                '--per_device_train_batch_size', str(per_device_train_batch_size),
                                '--per_device_eval_batch_size', str(per_device_eval_batch_size),
                                '--warmup_steps', str(warmup_steps),
                                '--weight_decay', str(weight_decay)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    # print the output in real time
    for line in iter(process.stdout.readline, b''):
        print(line.decode().strip())

    process.stdout.close()
    return_code = process.wait()

    # Check if the subprocess has finished successfully
    if return_code != 0:
        raise RuntimeError(f"Subprocess finished with return code {return_code}")

    # Load the evaluation metrics from a file
    # You need to modify your train.py script to write the evaluation metrics to a file
    with open('evaluation_metrics.json', 'r') as f:
        result_dict = json.load(f)

    return result_dict['eval_loss']

study = optuna.create_study(direction='minimize')
study.optimize(objective, n_trials=100)
