#!/bin/bash

homebrew_path=$(brew --prefix)

if [ -z "$homebrew_path" ]; then
    echo "Homebrew is not installed or not found."
    exit 1
fi


if ! command -v brew &>/dev/null; then
    echo "Homebrew is not installed. Please make sure to install it."
    exit 1
fi



include_path="$homebrew_path/include"
lib_path="$homebrew_path/lib"

default_shell="$SHELL"
shell_basename="$(basename "$default_shell")"

echo "Shell is $shell_basename"

case "$shell_basename" in
    "bash")
        profile_file="$HOME/.bashrc"
        ;;
    "zsh")
        profile_file="$HOME/.zshrc"
        ;;
    "fish")
        profile_file="$HOME/.config/fish/config.fish"
        ;;
    *)
        echo "Unsupported shell: $shell_basename"
        exit 1
        ;;
esac

did_change_shell=false

if ! grep -q "export C_INCLUDE_PATH=\"\$C_INCLUDE_PATH:$include_path\"" "$profile_file"; then
    echo "export C_INCLUDE_PATH=\"\$C_INCLUDE_PATH:$include_path\"" >> "$profile_file"

    echo "C_INCLUDE_PATH has been updated in $profile_file."
    did_change_shell=true
else
    echo "C_INCLUDE_PATH entry already exists in $profile_file. No changes made."
fi

if ! grep -q "export LIBRARY_PATH=\"\$LIBRARY_PATH:$lib_path\"" "$profile_file"; then
    echo "export LIBRARY_PATH=\"\$LIBRARY_PATH:$lib_path\"" >> "$profile_file"

    echo "LIBRARY_PATH has been updated in $profile_file."
    did_change_shell=true
else
    echo "LIBRARY_PATH entry already exists in $profile_file. No changes made."
fi

if $did_change_shell; then
    echo "⚠️ ⚠️ Shell configuration has been updated. Please reload your shell using "source" command. Then run the run.sh script again to continue."
    exit 1
fi

if ! command -v ffmpeg &>/dev/null; then
    echo "ffmpeg is not installed. Installing..."
    brew install ffmpeg
    echo "ffmpeg is now installed!"
fi

echo "Installing portaudio.."

brew install portaudio

echo "Installing convopilot.."
pip install convopilot

echo "Installation is done! Now running convopilot.."


convopilot

