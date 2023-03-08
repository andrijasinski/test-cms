import os
import re
from pathlib import Path

METADATA_FILENAME = "metadata.yml"
ALLOWED_LOCALISATION_DIR_NAMES_REGEX = r"^([a-zA-Z]{2})$|^([a-zA-Z]{2}[-_][a-zA-Z]{2})$"

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
    
  content_directories = list(filter(lambda x: x.is_dir(), content_root_path.iterdir()))
  print(f"Directories in root content dir: {content_directories}")
  
  bad_directories = []
  for directory in content_directories:
    match = re.search(ALLOWED_LOCALISATION_DIR_NAMES_REGEX, directory.name)
    if not match:
      bad_directories.append(str(directory))
    
  if len(bad_directories) > 0:
      with Path(os.getenv("BAD_DIRS_PATH")).open("w") as f:
        f.write(", ".join(bad_directories))
      raise Exception("Not all directory names are following requirements of ISO 639-1 language codes or ISO 639-1 language codes & ISO3166-1 alpha-2 country codes (f.e `en-GB`) ")
  
def mainV2():
  root_dir = Path(os.getenv("GITHUB_WORKSPACE"))
  bad_directories = iterate_directory(root_dir)
  if len(bad_directories) > 0:
    with Path(os.getenv("BAD_DIRS_PATH")).open("w") as f:
      f.write(", ".join(bad_directories))
    raise Exception("Not all directory names are following requirements of ISO 639-1 language codes or ISO 639-1 language codes & ISO3166-1 alpha-2 country codes (f.e `en-GB`) ")
    
def iterate_directory(path):
  bad_dirs = []
  for node in path.iterdir():
    if node.is_dir() and node.name == ".github":
      continue
    elif node.is_dir():
      bad_dirs += check_directory(node)
    elif node.name == METADATA_FILENAME:
      bad_dirs += check_directory_names(node.parent)
  return bad_dirs
      
def check_directory_names(path):
  content_directories = list(filter(lambda x: x.is_dir(), path.iterdir()))
  print(f"Checking directories for names: {content_directories}")
  
  bad_directories = []
  for directory in content_directories:
    match = re.search(ALLOWED_LOCALISATION_DIR_NAMES_REGEX, directory.name)
    if not match:
      bad_directories.append(str(directory))
  return bad_directories
    

  
if __name__ == "__main__":
  mainV2()
