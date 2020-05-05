from setuptools import setup
setup(
    name='app',
    version='0.0.1',
    entry_points={
        'console_scripts': [
            'app=app:run'
        ]
    }
)