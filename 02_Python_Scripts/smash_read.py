# First script to read and display contents of a SMASH file
import struct


def read_smash_file(file_path):
    with open(file_path, 'rb') as f:
        # Read the header (assuming 16 bytes for this example)
        header = f.read(16)
        print("Header:", header)

        # Read the rest of the file in chunks of 32 bytes
        while True:
            chunk = f.read(32)
            if not chunk:
                break
            print("Chunk:", chunk)

