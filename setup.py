from setuptools import setup, find_packages

setup(
    name='pycodelab',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'click >= 8.1.7',
        'gitdb >= 4.0.10',
        'GitPython >= 3.1.32',
        'PyYAML >= 6.0.1'
    ],
    entry_points={
        'console_scripts': [
            'pcl = pycodelab.cli:main'
        ]
    },
)