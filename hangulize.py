#!/usr/bin/env python
# coding: utf-8
##Main code for a Phoneme to Grapheme Converter from Roman text to Korean Hangul script.
##For console use: default program simply needs a txt file to be provided for conversion before providing
## a rule based conversion.  e.g. hangulize "romanization.txt"
##Flags for use is a boolean for introduction of conversions using Syllable based ngram models (--Syllable) **recommended for accuracy
##In cases where strings differ, will provide all forms ("x/y") for user to choose.  
##If detectable strings that are not conductive to Korean phonemics are provided, will be replaced with ERROR in output text file.

import argparse
import operator
from unicodedata import *
import P2G_Hangul_Ngram_Syl
import P2G_Hangul_Rule

invalids = {'q', 'f', 'z', 'x', 'v'}

def validate(string):
	###Checks for use of characters that should not occur in Korean Romanization/phoneticization
	for i in string:
		if i in invalids:
			return False
	return True 

def hangulize(roman, Syl=True):
	##Passes to subsidiary converters 
	hanguls = []
	hanguls.append(normalize("NFKC", P2G_Hangul_Rule.hangulize(roman)))
	if Syl:
		hangul = P2G_Hangul_Ngram_Syl.hangulize(roman)
		if hangul not in hanguls:
			hanguls.append(hangul)
	return "/".join(hanguls)

def main(args):
	with open(args.Romanization) as source:
		with open(args.Target, 'w') as sink:
			for line in source:
				for i in line.split():
					if (validate(i)):
						sink.write(hangulize(i, args.Syllable) + " ")
					else:
						sink.write("ERROR")
				sink.write("\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Phoneme to Grapheme translator for Korean Romanization")
    parser.add_argument("--Syllable", action="store_true",default=False, help="Determines whether to incorporate Syllable based Ngram Model for higher accuracy rate")
    parser.add_argument("Romanization", help="Text file to romanize")
    parser.add_argument("Target", nargs='?', default="hangul.txt", help="Name of file to write to")
    main(parser.parse_args())