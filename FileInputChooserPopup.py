from kivy.uix.popup import Popup


class FileInputChooserPopup(Popup):
  """
  ROLE: Give the user the ability to choose what file he wants to align
  """
  
  def __init__(self, caller, **kwargs):
    """
    ROLE: Constructor
    PARAMETERS: caller, AlignSequencesTool (Main widget)
    """
    super(FileInputChooserPopup, self).__init__(**kwargs)

    self.caller = caller
          

  def update_file_path(self):
    """
    ROLE: Change the wanted file path to the selected file path.
          Convert the file path to the name of the file
    OUTT: caller.pathToFileX, string
          caller.fileNameX, string
    """

    if self.caller.fileNumber==1:
      self.caller.pathToFile1 = self.ids.file_chooser.selection[0]
      self.caller.fileName1 = self.caller.pathToFile1.split('/')[-1]

    elif self.caller.fileNumber==2:
      self.caller.pathToFile2 = self.ids.file_chooser.selection[0]
      self.caller.fileName2 = self.caller.pathToFile2.split('/')[-1]

    self.dismiss()
