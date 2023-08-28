import click
import git
import yaml

import sys
import os
import subprocess
import platform
import pathlib
import datetime
import shutil

from pip._internal.operations.freeze import freeze

from pycodelab.templates import LAB_CONFIG_TEMPLATE, DATA_TEMPLATE
from pycodelab.dataloaders import DATALOADERS


@click.group()
def main():
    pass


@main.command()
def init():
    if os.path.exists('.pcl'):
        click.echo('Already in a PyCodeLab directory!')
    else:
        os.mkdir('.pcl')

        with open('.pcl/config.yaml', 'w') as init_confit:
            init_confit.write(LAB_CONFIG_TEMPLATE)
        
        if platform.system() == 'Windows':
            subprocess.run(['notepad', '.pcl/config.yaml'])
        else:
            subprocess.run(['nano', '.pcl/config.yaml'])

        try:
            repo = git.Repo(".")
        except git.exc.InvalidGitRepositoryError:
            click.echo('No repository found. Intializing new git repo.')
            repo = git.Repo.init()

        click.echo(f'Succesfully initialized new lab in {os.getcwd()}')


@main.group()
def exp():
    pass


@exp.command('run')
@click.option('--no_cache', is_flag=True)
@click.option('--no_backup', is_flag=True)
def exp_run(no_cache, no_backup):
    if os.path.exists('.pcl'):
        with open('.pcl/config.yaml', 'r') as  config_file:
            try:
                config = yaml.safe_load(config_file)
            except yaml.YAMLError as exc:
                click.echo(f'Couldn\'t read lab config becasue of: {exc}')
                exit()

        workspace_path = pathlib.Path(config['workspace_path'])
        data_path = pathlib.Path(config['data_path'])
        experiments_path = pathlib.Path(config['experiments_path'])

        repo = git.Repo('.')
            
        repo_info = {
            'branch': repo.active_branch.name,
            'commit': repo.active_branch.commit.hexsha
        }

        # if repo.is_dirty() | len(repo.untracked_files) > 0:
        #     raise Exception('Main repo has unstaged, uncommited or untracked changes. Commit them before running experiment.')

        with open(workspace_path / 'config.yaml', 'r') as  config_file:
            try:
                experiment_config = yaml.safe_load(config_file)
            except yaml.YAMLError as exc:
                click.echo(f'Couldn\'t read experiment config becasue of: {exc}')
                exit()

        data_name = experiment_config['data'].replace('.yaml','')
        if not os.path.exists(data_path / f'{data_name}.yaml'):
            click.echo(f'Data {data_name} doesn\'t exists.')
            exit()

        with open(data_path / f'{data_name}.yaml', 'r') as  config_file:
            try:
                data_config = yaml.safe_load(config_file)
            except yaml.YAMLError as exc:
                click.echo(f'Couldn\'t read experiment config becasue of: {exc}')
                exit()

        dataloader = DATALOADERS.get(data_config['type'])

        if dataloader:
            dataset = dataloader(data_name, data_config, not no_cache)

            sys.path.append('.')

            module_name = (str(workspace_path).replace(os.path.sep,'.')+'.run').replace('..', '')
            experiment_module = __import__(module_name, fromlist=['main'])
            
            os.chdir(workspace_path)
            experiment_function = getattr(experiment_module, 'main')

            try:
                experiment_function(dataset, experiment_config.get('params'))
            except Exception as exc:
                click.echo(f'During experiment, an exception was found: {exc}')
                exit()

            os.chdir('..')

            if not no_backup:

                experiment_time = datetime.datetime.now()
                experiment_name = experiment_time.strftime('%Y%m%d%H%M%S')
                
                os.makedirs(experiments_path / experiment_name)

                with open(experiments_path / experiment_name / 'repo_info.yaml', 'w') as repo_file:
                    yaml.dump(repo_info, repo_file)

                env_config = {
                    'python_version': platform.python_version(),
                    'pip_list': [requirement for requirement in freeze(local_only=True)]
                }

                with open(experiments_path / experiment_name / 'env.yaml', 'w') as env_file:
                    yaml.dump(env_config, env_file)

                shutil.copytree(workspace_path, experiments_path / experiment_name, dirs_exist_ok=True)

                repo.git.add(experiments_path / experiment_name)
                repo.git.commit(message=f'[EXPERIMENT] {experiment_name}')

        else:
            click.echo('Data type not supported')
    else:
        click.echo('Not in a PyCodeLab directory!')


@main.group()
def data():
    pass

@data.command('add')
@click.argument('name')
def data_add(name):
    if os.path.exists('.pcl'):
        with open('.pcl/config.yaml', 'r') as  config_file:
            try:
                config = yaml.safe_load(config_file)
            except yaml.YAMLError as exc:
                click.echo(f'Couldn\'t read lab config becasue of: {exc}')
                exit()

        data_path = pathlib.Path(config['data_path'])

        name = name.replace('.yaml', '').replace('.yml', '').strip().replace(' ', '_')

        if not os.path.exists(data_path):
            os.makedirs(data_path)
        else:
            if os.path.exists(data_path / f'{name}.yaml'):
                click.echo('Data already exists in this lab')
                exit()
        
        with open(data_path / f'{name}.yaml', 'w') as data_file:
            data_file.write(DATA_TEMPLATE)

        if platform.system() == 'Windows':
            subprocess.run(['notepad', data_path / f'{name}.yaml'])
        else:
            subprocess.run(['nano', data_path / f'{name}.yaml'])
    else:
        click.echo('Not in a PyCodeLab directory!')


if __name__ == '__main__':
    main()