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
    
  content_root_path = None
  if len(metadata_paths) > 1:
    content_root_path = min(list(map(lambda x: x.parent, metadata_paths)))
  else:
    content_root_path = metadata_paths[0].parent
    
  print(f"Files in that dir: {list(content_root_path.iterdir())}")
    
  
  

if __name__ == "__main__":
  main()
