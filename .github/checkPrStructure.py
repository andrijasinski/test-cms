import main from checkPrStructureMain
import os 

if __name__ == "__main__":
  try:
    main()
  except:
    with open("bad_dirs.txt", "r") as f:
      os.environ["GITHUB_OUTPUT"] = f.readlines()
    raise
    
