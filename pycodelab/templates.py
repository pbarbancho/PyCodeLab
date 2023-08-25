LAB_CONFIG_TEMPLATE = """workspace_path: workspace
experiments_path: experiments
data_path: data
models_path: models"""

DATA_TEMPLATE = """type: # callable, url, directory, file
src: # data location, if not callable
dataloader: # function to load data, if needed
params:
    # params to pass to dataloader
"""