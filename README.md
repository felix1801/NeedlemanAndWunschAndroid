Welcome to Félix MORTAS's Needleman & Wunsch alignment algorithm.

This is the DNA sequence alignment algorithm of Needleman & Wunsch
This algorithm allows to align 2 DNA sequences of different sizes by putting a maximum of matches and a minimum of gaps.

The user can decide to align the demonstration sequences provided with the program, or can align 2 DNA sequences from 2 files with fasta extension
These files are fairly easy to find on the internet (NCBI for example) and should be stored somewhere on the user's device


Prerequisites:
	Libraries to install :
		- kivy 2.0.0
		- numpy (normally already in anaconda environment)


Usage:

Run main.py

1) Select the fasta files with the buttons "select file 1" and "select file 2"
	If you don't have any fasta file and want to use the demo files, ignore this step
	
2) Edit the points for each match, missmatch and gap event (useful for geneticists who know about them, or for those who want to test hasardous alignments)
	If you have no idea what the scores mean, don't touch anything and leave the default values
	
3) Press the "Launch" button

4) View:
	- The name of the sequences
	- The alignment of the sequences (scrollable)
	- The stats (scores, number of gaps ...)

5) Save your file in text format with the "Save" button
	
Good alignment !
