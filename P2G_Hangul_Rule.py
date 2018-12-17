#!/usr/bin/env python
# coding: utf-8

###To try out:  Take final rule based P2G and place syl (or char) ngram on top.
###Since we've already resolved everything into Hangul, all that's necessary is to 
###Make an intermediary fst to convert hangul back to code points
###Then can be fitted onto ngram
####COMBINED WITH SYLnGRAM: 91%  eRROR RATE 11
###Character Model makes no significant change
from pynini import *
from unicodedata import *
import csv
import jamotools

CODED = "NFKD"

#####################################################################################################################
###Creates our FST.  We didn't want to run it every time so decided to make it a simple function
def make_fst():
	###Assigns all Korean Chars a roman equivalent.  CODED implies they were normalized.  
	##S used for empty char due to conflation with /ng/ character.  N for /ng/ character.  
	hangul_chars = [" ", 'ㅇ', 'S', " ", 'ㄱ' , 'ㄲ' , 'ㄴ' ,'ㄷ' ,'ㄸ' ,'ㄹ' ,'ㅁ','ㅂ' ,'ㅃ' ,'ㅅ' ,'ㅆ' ,'N','ㅈ' ,'ㅉ' ,'ㅊ' ,'ㅋ' ,'ㅌ','ㅍ' ,'ㅎ','ㅏ' , 'ㅐ' ,'ㅑ' ,'ㅒ' ,'ㅓ' ,'ㅔ' ,'ㅕ' ,'ㅖ' ,'ㅗ' ,'ㅘ' ,'ㅙ' ,'ㅚ' ,'ㅛ' ,'ㅜ' ,'ㅝ' ,'ㅞ' ,'ㅟ' ,'ㅠ' ,'ㅡ' ,'ㅢ' ,'ㅣ']
	hangul = string_map([[normalize(CODED, _)] for _ in hangul_chars])

	roman_chars = ["-", " ", 'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
	roman = string_map([[_] for _ in roman_chars])

	closure = union(hangul, roman).closure().optimize()

	##FSTs


	###For Variants that may arise for rules
	hangul_vowels = ['ㅏ' , 'ㅐ' ,'ㅑ' ,'ㅒ' ,'ㅓ' ,'ㅔ' ,'ㅕ' ,'ㅖ' ,'ㅗ' ,'ㅘ' ,'ㅙ' ,'ㅚ' ,'ㅛ' ,'ㅜ' ,'ㅝ' ,'ㅞ' ,'ㅟ' ,'ㅠ' ,'ㅡ' ,'ㅢ' ,'ㅣ']
	hangul_vowels_CODED = string_map([[normalize(CODED, _)] for _ in hangul_vowels])
	hangul_codas = ['ㄱ', 'ㄲ' , 'ㄴ' ,'ㄷ', 'ㄹ' ,'ㅁ','ㅂ', 'ㅅ' ,'ㅆ' ,'N','ㅈ']
	hangul_codas_CODED = string_map([[normalize(CODED, _)] for _ in hangul_codas])
	hangul_onsets = [" ", 'ㄱ' , 'ㄲ' , 'ㄴ' ,'ㄷ' ,'ㄸ' ,'ㄹ' ,'ㅁ','ㅂ' ,'ㅃ' ,'ㅅ' ,'ㅆ', 'ㅈ' ,'ㅉ' ,'ㅊ' ,'ㅋ' ,'ㅌ','ㅍ' ,'ㅎ', "S"] ##We count the empty sign
	hangul_onsets_CODED = string_map([[normalize(CODED, _)] for _ in hangul_onsets])


	###Fsts based off korean jamos that romanize to three letters.  
	hangul_tri = ['ㅒ' , 'ㅕ' , 'ㅙ']
	roman_tri = [ 'yae', 'yeo', 'wae']
	hangul_tri_CODED = [normalize(CODED, _) for _ in hangul_tri]

	roman_hangul_tri = [_ for _ in zip(roman_tri, hangul_tri_CODED)]
	roman_hangul_FST_tri = cdrewrite(string_map(roman_hangul_tri), "", "", closure).optimize()

	###As abbove for double letters.  
	hangul_doub = ['ㄲ', 'ㄲ', 'ㅃ' , 'ㄸ', 'ㄸ', 'ㅃ', 'ㅆ', 'ㅉ', 'ㅊ', 'N', 'ㅐ',  'ㅑ',  'ㅖ', 'ㅘ', 'ㅚ', 'ㅛ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅓ'  , 'ㅅ']
	roman_doub = ['kk','gg', 'pp', 'tt', 'dd', 'bb', 'ss', 'jj', 'ch', 'ng', 'ae', 'ya',  'ye','wa', 'oe', 'yo', 'wo', 'we', 'wi', 'yu', 'eu', 'ui', 'eo', "sh"]
	hangul_doub_CODED = [normalize(CODED, _) for _ in hangul_doub]

	roman_hangul_doub = [_ for _ in zip(roman_doub, hangul_doub_CODED)]
	roman_hangul_FST_doub = cdrewrite(string_map(roman_hangul_doub), "", "", closure).optimize()

	###All the rest of the chars.  Some hangul will be repeated as there are multiple forms of mapping
	hangul_sing = ['ㄱ', 'ㄱ',  'ㄲ', 'ㄴ', 'ㄷ', 'ㄷ',  'ㄹ', 'ㄹ', 'ㅁ','ㅂ', 'ㅂ', 'ㅅ', 'ㅅ', 'ㅆ', 'ㅈ', 'ㅈ', 'ㅋ','ㅌ', 'ㅍ', 'ㅎ', 'ㅏ', 'ㅗ', 'ㅜ', 'ㅣ', 'ㅔ']
	roman_sing =  ['k',  'g',   'k', 'n',  'd',  't',  'r' , 'l',  'm', 'b',  'p',  's',  't', 't', 'j',  't',  'k', 't', 'p',  'h',  'a', 'o',  'u',  'i',  'e']                               
	hangul_sing_CODED = [normalize(CODED, _) for _ in hangul_sing]

	roman_hangul_sing = [_ for _ in zip(roman_sing, hangul_sing_CODED)]
	roman_hangul_FST_sing = cdrewrite(string_map(roman_hangul_sing), "", "", closure).optimize()

	####Base P2G
	hangul_roman= (roman_hangul_FST_tri * roman_hangul_FST_doub * roman_hangul_FST_sing)

	#####################################################################################################################

	###Following rules attempt to adjust issues that arrise in regards to Hangul 'o'
	###As Hangul uses 'o' for both /ng/ and to designate a lack of onset to a rhyme, need to demonstrate when each should occur.  
	###First is integrating a space marker "S" to designate the use of the 'o' jamo when no onset to rhyme. Our function assigns a space
	###to the beginning of words to disambiguate this occurence.  We then remove the space.   
	initial_spacing_FST = cdrewrite(transducer("", "S"), " ", hangul_vowels_CODED, closure)  * cdrewrite(transducer(" ", ""), "", "", closure) 
	###Now inserts the 'o' whenever vowels are adjacent or next to the coda /ng/.  Due to korean syllable constraints, this is a 
	###comfortable assumption for where an onset should occur.  
	spacing_FST = initial_spacing_FST * cdrewrite(transducer("", "S"), hangul_vowels_CODED | 'N', hangul_vowels_CODED, closure).optimize()

	###To bring back original hangul characters S and N were standing for
	char_return =  cdrewrite(string_map([["S", "ᄋ"], ["N", "ᄋ"]]), "", "", closure)

	##Taking care of hyphens
	hyphen_reduction = cdrewrite(transducer("-", ""), "", "", closure)

	#####################################################################################################################
	##Assorted phonological rules that should improve accuracy.  
	###Series of sonorants applicable to korean.  
	roman_sonorants_FST = union('a','e','i','l','m','n','o','r','u', 'y', 'w', 'ng').optimize()

	##If a P, T, or K occurs intervocalically.  We know that it isn't the unaspirated forms as those would be rendered as voiced in 
	#english interpretation.  Thus, must be the aspirated forms
	voicing = cdrewrite(string_map([['p',normalize(CODED, 'ㅍ')], ['t', normalize(CODED, 'ㅌ')], ['k', normalize(CODED, 'ㅋ')]]), roman_sonorants_FST, roman_sonorants_FST, closure).optimize()

	##Largely just need to make sure it doesn't affect geminates.  But since Korean will only have a vowel in this position, we can be lazy and use sonorants
	word_onset = cdrewrite(string_map([['p',normalize(CODED, 'ㅍ')], ['t', normalize(CODED, 'ㅌ')], ['k', normalize(CODED, 'ㅋ')]]), " ", roman_sonorants_FST, closure).optimize()

	###Common in Hangul to realize a alveolar coda with this character
	alveolar_stop = cdrewrite(transducer("t",normalize(CODED,"ㅅ")), "", " ", closure) ###Common in Hangul to realize a alveolar coda with this character

	phonemic_rule_rev =  word_onset * voicing * alveolar_stop

	#####################################################################################################################
	###Final Product
	hangul_roman_FST =  phonemic_rule_rev * hangul_roman * hyphen_reduction * spacing_FST * char_return

	hangul_roman_FST.write("fars/P2G_Hangul_Rule.fst")
#####################################################################################################################

###Initializes Fst for the Hangulize function
try:
	FST = Fst.read("fars/P2G_Hangul_Rule.fst")
except:
	FST = make_fst()

#####################################################################################################################

def hangulize(roman):
    ##Roman script to Hangul converter
    roman = " " + roman.lower() + " "  ##" " is because we cannot remember beginning of word and end of word names
    return jamotools.join_jamos(shortestpath(roman * FST).stringify())

       