from pynini import *
from unicodedata import *
import csv
import jamotools
import P2G_Hangul_Ngram_Syl
import P2G_Hangul_Rule

CODED = "NFKD"

def test():
    #Provide Data for fine tuning
	with open("data/Hangul_Roman.csv", "r") as source:
		error = 0
		total = 0
		correct = 0
		for (hangul, roman1, roman2, roman3, roman4) in csv.reader(source, delimiter=","):
			print(roman1)
			try:
				total += 1
				x = jamotools.join_jamos(P2G_Hangul_Rule.hangulize(roman1))
				accuracy = ((normalize(CODED, x) == normalize(CODED, hangul)) or (normalize(CODED, jamotools.join_jamos(P2G_Hangul_Ngram_Syl.hangulize(roman1))) == normalize(CODED, hangul)))
                ###Short circuiting booleans to test if at least one is right
				if accuracy:
					correct += 1
				else:                
					print(roman1 + " : " + x)
					print(" Should be: " + jamotools.join_jamos(hangul))
			except Exception as e:
				error += 1
		print(error)
		print(total - correct)
		print(correct/total)