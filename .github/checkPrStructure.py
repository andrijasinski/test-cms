import os
from pathlib import Path

METADATA_FILENAME = "metadata.yml"

def main():
  changed_files = os.getenv("CHANGED_FILES").split(",")
  print(f"Changed files are: {changed_files}")
  
  paths = map(lambda x: Path(x), changed_files)
  metadata_path = list(filter(lambda x: x.name == METADATA_FILENAME, paths))
  if len(metadata_path) == 0:
    print(f"No {METADATA_FILENAME} is found, exiting")
    exit 1
    
  print(paths)
  print(metadata_path)
  
  

if __name__ == "__main__":
  main()
