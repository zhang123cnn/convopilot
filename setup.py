from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='convopilot',
    version='0.2.1',
    packages=find_packages(include=['convopilot']),
    license="MIT",
    author="Xiaomeng Zhang",
    author_email="zhang123cnn@gmail.com",
    description="An AI tool to help users better navigate conversations.",
    install_requires=requirements,
    url='https://github.com/zhang123cnn/convopilot',
    readme='README.md',
    entry_points={
        'console_scripts': [
            'convopilot=convopilot.record_audio:cli',
            'convopilot-server=convopilot.server:main'
        ]
    },
)
