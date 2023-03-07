import os
from pathlib import Path

METADATA_FILENAME = "metadata.yml"

def main():
  changed_files = os.getenv("CHANGED_FILES").split(",")
  print(f"Changed files are: {changed_files}")
  
  paths = list(map(lambda x: Path(x), changed_files))
  metadata_paths = list(filter(lambda x: x.name == METADATA_FILENAME, paths))
  
  print(f"Paths: {paths}")
  print(f"Metadata paths: {metadata_paths}")
  
  if len(metadata_paths) == 0:
    raise Exception(f"The {METADATA_FILENAME} is not found, exiting. The branch should have at least one {METADATA_FILENAME} file in the content root folder.")
    
  metadata_path = None
  if len(metadata_paths) > 1:
    metadata_path = min(list(map(lambda x: x.parent, metadata_paths)))
  else:
    metadata_path = metadata_paths[0]
    
  print(f"Files in that dir: {list(metadata_path.iterdir())}")
    
  
  

if __name__ == "__main__":
  main()
