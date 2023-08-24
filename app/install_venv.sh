if [ -d ./release/app/venv ]; then
    echo "Removing old venv.."
    rm -r ./release/app/venv
fi

echo "Installing venv.."

cp -r ../venv ./release/app/venv

echo "Successfully installed venv to ./release/app"
