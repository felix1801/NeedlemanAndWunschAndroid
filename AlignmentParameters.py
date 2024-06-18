class AlignmentParameters(object):
  """
  ROLE: Object contain the parameters and results alignment
  """

  def __init__(self, pointsMatch, pointsMissmatchIntra, pointsMissmatchExtra, pointsOpeningGap, pointsExtensiveGap):
    """
    ROLE: Constructor
    PARAMETERS: pointsMatch, float
                pointsMissmatchIntra, float
                pointsMissmatchExtra, float
                pointsOpeningGap, float
                pointsExtensiveGap, float
    """
    self.pointsMatch = pointsMatch
    self.pointsMissmatchIntra = pointsMissmatchIntra
    self.pointsMissmatchExtra = pointsMissmatchExtra
    self.pointsOpeningGap = pointsOpeningGap
    self.pointsExtensiveGap = pointsExtensiveGap


  def set_sequences_parameters(self, titleSeq1, titleSeq2, sequence1, sequence2):
    """
    ROLE: Set the parameters of the sequence
    PARAMETERS: titleSeq1, string
                titleSeq2, string
                sequence1, string
                sequence2, string
    """

    self.titleSeq1 = titleSeq1
    self.titleSeq2 = titleSeq2
    self.sequence1 = sequence1
    self.sequence2 = sequence2
