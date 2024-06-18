class Alignment(object):
  """
  ROLE: Object containing the parameters and results alignment
  """

  def __init__(
              self, 
              parameters, 
              alignmentSeq1, 
              alignmentQuali, 
              alignmentSeq2, 
              scoreAlignment, 
              nbMatch, 
              nbGap, 
              nbMissmatch, 
              nbMissmatchIntra, 
              nbMissmatchExtra
              ):
    """
    ROLE: Constructor
    PARAMETERS: parameters, Parameters
                alignmentSeq1, string
                alignmentQuali, string
                alignmentSeq2, string
                scoreAlignment, float
                nbMatch, int
                nbGap, int
                nbMissmatch, int
                nbMissmatchIntra, int
                nbMissmatchExtra, int
    """

    self.parameters = parameters

    self.alignmentSeq1 = alignmentSeq1
    self.alignmentQuali = alignmentQuali
    self.alignmentSeq2 = alignmentSeq2

    self.scoreAlignment = scoreAlignment
    self.nbMatch = nbMatch
    self.nbGap = nbGap
    self.nbMissmatch = nbMissmatch
    self.nbMissmatchIntra = nbMissmatchIntra
    self.nbMissmatchExtra = nbMissmatchExtra

    self.format_alignment()


  def format_alignment(self):
    """
    ROLE: Insert every nucleotide one by one into the data_items variable that will be used to display the result of the alignement
    OUTPUT: data_items, list (used to display the result of the alignment in RecycleResultsPopup)
    """

    self.data_items = []

    nbMissingCells = 60 - (len(self.alignmentQuali)%60)

    for i in range(nbMissingCells):
      self.alignmentSeq1 += " "
      self.alignmentQuali += " "
      self.alignmentSeq2 += " "

    for i in range(0, len(self.alignmentQuali), 60):
      [self.data_items.append(nuc) for nuc in self.alignmentSeq1[i:i+60]]
      [self.data_items.append(nuc) for nuc in self.alignmentQuali[i:i+60]]
      [self.data_items.append(nuc) for nuc in self.alignmentSeq2[i:i+60]]
      [self.data_items.append(' ') for blank in range(60)]
