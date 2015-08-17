# setup.py

from setuptools import setup

setup(
    name='MyApp',
    version="1.0",
    packages=['myapp', "myexts", "mymodule"],
    zip_safe=False,
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'myapp = myapp.cli:cli',
        ]
    },
    install_requires=[
        'Flask>=0.10',
        'Flask-AppFactory[celery]',
        'Flask-SQLAlchemy',
    ],
)
