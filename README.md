# hangulizer
Phoneme to Grapheme converter (P2G) between roman and hangul script for LING83600.  Takes a text containing romanization of Korean lemms and produces list of likely equivalents in Hangul script. 

To use:
  [python3 (shebang added but untested due to dev issues)] hangulize.py [--Syllable] source [output (hangul.txt by default)]
  
  Note: --Syllable flag increases range of outputs and increases accuracy at possible cost to run-time performance.

Required: 
- python 3.6.5 or later.  
- pynini package and associated dependencies (please see requirements at http://www.openfst.org/twiki/bin/view/GRM/Pynini)
- jamotools package: pip install jamotools

Common Issues:
- Software assumes that provided forms are romanizations of Hangul graphemes.  As such, assumes syllable composition to be VALID PHONETIC APPROXIMATIONS OF KOREAN WORDS.  Usage of English exclusive phonemes (/f/, /v/, /z/) will result in ERROR token in output text string.
-Above issue also applies to mophological restrictions in Korean.  (e.g. conversion of "string").  Will result in runtime error.  (Future work intends to alleviate this issue.)   

Thanks to:
-Pynini
-Jamotools
-Wiktionary for Korean Lemmas and associated romanizations.
-Universal Dependencies Treebank for Training Data.
-OpenFst group. 
