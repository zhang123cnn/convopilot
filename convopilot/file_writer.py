import datetime
import os


class FileWriter:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def write(self, file_name, content):
        file_path = os.path.join(self.output_dir, file_name)

        # check if file already exists, then add datetime into the filename to avoid duplication
        if os.path.exists(file_path):
            file_name, file_ext = os.path.splitext(file_name)
            now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            file_name = f"{file_name}_{now}{file_ext}"
            file_path = os.path.join(self.output_dir, file_name)

        with open(file_path, "a") as f:
            f.write(content)