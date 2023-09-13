from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='convopilot',
    version='0.2.6',
    packages=find_packages(include=['convopilot']),
    package_data={'convopilot': ['bin/ffmpeg',
    'bin/portaudio/lib/libportaudio.2.dylib',
    'bin/portaudio/lib/libportaudio.a',
    'bin/portaudio/lib/libportaudio.dylib',
    'bin/portaudio/lib/libportaudio.la',
    'bin/portaudio/lib/pkgconfig/portaudio-2.0.pc',
    'bin/portaudio/lib/pkgconfig/portaudiocpp.pc',
    'bin/portaudio/lib/libportaudiocpp.0.dylib',
    'bin/portaudio/lib/libportaudiocpp.a',
    'bin/portaudio/lib/libportaudiocpp.dylib']},
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
