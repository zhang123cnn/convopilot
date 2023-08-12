from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='convopilot',
    version='0.1.1',
    packages=find_packages(include=['convopilot']),
    license="MIT",
    author="Xiaomeng Zhang",
    author_email="zhang123cnn@gmail.com",
    description="An AI tool to help users better navigate conversations.",
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'convopilot=convopilot.record_audio:cli'
        ]
    },
)
