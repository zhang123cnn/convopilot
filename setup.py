from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="convopilot",
    version="0.2.7",
    packages=find_packages(include=["convopilot"]),
    package_data={
        "convopilot": [
            "bin/ffmpeg",
            "bin/portaudio/lib/libportaudio.2.dylib",
            "bin/portaudio/lib/libportaudio.a",
            "bin/portaudio/lib/libportaudio.dylib",
            "bin/portaudio/lib/libportaudio.la",
            "bin/portaudio/lib/pkgconfig/portaudio-2.0.pc",
            "bin/portaudio/lib/pkgconfig/portaudiocpp.pc",
            "bin/portaudio/lib/libportaudiocpp.0.dylib",
            "bin/portaudio/lib/libportaudiocpp.a",
            "bin/portaudio/lib/libportaudiocpp.dylib",
            "bin/portaudio/include/portaudiocpp/AutoSystem.hxx",
            "bin/portaudio/include/portaudiocpp/BlockingStream.hxx",
            "bin/portaudio/include/portaudiocpp/CFunCallbackStream.hxx",
            "bin/portaudio/include/portaudiocpp/CallbackInterface.hxx",
            "bin/portaudio/include/portaudiocpp/CallbackStream.hxx",
            "bin/portaudio/include/portaudiocpp/CppFunCallbackStream.hxx",
            "bin/portaudio/include/portaudiocpp/Device.hxx",
            "bin/portaudio/include/portaudiocpp/DirectionSpecificStreamParameters.hxx",
            "bin/portaudio/include/portaudiocpp/Exception.hxx",
            "bin/portaudio/include/portaudiocpp/HostApi.hxx",
            "bin/portaudio/include/portaudiocpp/InterfaceCallbackStream.hxx",
            "bin/portaudio/include/portaudiocpp/MemFunCallbackStream.hxx",
            "bin/portaudio/include/portaudiocpp/PortAudioCpp.hxx",
            "bin/portaudio/include/portaudiocpp/SampleDataFormat.hxx",
            "bin/portaudio/include/portaudiocpp/Stream.hxx",
            "bin/portaudio/include/portaudiocpp/StreamParameters.hxx",
            "bin/portaudio/include/portaudiocpp/System.hxx",
            "bin/portaudio/include/portaudiocpp/SystemDeviceIterator.hxx",
            "bin/portaudio/include/portaudiocpp/SystemHostApiIterator.hxx",
            "bin/portaudio/include/portaudio.h",
            "bin/portaudio/include/pa_mac_core.h",
        ]
    },
    license="MIT",
    author="Xiaomeng Zhang",
    author_email="zhang123cnn@gmail.com",
    description="An AI tool to help users better navigate conversations.",
    install_requires=requirements,
    url="https://github.com/zhang123cnn/convopilot",
    readme="README.md",
    entry_points={
        "console_scripts": [
            "convopilot=convopilot.record_audio:cli",
            "convopilot-server=convopilot.server:main",
        ]
    },
)
