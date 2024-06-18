import numpy as np #ce module permet la creation de tableau (arrays)

class TracebackMatrix(object):
    """
    ROLE: Create the traceback matrix of the 2 sequences
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

        self.pointsMatch = pointsMatch
        self.pointsMissmatchIntra = pointsMissmatchIntra
        self.pointsMissmatchExtra = pointsMissmatchExtra
        self.pointsOpeningGap = pointsOpeningGap
        self.pointsExtensiveGap = pointsExtensiveGap
        
        self.seq1 = seq1
        self.seq2 = seq2
        self.seqLen1 = len(seq1)
        self.seqLen2 = len(seq2)


    def init_matrix(self):
        """
        ROLE: Build a numpy array of 1 + sequences lenght dimensions.
              Init the first column and row with defaults integers values
              Fill the rest with None
        OUTPUT: matrix, np.array
        """

        self.matrix = np.array([[None]*(self.seqLen2+1)]*(self.seqLen1+1))

        for i in range(self.seqLen2 + 1):
            self.matrix[0][i] = "-"
        for i in range(self.seqLen1 + 1):
            self.matrix[i][0] = "|"

        self.matrix[0][0] = "Done"

            
    def align(self):  
        """
        ROLE: Follow the best alignment from the bottom right corner of the matrix
        OUTPTUS: alignmentSeq1, string
                 alignmentQuali, string
                 alignmentSeq2, string
        """

        # Init values
        i = self.matrix.shape[0] - 1
        j = self.matrix.shape[1] - 1

        self.alignementSeq1 = ""
        self.alignementSeq2 = ""
        self.alignementQuali = ""
        
        # Browse the matrix from the bottom right corner by taking the path with highest score
        while self.matrix[i][j] != "Done":

            if self.matrix[i][j] == '*' or self.matrix[i][j] == "3" or self.matrix[i][j] == "DG" or self.matrix[i][j] == "DH":  

                self.alignementSeq1 += self.seq1[i-1]
                self.alignementSeq2 += self.seq2[j-1]
                if self.seq1[i-1].lower() == self.seq2[j-1].lower():
                    self.alignementQuali += "|"
                else:
                    self.alignementQuali += ":"
                    
                i -= 1  
                j -= 1
            
            if self.matrix[i][j] == '|' or self.matrix[i][j] == "GH":

                self.alignementSeq1 += self.seq1[i-1]
                self.alignementSeq2 += '-'
                self.alignementQuali += " "
                
                i -= 1  
            
            elif self.matrix[i][j] == "-":

                self.alignementSeq1 += "-"
                self.alignementSeq2 += self.seq2[j-1]
                self.alignementQuali += " "
                
                j -= 1  
        
        self.alignementSeq1 = self.alignementSeq1[::-1]
        self.alignementQuali = self.alignementQuali[::-1]
        self.alignementSeq2 = self.alignementSeq2[::-1]
        

    def __countMatchs(self): 
        """
        ROLE: Count the number of matchs of the alignment
        OUTPUTS: nbMatch, int
        """

        nbMatch = 0

        for i in range(len(self.alignementQuali)):
            if self.alignementQuali[i] == "|":
                nbMatch += 1

        self.nbMatch=nbMatch
        

    def __countMissmatchs(self):  
        """
        ROLE: Count the number of missmatchs of the alignment
        OUTPUTS: nbMissmatch, int
        """

        nbMissmatch = 0
        nbMissmatchIntra = 0
        nbMissmatchExtra = 0

        for i in range(len(self.alignementQuali)):
            if self.alignementQuali[i] == ":":
                nbMissmatch += 1
                
                if (self.alignementSeq2[i].lower() == 'a' and self.alignementSeq1[i].lower() == 'g') \
                or (self.alignementSeq2[i].lower() == 'g' and self.alignementSeq1[i].lower() == 'a') \
                or (self.alignementSeq2[i].lower() == 'c' and self.alignementSeq1[i].lower() == 't') \
                or (self.alignementSeq2[i].lower() == 't' and self.alignementSeq1[i].lower() == 'c') \
                or (self.alignementSeq2[i].lower() == 'u' and self.alignementSeq1[i].lower() == 'c')  \
                or (self.alignementSeq2[i].lower() == 'c' and self.alignementSeq1[i].lower() == 'u'):
                    nbMissmatchIntra += 1
                
                else :
                    nbMissmatchExtra += 1

        self.nbMissmatch = nbMissmatch
        self.nbMissmatchIntra = nbMissmatchIntra
        self.nbMissmatchExtra = nbMissmatchExtra


    def __countGaps(self):  
        """
        ROLE: Count the number of gaps of the alignment
        OUTPUTS: nbGap, int
        """

        nbGap = 0

        for i in range(len(self.alignementQuali)):
            if self.alignementQuali[i] == " ":
                nbGap += 1
        
        self.nbGap = nbGap


    def __countScore(self):
        """
        ROLE: Count the value of the best alignment score
        OUTPUTS: scoreAlignment, float
        """

        score=0

        for i in range(len(self.alignementQuali)):
            if self.alignementQuali[i] == "|":
                score += self.pointsMatch

            elif self.alignementQuali[i] == "-":
                if i == 0:
                    score += self.pointsOpeningGap
                elif self.alignementQuali[i-1] == "-":
                    score += self.pointsExtensiveGap
                else:
                    score += self.pointsOpeningGap

            elif self.alignementQuali[i] == ":":
                if (self.alignementSeq2[i].lower() == 'a' and self.alignementSeq1[i].lower() == 'g') \
                or (self.alignementSeq2[i].lower() == 'g' and self.alignementSeq1[i].lower() == 'a') \
                or (self.alignementSeq2[i].lower() == 'c' and self.alignementSeq1[i].lower() == 't') \
                or (self.alignementSeq2[i].lower() == 't' and self.alignementSeq1[i].lower() == 'c') \
                or (self.alignementSeq2[i].lower() == 'u' and self.alignementSeq1[i].lower() == 'c') \
                or (self.alignementSeq2[i].lower() == 'c' and self.alignementSeq1[i].lower() == 'u'):
                    score += self.pointsMissmatchIntra 
                else:
                    score += self.pointsMissmatchExtra 

        self.scoreAlignement = score


    def get_alignment(self):
        """
        ROLE: Align the sequences and counts the number of matchs, missmatchs, gaps and score
        """

        self.align()
        self.__countMatchs()
        self.__countMissmatchs() 
        self.__countGaps()
        self.__countScore()
