import hashlib
from os import linesep

class FastaFile(object):
  """
  ROLE: Contain file parameters. Needs to be closed.
  """

  def __init__(self, path):
    """
    ROLE: Constructor
    PARAMETERS: path, string
    OUTPUT: file, io.BufferedReader
            binaryContent, bytes
            checksum, string
    """

    self.path = path
    self.file = open(self.path, 'rb')
    self.binaryContent = self.file.read()
    self.checksum = hashlib.md5(self.binaryContent).hexdigest()


  def read_content(self):
    """
    ROLE: Convert binaryContent to textContent.
          Format the sequence to an item usable in RecycleView
    OUTPUT: title, string
            sequence, string
            data_items, list (used to display the content of the file in RecycleInputPopup)
    """

    self.textContent = self.binaryContent.decode('utf-8')
    self.lines = self.textContent.split(linesep)
    if self.lines[-1]=='':
      self.lines.pop(-1)

    self.title = self.lines[0]
    self.sequence = ''

    for line in self.lines[1::]:
      self.sequence += line.strip()

    self.data_items = list(self.sequence)


  def close(self):
    """
    ROLE: Close the file
    """
    
    self.file.close()
