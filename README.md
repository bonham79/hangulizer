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

-Pynini:
      K. Gorman. 2016. [Pynini: A Python library for weighted finite-state grammar compilation]
      (http://openfst.cs.nyu.edu/twik/pub/GRM/Pynini/pynini-paper.pdf).  
      In *Proc. ACL Workshop on Statistical NLP and Weighted Automata*, 75-80.
      
-Jamotools

-Wiktionary for Korean Lemmas and associated romanizations.

-Universal Dependencies Treebank for Training Data.

-OpenFst group:
        Cyril Allauzen, Michael Riley, Johan Schalkwyk, Wojciech Skut and Mehryar Mohri, 
        "OpenFst: A General and Efficient Weighted Finite-State Transducer Library", 
        Proceedings of the Ninth International Conference on Implementation and 
        Application of Automata, (CIAA 2007), volume 4783 of Lecture Notes in 
        Computer Science, pages 11-23. Springer, 2007. http://www.openfst.org.
