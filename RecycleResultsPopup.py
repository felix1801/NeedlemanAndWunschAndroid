from kivy.uix.popup import Popup
from kivy.properties import ListProperty

from Notification import Notification

from kivy.utils import platform
import os

class RecycleResultsPopup(Popup):
  """
  ROLE: Build the popup object that will display the results of the alignment
  """

  def __init__(self, checksum1, checksum2, alignment, **kwargs):
    """
    ROLE: Constructor
    PARAMETERS: checksum1, string
                checksum2, string
                alignment, Alignment
    """

    self._checksum1 = checksum1
    self._checksum2 = checksum2
    self.alignment = alignment

    super(RecycleResultsPopup, self).__init__(**kwargs)


  def compare_checksums(self, checksum1, checksum2):
    """
    ROLE: Compare the checksums of this popup with the one passed in parameters
    PARAMETERS: checksum1, string
                checksum2, string
    OUTPUTS: True if checksums are the same
             False if they are different
    """

    if (self._checksum1 == checksum1 and self._checksum2==checksum2) \
    or (self._checksum2 == checksum1 and self._checksum1==checksum2):
      return True
    
    else:
      return False


  def compare_points(self, parameters):
    """
    ROLE: Compare points of this popup with the one of the AlignmentParameters object passed in parameters
    PARAMETERS: parameters, AlignmentParameters
    OUTPUTS: True if points are the same
             False if they are different
    """

    if self.alignment.parameters.pointsMatch==parameters.pointsMatch \
    and self.alignment.parameters.pointsMissmatchIntra==parameters.pointsMissmatchIntra \
    and self.alignment.parameters.pointsMissmatchExtra==parameters.pointsMissmatchExtra \
    and self.alignment.parameters.pointsOpeningGap==parameters.pointsOpeningGap \
    and self.alignment.parameters.pointsExtensiveGap==parameters.pointsExtensiveGap:
        return True
    
    else:
        return False


  def save_results(self):
    """
    ROLE: Write the results of the alignment in a text file
    OUTPUTS: seq1__vs__seq2.txt, file
    """

    path = "/storage/emulated/0/dna_results" if platform=='android' else os.environ['HOME'] + os.path.sep + "dna_results"
    
    if not os.path.exists(path):
      os.makedirs(path)

    if (not os.path.exists(path + os.path.sep + self.alignment.parameters.titleSeq1 + '__vs__' + self.alignment.parameters.titleSeq2 + '.txt')) \
    and (not os.path.exists(path + os.path.sep + self.alignment.parameters.titleSeq2 + '__vs__' + self.alignment.parameters.titleSeq1 + '.txt')):
      # If file doesn't exist, write it
      with open(path + os.path.sep + self.alignment.parameters.titleSeq1 + '__vs__' + self.alignment.parameters.titleSeq2 + '.txt', 'w') as file:

        # Write the name of the sequences
        file.write("Upper sequence title: " + self.alignment.parameters.titleSeq1 + os.linesep)
        file.write("Lower sequence title: " + self.alignment.parameters.titleSeq2 + os.linesep)
        file.write(os.linesep)

        # Add the nucleotides to display to the data object
        data_items = ''.join(self.alignment.data_items)        
        for i in range(0, len(data_items), 60):
          file.write(data_items[i:i+60] + os.linesep)

        # Write the scores and count of score, gaps, matchs and mismatchs
        file.write("Total score: " + str(self.alignment.scoreAlignment) + os.linesep)
        file.write("Number of gaps: " + str(self.alignment.nbGap) + os.linesep)
        file.write("Number of matchs: " + str(self.alignment.nbMatch) + os.linesep)
        file.write("Number of missmatchs: " + str(self.alignment.nbMissmatch) + os.linesep)
        file.write("\tincluding " + str(self.alignment.nbMissmatchIntra) + " Intra bases" + os.linesep)
        file.write("\tincluding : " + str(self.alignment.nbMissmatchExtra) + " Extra bases" + os.linesep)

      Notification(title="Success", notificationText="Results successfully saved in " + path).open()

    else:
      # If the results has already been saved, open Notification popup
      Notification(title="Already saved", notificationText="Results has already been saved in " + path).open()
