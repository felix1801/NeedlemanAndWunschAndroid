from threading import Thread

from ScoreMatrix import ScoreMatrix
from TracebackMatrix import TracebackMatrix
from Alignment import Alignment


class NwPOO(Thread):
    """
    ROLE: Working class that execute the alignment in background, in a separate worker than the main thread (thread = fonction qui s'éxécute en arrière plan et qui retourne le résultat au programme principal)
          Inherits from Thread class (become a thread)
    """
    def __init__(self, parameters, update_bar_alignment=None, **kwargs):
        """
        ROLE: Constructor.
        PARAMETERS: parameters, AlignmentParameters
                    update_bar_alignment: lambda function that update the progressbar value (optional)
        """

        Thread.__init__(self)   # Build Thread object which will execute the script in background
        
        self.parameters = parameters
        self.update_bar_alignment = update_bar_alignment

    def run(self):
        """
        ROLE: Processing of the alignment.
        COMMENT: This method should never be called directly. This is the 'start' method of the Thread Class (NwPOO) in the main file that will call this 'run' method.
        """

        ms=ScoreMatrix(
                        self.parameters.sequence1, 
                        self.parameters.sequence2, 
                        self.parameters.pointsMatch, 
                        self.parameters.pointsMissmatchIntra, 
                        self.parameters.pointsMissmatchExtra, 
                        self.parameters.pointsOpeningGap, 
                        self.parameters.pointsExtensiveGap
                        )        

        mtb=TracebackMatrix(
                            self.parameters.sequence1, 
                            self.parameters.sequence2, 
                            self.parameters.pointsMatch, 
                            self.parameters.pointsMissmatchIntra, 
                            self.parameters.pointsMissmatchExtra, 
                            self.parameters.pointsOpeningGap, 
                            self.parameters.pointsExtensiveGap
                            )

        ms.init_matrix()
        mtb.init_matrix()
        
        # Filling of both matrix
        for i in range(ms.seqLen1):
            for j in range(ms.seqLen2):
                ms.bestScore(mtb.matrix, i, j)
                ms.matrix[1+i][1+j] = ms.maxScore
                mtb.matrix[1+i][1+j] = ms.maxScoreOrigin
                self.update_bar_alignment()
                
        # Sequence alignment and score processing
        mtb.get_alignment()

        # Create the alignmentObject,
        self.alignment = Alignment(
                                    self.parameters,
                                    mtb.alignementSeq1,
                                    mtb.alignementQuali,
                                    mtb.alignementSeq2,
                                    mtb.scoreAlignement,
                                    mtb.nbMatch,
                                    mtb.nbGap,
                                    mtb.nbMissmatch,
                                    mtb.nbMissmatchIntra,
                                    mtb.nbMissmatchExtra
                                    )

        self.update_bar_alignment()   # Thanks to the lambda function passed in parameters of the class, call the 'update_bar_alignment' function in the main file
