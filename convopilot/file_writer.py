import os

class FileWriter:
    def __init__(self, output_dir):
        self.output_dir = output_dir

    def write(self, filename, data, mode='w'):
        try:
            full_path = os.path.join(self.output_dir, filename)
            with open(full_path, mode) as file:
                file.write(data)
            print(f"Data has been written to {full_path} using mode '{mode}'.")
        except Exception as e:
            print(f"An error occurred: {e}")

