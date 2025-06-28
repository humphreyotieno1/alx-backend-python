from setuptools import setup, find_packages

setup(
    name="messaging_app",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'Django>=4.0',
        # Add other dependencies from requirements.txt
    ],
)
