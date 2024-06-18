import numpy as np

class ScoreMatrix(object):
  """
  ROLE: Create the score matrix of the 2 sequences
  """

  def __init__(
              self, 
              seq1="No", 
              seq2="Sequence", 
              pointsMatch = 2, 
              pointsMissmatchIntra = 1, 
              pointsMissmatchExtra = -1, 
              pointsOpeningGap = -10, 
              pointsExtensiveGap = -1
              ):
    """
    ROLE: Constructor
    PARAMETERS: seq1, string
                seq2, string
                pointsMatch, float
                pointsMissmatchIntra, float
                pointsMissmatchExtra, float
                pointsOpeningGap, float
                pointsExtensiveGap, float
    OUTPUTS: seqLen1, int
             seqLen2, int
    """

    self.seq1 = seq1
    self.seq2 = seq2
    self.seqLen1 = len(seq1)
    self.seqLen2 = len(seq2)

    self.pointsMatch = pointsMatch
    self.pointsMissmatchIntra = pointsMissmatchIntra
    self.pointsMissmatchExtra = pointsMissmatchExtra
    self.pointsOpeningGap = pointsOpeningGap
    self.pointsExtensiveGap = pointsExtensiveGap
    
    
  def init_matrix(self):
    """
    ROLE: Build a numpy array of 1 + sequences lenght dimensions.
          Init the first column and row with defaults integers values
          Fill the rest with None
    OUTPUTS: matrix, np.array
    """

    self.matrix=np.array([[None]*(self.seqLen2+1)]*(self.seqLen1+1))
    
    for i in range(self.seqLen2 + 1):
        self.matrix[0][i] = -i - 10
        
    for i in range(self.seqLen1 + 1):
        self.matrix[i][0] = -i - 10

    self.matrix[0][0] = 0
    

  def __getMatch(self, i, j):
    """
    ROLE: Get the score for a match
    PARAMETERS: i, int
                j, int
    """

    score = 0

    if self.seq1[i].lower() == self.seq2[j].lower():
        score = self.pointsMatch + self.matrix[i][j]
        
    elif (self.seq2[j].lower() == 'a' and self.seq1[i].lower() == 'g') \
    or (self.seq2[j].lower() == 'g' and self.seq1[i].lower() == 'a') \
    or (self.seq2[j].lower() == 'c' and self.seq1[i].lower() == 't') \
    or (self.seq2[j].lower() == 't' and self.seq1[i].lower() == 'c') \
    or (self.seq2[j].lower() == 'u' and self.seq1[i].lower() == 'c') \
    or (self.seq2[j].lower() == 'c' and self.seq1[i].lower() == 'u'):  
        score = self.pointsMissmatchIntra + self.matrix[i][j]
    
    else:  
        score = self.pointsMissmatchExtra + self.matrix[i][j]
    
    self.diagonalScore = score
  

  def __getGapUp(self, mtb, i, j):
    """
    ROLE: Get the score for a gap in the sequence 2
    PARAMETERS: mtb, TracebackMatrix
                i, int
                j, int
    """

    score = 0

    if i == 0:
        score = self.matrix[1 + i - 1][1 + j] + self.pointsOpeningGap

    else:
        if mtb[1 + i - 1][1 + j] == '|':
            score = self.matrix[1 + i - 1][1 + j] + self.pointsExtensiveGap

        else:
            score = self.matrix[1 + i - 1][1 + j] + self.pointsOpeningGap

    self.upScore = score


  def __getGapLeft(self, mtb, i, j):
    """
    ROLE: Get the score for a gap in the sequence 1
    PARAMETERS: mtb, TracebackMatrix
                i, int
                j, int
    """

    score = 0
    if j == 0:
        score = self.matrix[1 + i][j] + self.pointsOpeningGap
    else:
        if mtb[1 + i][j] == '-': #symbole du gap (si gap a gauche -> extensif)
            score = self.matrix[1 + i][j] + self.pointsExtensiveGap
        else:
            score = self.matrix[1 + i][j] + self.pointsOpeningGap
    self.leftScore = score

      
  def bestScore(self, mtb, i, j):  
    """
    ROLE: Get the best score between match, gap seq 2 and gap seq 1.
          Set the orgin of the best score
    PARAMETERS: mtb, TracebackMatrix
                i, int
                j, int
    """

    self.__getMatch(i, j)
    self.__getGapUp(mtb, i , j)
    self.__getGapLeft(mtb, i , j)

    if self.diagonalScore > self.upScore and self.diagonalScore > self.leftScore:
        self.maxScoreOrigin = "*"
    elif self.leftScore > self.diagonalScore and self.leftScore > self.upScore:
        self.maxScoreOrigin = "-"
    elif self.upScore > self.diagonalScore and self.upScore > self.leftScore:
        self.maxScoreOrigin = "|"
    elif self.diagonalScore == self.leftScore and self.diagonalScore > self.upScore:
        self.maxScoreOrigin = "DG"
    elif self.diagonalScore == self.upScore and self.diagonalScore > self.leftScore:
        self.maxScoreOrigin = "DH"
    elif self.leftScore == self.upScore and self.leftScore > self.diagonalScore:
        self.maxScoreOrigin = "GH"
    elif self.diagonalScore == self.leftScore and self.diagonalScore == self.upScore:
        self.maxScoreOrigin = "3"
        
    self.maxScore = max(self.diagonalScore, self.upScore, self.leftScore)
