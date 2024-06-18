# -*- coding: utf-8 -*-

# Import python libraries
from os.path import sep as pathsep
import hashlib

# Import customed objects
from NwPOO import NwPOO
from AlignmentParameters import AlignmentParameters
from FastaFile import FastaFile

# Import kivy widgets
from kivy.uix.boxlayout import BoxLayout

# Import kivy objects
from kivy.properties import StringProperty
from kivy.clock import Clock
from kivy.factory import Factory

# Import customed kivy widgets
from FileInputChooserPopup import FileInputChooserPopup
from Notification import Notification
from RecycleInputPopup import RecycleInputPopup
from ProgressbarPopup import ProgressbarPopup
from RecycleResultsPopup import RecycleResultsPopup

# Import .kv files
from kivy.lang import Builder
Builder.load_file("styles" + pathsep + "custom_style.kv")
Builder.load_file("styles" + pathsep + "AlignSequencesTool.kv")
Builder.load_file("styles" + pathsep + "FileInputChooserPopup.kv")
Builder.load_file("styles" + pathsep + "TutorialPopup.kv")
Builder.load_file("styles" + pathsep + "Notification.kv")
Builder.load_file("styles" + pathsep + "RecycleInputPopup.kv")
Builder.load_file("styles" + pathsep + "ProgressbarPopup.kv")
Builder.load_file("styles" + pathsep + "RecycleResultsPopup.kv")


