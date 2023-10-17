
![logo](https://github.com/zhang123cnn/convopilot/blob/main/logo.jpg?raw=true)


# ConvoPilot


## Getting started (auto)

### Installation

- `brew install portaudio`
- `brew install ffmpeg`
- `cd app`
- `npm run dist`
  
You should find macOS binaries in /app/release/build

- Run ConvoPilot.app

## Usage
### Using GPT-4
1. export OPENAI_API_KEY=[PUT YOUR API KEY HERE]
1. convopilot -m gpt-4 -p "Your prompt"

### Write transcription data into a specific file
1. convopilot -o path_to_file 
