if [ -d ./venv ]; then
    echo "Removing old venv from python directory.."
    rm -r ./venv
fi
echo "Creating new venv in python directory..."
virtualenv venv && source ./venv/bin/activate && LIBRARY_PATH=$LIBRARY_PATH:./convopilot/bin/portaudio/lib C_INCLUDE_PATH=$C_INCLUDE_PATH:./convopilot/bin/portaudio/include pip install .
echo "Created new venv in python directory!"
