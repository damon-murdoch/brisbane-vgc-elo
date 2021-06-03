# JSON object parsing library
import json

# read_json(filename: str): object
def read_json(filename):

  try:

    # Attempt to open the filename
    with open(filename, 'r') as file:

      # Read the content from the file
      content = file.read()

      # If the string is not empty
      if content != "":

        # Load the content from the file
        return json.loads(content)

      else: # String is empty

        # Return 0 (no result)
        return 0

  except:

    # Return -1 (failure)
    return -1

# write_json(filename: str, content: object): void
def write_json(filename, content):

  try:

    # Attempt to open the filename
    with open(filename, 'w+') as file:

      # Write the content to the file
      file.write(json.dumps(content))

  except:

    # Return -1 (failure)
    return -1

# merge_json(object: hashtable, file: string): void
# Given a Python object and a filename, merge the 
# given file with the object (or creates the file
# if it does not exist) and writes the changes
# back to the file.
def merge_json(object, file):

  # Get the Json content from the file
  content = read_json(file)

  # If an error code is returned
  if content is int:

    # Content is an empty object
    content = {}

  # Merge the content from the file with the new content
  content.merge(object)

  # Write the merged content to the file
  write_json(file, content)

if __name__ == '__main__':

  out = { 
    'firstname': 'Damon', 
    'lastname': 'Murdoch',
    'age': 23,
  }

  print(out)

  write_json("out.json", out)

  inp = read_json("out.json")

  print(inp)