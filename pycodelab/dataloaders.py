import os
import pathlib
import pickle
import sys

import yaml

class CallableDataLoader:

    def __init__(self):
        pass
    
    @staticmethod
    def load(data_name: str, data_info: dict, caching: bool=True) -> any:

        if not os.path.exists('.pcl'):
            print('Not in a PyCodeLab directory!')
        else:
            with open('.pcl/config.yaml', 'r') as  config_file:
                try:
                    config = yaml.safe_load(config_file)
                except yaml.YAMLError as exc:
                    print(f'Couldn\'t read lab config becasue of: {exc}')
                    exit()

        data_path = pathlib.Path(config['data_path'])
        if caching:
            if os.path.exists(data_path / 'cache' / f'{data_name}.pyc'):
                print('Found cache data. Loading it')
                with open(data_path / 'cache' / f'{data_name}.pyc', 'rb') as cache:
                    try:

                        return pickle.load(cache)
                    
                    except Exception as exc:
                        print(f'Couldn\'t load cache because {exc}. Executing dataloader')

        function_name = data_info['dataloader']
        function_params = data_info['params']

        function_path = function_name.split('.')
        sys.path.append('.')
        module = __import__('.'.join(function_path[:-1]), fromlist=[function_path[-1]])
        function = getattr(module, function_path[-1])

        dataset = function(**function_params)

        if caching:
            os.makedirs(data_path / 'cache', exist_ok=True)
            with open(data_path / 'cache' / f'{data_name}.pyc', 'wb') as cache:
                    try:
                        pickle.dump(dataset, cache)
                    except Exception as exc:
                        print(f'Couldn\'t create cache because of {exc}')

        return dataset

DATALOADERS = {
    'callable': CallableDataLoader.load
}