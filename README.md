
![logo](https://github.com/zhang123cnn/convopilot/blob/main/logo.jpg?raw=true)


# ConvoPilot


## Getting started (auto)

Run the automatic setup script:
`./run.sh`

## Getting started (Mac)
1. make sure you have installed homebrew and python3
1. brew install ffmpeg
1. brew install portaudio
    1. If you homebrew is installed in a non-system directory and you are getting error on portaudio.h and clang, make sure you export the c include path and library path as follows
        1. export C_INCLUDE_PATH=$C_INCLUDE_PATH:[Your local homebrew path]/homebrew/include
        1. export LIBRARY_PATH=$LIBRARY_PATH:[Your local homebrew path]/homebrew/lib
1. pip install convopilot
1. convopilot

## Usage
### Using GPT-4
1. export OPENAI_API_KEY=[PUT YOUR API KEY HERE]
1. convopilot -m gpt-4 -p "Your prompt"

### Write transcription data into a specific file
1. convopilot -o path_to_file 
