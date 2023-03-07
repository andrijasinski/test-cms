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
  
#   matches = list(map(lambda x: re.search(ALLOWED_LOCALISATION_DIR_NAMES_REGEX, x.name), content_directories))
  bad_directories = []
  for directory in content_directories:
    match = re.search(ALLOWED_LOCALISATION_DIR_NAMES_REGEX, directory.name)
    if not match:
      bad_directories.append(str(directory))
    
  if len(bad_directories) > 0:
      print(f"bad dirs path {Path(".") / "bad_dirs.txt"}")
      with (Path(".") / "bad_dirs.txt").open("w") as f:
        f.write(", ".join(bad_directories))

#       with open(os.path.join(os.getcwd(), 'bad_dirs.txt'), 'w') as f:
#         f.write(", ".join(bad_directories))
      raise Exception("Not all directory names are following requirements of ISO 639-1 language codes or ISO 639-1 language codes & ISO3166-1 alpha-2 country codes (f.e `en-GB`) ")
  

if __name__ == "__main__":
  main()
#   try:
#     main()
#   except:
#     with open("bad_dirs.txt", "r") as f:
#       dirs = str(f.read())
#       print(dirs)
#       os.environ["GITHUB_ENV"] = f"{os.environ["GITHUB_ENV"]},bad_dirs={dirs}"
#     raise

