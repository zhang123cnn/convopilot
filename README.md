# ConvoPilot


## Get started (Mac)
1. make sure you have installed homebrew
1. brew install ffmpeg
1. brew install portaudio
1. git clone git@github.com:zhang123cnn/convopilot.git
1. python -m pip install -e .
1. convopilot
1. [Optional] If you homebrew is installed in a non-system directory, make sure you export the c include path and library path as follows
  1. export C_INCLUDE_PATH=$C_INCLUDE_PATH:[Your local homebrew path]/homebrew/include
  1. export LIBRARY_PATH=$LIBRARY_PATH:[Your local homebrew path]/homebrew/lib

## Usage
### Using GPT-4
1. Copy .env.template to .env
1. Put your openai api key in the file
1. convopilot -m gpt-4 -p "Your prompt"

### Write transcription data into a specific file
1. convopilot -o path_to_file 