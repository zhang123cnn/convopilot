class FileWriter:
    def write(self, filename, data, mode='w'):
        try:
            with open(filename, mode) as file:
                file.write(data)
            print(f"Data has been written to {filename} using mode '{mode}'.")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    try:
        writer = FileWriter()
        filename = "transcription.txt"
        transcription_data = "This is some transcription data."

        writer.write(filename, transcription_data)
    except Exception as e:
        print(f"An error occurred: {e}")