if [ -d ./venv ]; then
    echo "Removing old venv from python directory.."
    rm -r ./venv
fi
echo "Creating new venv in python directory..."
virtualenv venv && source ./venv/bin/activate && pip install .
echo "Created new venv in python directory!"
