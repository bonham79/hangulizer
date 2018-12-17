#!/usr/bin/env python
# coding: utf-8

##80% accuracy ~11 fails

from pynini import *
from unicodedata import *
import csv
import jamotools

#####################################################################################################################

ngram = Fst.read("fars/comp.syl.lm") ##Trigram yields 1% increase ~80.  But masssively slow.  
sym = SymbolTable.read_text("ngrams/comp.syl.sym")

####################################################################################################################
###Made a function so it wouldn't need to be read every time
def make_fst():
    ##Dictionaries of jamo and possible sounds they may take on. Onsets, rhymes and codas with associated romanizations above.    
    hangul_vowels = ['ㅏ' , 'ㅐ' ,'ㅑ' ,'ㅒ' ,'ㅓ' ,'ㅔ' ,'ㅕ' ,'ㅖ' ,'ㅗ' ,'ㅘ' ,'ㅙ' ,'ㅚ' ,'ㅛ' ,'ㅜ' ,'ㅝ' ,'ㅞ' ,'ㅟ' ,'ㅠ' ,'ㅡ' ,'ㅢ' ,'ㅣ']
    roman_vowels  = ['a'  , 'ae' ,'ya','yae','eo' ,'e' , 'yeo','ye', 'o' ,'wa','wae','oe' ,'yo' ,'u' , 'wo','we', 'wi', 'yu' ,'eu','ui' ,'i']
    hangul_codas = ['', 'ㅇ','ㄱ', 'ㄱ','ㄲ' , 'ㄴ' ,'ㄷ', 'ㄹ' ,'ㄹ' ,'ㅁ','ㅂ', 'ㅂ','ㅂ','ㅅ' ,'ㅅ' ,'ㅆ' ,'ㅆ' ,'ㅈ', 'ㅈ','ㅉ' ,'ㅊ' ,'ㄳ', 'ㄳ' , 'ㄵ' , 'ㄵ' ,'ㄶ', 'ㄶ','ㄺ', 'ㄺ', 'ㄻ', 'ㄻ','ㄼ', 'ㄼ','ㄼ','ㄽ', 'ㄽ','ㄽ','ㄾ','ㄾ','ㄿ','ㄿ','ㅀ', 'ㅀ','ㅄ', 'ㅄ']
    roman_codas  = ['' ,'ng','k', 'g','k' , 'n'  ,'t',  'l' ,'r' ,'m',  'p', 'b', 'm', 't' ,'s' , 't' , 'ss' ,'t',  'j', 't' ,'t'  , 'g', 'gs',  'nj'  ,'nt','nh', 'n', 'g', 'lg','m' ,'lm', 'b', 'lb','lp','s' ,'ls', 'l', 't','l', 'p','l', 'h', 'l', 'p', 'ps']  
    hangul_onsets = ['ㅎ','ㅇ' ,'ㄱ' , 'ㄲ' , 'ㄴ' ,'ㄷ' ,'ㄷ' ,'ㄷ' ,'ㄸ' ,'ㄸ','ㄹ' ,'ㄹ','ㅁ','ㅂ' ,'ㅃ' ,'ㅅ' ,'ㅆ', 'ㅈ' ,'ㅉ' ,'ㅊ' ,'ㅋ' ,'ㅌ','ㅍ'] ##We count the empty sign
    roman_onsets  = ['h' , ''   ,'g'  , 'kk','n' ,'d',  't' ,'ch','dd','tt',  'r', 'l','m' ,'b' , 'pp', 's' ,'ss', 'j' ,'jj' ,'ch' , 'k' ,'t', 'p']

    ###Normalizing and zipping into iterables.
    hanrom_vowels = [[normalize("NFKC", i[0]), i[1]] for i in zip(hangul_vowels,roman_vowels)] 
    hanrom_codas = [[normalize("NFKC", i[0]), i[1]] for i in zip(hangul_codas,roman_codas)]
    hanrom_onsets = [[normalize("NFKC", i[0]), i[1]] for i in zip(hangul_onsets,roman_onsets)] 

    #####################################################################################################################
    ###Iterates through all possible combinations of korean sounds and their syllabification. Creates dictionary to hold all.  
    syllables = dict()##Form roman:hangul
    for honset, ronset in hanrom_onsets:
        for hvowel, rvowel in hanrom_vowels:
            for hcoda, rcoda in hanrom_codas:
                hsyl = normalize("NFKC", jamotools.join_jamos(honset + hvowel + hcoda))
                rsyl = ronset + rvowel + rcoda 
                if len(hsyl) >= 2:
                    continue
                hsyl = "[" + str(ord(hsyl)) + "]"
                if rsyl in syllables: ##We've encounterd this romanization before.  Adds to list.  
                    syllables[rsyl] += [hsyl]
                else:
                    syllables[rsyl] = [hsyl]
     
    ###Turns into tuple to make our Pynini life easier.                 
    mapping = []
    for roman, hanguls in syllables.items():
        for hangul in hanguls:
            mapping += [[roman, hangul]]
            
    mapping += [[" ", " "]] ##Makes sure our spacing is viable.  
    syllable_fst = string_map(mapping).closure().optimize()

    syllable_fst.write("fars/P2G_Hangul_Ngram_Syl.fst")
#####################################################################################################################
###Initializes FST if it was lost.
try:
    FST = Fst.read("fars/P2G_Hangul_Ngram_Syl.fst")
except:
    FST = make_fst()

#####################################################################################################################

def sing_hangulize(roman):
    lattice = roman.lower().replace("-","") * FST * ngram
    results_FST = shortestpath(lattice).project(True).rmepsilon()
    results = [chr(int(jamo)) for jamo in results_FST.stringify(sym).split()] ###Applies to each seperate codepoint
    jamos = ''.join(results) ##""Then joins
    return(jamotools.join_jamos(jamos))


###This is an abomination.  Figure out your goddamn spaces
def hangulize(romans):
    if " " in romans:
        return(" ".join([sing_hangulize(romam) for romam in romans.split()]))
    else:
        return sing_hangulize(romans)
    