class AlignSequencesTool(BoxLayout):
  """
  ROLE : Tool main widget 
  """

  # List of the files and results already computed
  lstFiles = []
  lstResults = []

  # Maximum number of results that can be stored while the app is open
  MAX_RESULTS = 5 

  # Path to default files
  pathToFile1 = StringProperty("demo_files" + pathsep + "fichier1.fasta")
  pathToFile2 = StringProperty("demo_files" + pathsep + "fichier2.fasta")


  def open_file_input(self, fileNumber):
    """
    ROLE: Open the file input chooser popup
    PARAMETERS: fileNumber, int (number of the file to select)
    OUTPUT: FileInputChooserPopup()
    """

    self.fileNumber = fileNumber
    FileInputChooserPopup(caller=self).open()


  def show_file_content(self, fileNumber):
    """
    ROLE: Get the fasta file, build and open the RecycleInputPopup
    PARAMETERS: fileNumber, int (number of the file to display)
    OUTPUT: RecycleInputPopup()
            or
            Notification()
    """

    try: 
      # Try to display the content of the file selected. Fails if the file is not in *.fasta format

      # Select the path to the file 1 or 2
      if fileNumber==1:
        pathToFile = self.pathToFile1
      elif fileNumber==2:
        pathToFile = self.pathToFile2

      newFastaFile = FastaFile(pathToFile)

      # Check in lstFiles if the newFastaFile has already been open
      found = None
      for item in self.lstFiles:
        if item.checksum==newFastaFile.checksum:
          found = item

      if found:
        # Replace the newFastaFile by the old one
        newFastaFile.close()
        fastaFile = found

      else:
        # Read the content of the file and store it in lstFiles
        newFastaFile.read_content()
        newFastaFile.close()
        self.lstFiles.append(newFastaFile)
        fastaFile = newFastaFile


        if len(self.lstFiles) > self.MAX_RESULTS*2:
          # Remove the oldest stored file
          self.lstFiles.pop(0)

      RecycleInputPopup(
                        title=fastaFile.title, 
                        data_items=fastaFile.data_items,
                        ).open()
 
    except: 
      # If the file is not readable, display an error popup instead of the file content
      Notification(title="File Error", notificationText="The file you tryed to open is not in .fasta format").open()


  """
  List of functions when the 'Results' button of the GUI is pressed.
  The main goal is to open the Results Popup with the alignment and scores display
  """
  def open_new_results_popup(self):
    """
    ROLE: Dismiss the progressbarPopup
          Build and open the RecycleResultsPopup with checksums and alignment results.
          Add it to lstResults
    OUTPUT: recycleResultsPopup, RecycleResultsPopup
    """

    recycleResultsPopup = RecycleResultsPopup(
                                              checksum1 = self.fastaFile1.checksum,
                                              checksum2 = self.fastaFile2.checksum,
                                              alignment = self.worker.alignment
                                              )
    
    self.lstResults.append(recycleResultsPopup)

    if len(self.lstResults) > self.MAX_RESULTS:
      # Remove the oldest ReycleResultsPopup
      self.lstResults.pop(0)

    self.popupProgressBar.dismiss()
    recycleResultsPopup.open()
  

  def update_bar_alignment(self, dt=None):
    '''
    ROLE: Update the progress bar. 
          If the alignment is completed, call the 'open_new_results_popup' function.
    PARAMETERS: dt, float (Clock parameter)
    '''

    self.popupProgressBar.progressbarValue += 1

    if self.popupProgressBar.progressbarValue >= self.popupProgressBar.progressbarMax:
      self.open_new_results_popup()


  def set_sequences(self, source1, source2):
    """
    ROLE: Check if the file has already been opened.
          If not, read the sequences and store them.
          Build matrixArea variable that will be used in the ProgressBarPopup
    PARAMETERS: source1, FastaFile (selected file 1)
                source2, FastaFile (selected file 2)
    OUTPUT: fastaFile1, FastaFile
            fastaFile2, FastaFile
            matrixArea, int
    """

    # Check in lstFiles if the source1 and source2 files has already been open
    found1 = None
    found2 = None
    for item in self.lstFiles:
      if item.checksum==source1.checksum:
        found1 = item
      if item.checksum==source2.checksum:
        found2 = item

    if found1:
      self.fastaFile1 = found1

    else:
      # Read the file, add it to lstFiles and affect it to fastaFile1
      source1.read_content()
      source1.close()
      self.lstFiles.append(source1)
      self.fastaFile1 = source1

    if found2:
      self.fastaFile2 = found2

    else:
      # Read the file, add it to lstFiles and affect it to fastaFile2
      source2.read_content()
      source2.close()
      self.lstFiles.append(source2)
      self.fastaFile2 = source2
    
    self.matrixArea = len(self.fastaFile1.sequence) * len(self.fastaFile2.sequence)


  def create_alignment_parameter_object(self):
    """
    ROLE: Get the points for a match, mismatchs and gaps set in the UI.
          Create an object containing all the points.
    OUTPUT: AlignementParameters()
    """

    self.ids.input_points_match.text = "2" if self.ids.input_points_match.text=="" else self.ids.input_points_match.text
    self.ids.input_points_missmatch_intra.text = "1" if self.ids.input_points_missmatch_intra.text=="" else self.ids.input_points_missmatch_intra.text
    self.ids.input_points_missmatch_extra.text = "-1" if self.ids.input_points_missmatch_extra.text=="" else self.ids.input_points_missmatch_extra.text
    self.ids.input_points_opening_gap.text = "-10" if self.ids.input_points_opening_gap.text=="" else self.ids.input_points_opening_gap.text
    self.ids.input_points_extensive_gap.text = "-1" if self.ids.input_points_extensive_gap.text=="" else self.ids.input_points_extensive_gap.text

    return AlignmentParameters(
                              float(self.ids.input_points_match.text),
                              float(self.ids.input_points_missmatch_intra.text),
                              float(self.ids.input_points_missmatch_extra.text),
                              float(self.ids.input_points_opening_gap.text),
                              float(self.ids.input_points_extensive_gap.text)
                              )


  def launch_alignment(self):
    """
    ROLE: Align the sequences with the Needleman & Wunch algorithm then call the methods that will open the RecycleResultsPopup
    OUTPUT: NwPOO, Thread
            progressbarPopup, ProgressbarPopup
            or
            Notification()
    """

    parameters = self.create_alignment_parameter_object()   

    try:  
      # Try to display the result of the alignment. Fails if one of the file is not in *.fasta format
      fastaFile1 = FastaFile(self.pathToFile1)
      fastaFile2 = FastaFile(self.pathToFile2)

      # Check in lstResults if the files has already been aligned
      found = None
      for item in self.lstResults:
        if item.compare_checksums(fastaFile1.checksum, fastaFile2.checksum) and item.compare_points(parameters):
          found = item

      if found:
        # Dismiss the progressbarPopup and open the ReycleResultsPopup found in lstResults
        fastaFile1.close()
        fastaFile2.close()
        #self.popupProgressBar.dismiss()
        found.open()

      else:
        # Process the new alignment
        self.set_sequences(fastaFile1, fastaFile2)
        parameters.set_sequences_parameters(self.fastaFile1.title, self.fastaFile2.title, self.fastaFile1.sequence, self.fastaFile2.sequence)
                
        # Instanciate the worker that will run the Needleman and Wunsch algorithm in background        
        self.worker = NwPOO(parameters, lambda: Clock.schedule_once(self.update_bar_alignment))   

        self.popupProgressBar = ProgressbarPopup(title="Processing the alignment", progressbarMax=self.matrixArea + 1)
        self.popupProgressBar.open()

        # Call the 'run' method of the NwPOO class (launch the alignment)
        self.worker.start() 

    except: 
      # If at least one file is not readable, open Notification popup instead of doing the algorithm
      Notification(title="File Error", notificationText="One of your file is not in .fasta format").open()
