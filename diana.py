#!/usr/bin/env python 
# -*- coding: utf-8 -*-"
"""
DiaNA - 2020 - by psy (epsylon@riseup.net)

You should have received a copy of the GNU General Public License along
with DiaNA; if not, write to the Free Software Foundation, Inc., 51
Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""
VERSION = "v0.3_beta"
RELEASE = "19032020"
SOURCE1 = "https://code.03c8.net/epsylon/diana"
SOURCE2 = "https://github.com/epsylon/diana"
CONTACT = "epsylon@riseup.net - (https://03c8.net)"
"""
DNA-equiv:
 A <-> T
 C <-> G
"""
import re, os, glob, random, time, math
import matplotlib.pyplot as plt
import matplotlib.patches as patches

brain_path = "resources/BRAIN/brain.in" # in/out brain-tmp file
genomes_path = 'datasets/' # genome datasets raw data
genomes_list_path = "datasets/genome.list" # genome list
universal_primer_list_path = "resources/PATTERNS/UPL.list" # UPL list
dna_codons_list_path = "resources/PATTERNS/CODONS/DNAcodon.list" # DNA codon list
protein_formula_path = "resources/PATTERNS/CODONS/AAformula.list" # Protein Chemical Formula list
open_reading_frames_init_path = "resources/PATTERNS/ORF/ORF-init.list" # ORF init list
open_reading_frames_end_path = "resources/PATTERNS/ORF/ORF-end.list" # ORF end list
genomes = {} # main sources dict: genome_name
seeds_checked = [] # list used for random checked patterns
repeats = {} # repetitions 'tmp' dict: genome_name:(repets,pattern)
known_patterns = [] # list used for known patterns
max_length = 50 # [MAX. LENGTH] for range [PATTERN]

SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")

def convert_size(size):
    if (size == 0):
        return '0 B'
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size,1024)))
    p = math.pow(1024,i)
    s = round(size/p,2)
    return s, size_name[i]

def search_pattern_with_human():
    pattern = input("[HUMAN] [SEARCH] Pattern (ex: attacg): ").upper()
    print("\n"+"-"*5 + "\n")
    create_new_pattern(pattern) # create new pattern

def try_pattern_against_all_genomes_by_genome(pattern):
    for k, v in genomes.items():
        if pattern in v:
            t = len(re.findall(pattern, v))
            repeats[k] = t, pattern # create dict: genome = times, pattern

def try_pattern_against_all_genomes_by_pattern(pattern, index):
    p_index = 0 # pattern index
    for k, v in genomes.items():
        if pattern in v:
            p_index = p_index + 1
            t = len(re.findall(pattern, v))
            repeats[index,p_index] = pattern, k, t # create dict: index, p_index = pattern, genome, times

def sanitize_dna_pattern(pattern):
    valid_pattern = True
    for c in pattern:
        if c == "A":
            pass
        elif c == "T":
            pass
        elif c == "G":
            pass
        elif c == "C":
            pass
        elif c == "N":
            pass
        else:
            valid_pattern = False
    return valid_pattern

def teach_ai():
    mode = input("[TRAIN-AI] MODE -> (H)uman, (A)utomata: ").upper()
    if not os.path.isfile(brain_path):
        create_initial_seed_file()
    if mode == "H": # human mode
        teach_ai_human_mode()
    else: # libre AI
        teach_ai_automata_mode() # automata mode

def teach_ai_human_mode(): # search/discard patterns with human interaction & generate local database
    search_patterns_lesson_with_a_human()

def search_patterns_lesson_with_a_human():
    print("\n"+"-"*30)
    print("\n[TRAIN-AI] [HUMAN] [STOP] this mode; just entering whatever invalid pattern (ex: 'exit' or 'q').\n")
    key = "K" # continue
    while key == "K":
        pattern = input("[TRAIN-AI] [HUMAN] [LOOP] [SEARCH] Pattern (ex: attacg): ").upper()
        print("\n"+"-"*5 + "\n")
        key = search_pattern_on_lesson(pattern)
        if key == "Z": # stop
            break

def search_pattern_on_lesson(pattern):
    valid_pattern = sanitize_dna_pattern(pattern)
    if valid_pattern == True:
        key = search_pattern_on_local_database(pattern) # search pattern on local database
    else:
        print("[ERROR] -> Invalid DNA pattern ... [EXITING!]\n")
        key = "Z" # stop
    return key

def search_pattern_on_local_database(pattern):
    f=open(brain_path, 'r')  
    memory = f.read().replace('\n',' ')
    f.close()
    patterns_known = 0
    if not "'"+pattern+"'" in memory: # always create new patterns
        create_new_pattern(pattern) # create new pattern
        patterns_known = patterns_known + 1
    else:
        for k, v in genomes.items(): # create patterns found for new genomes
            if k not in memory:
                create_new_pattern(pattern) # create new pattern
                patterns_known = patterns_known + 1
    if patterns_known == 0:
        print("[TRAIN-AI] [AUTOMATA] [LOOP] [RESULTS] -ALREADY- [LEARNED!] ... -> [GOING FOR NEXT!]\n")
    print("-"*5 + "\n")
    key = "K" # continue
    return key

def create_initial_seed_file():
    f=open(brain_path, 'w')
    f.write("")
    f.close()    

def create_new_pattern(pattern): # append it to brain
    valid_pattern = sanitize_dna_pattern(pattern)
    if valid_pattern == True:
        if pattern not in known_patterns:
            known_patterns.append(pattern)
            try_pattern_against_all_genomes_by_genome(pattern) # generate repeats dict
        patterns_found = 0
        for k, v in repeats.items(): # list patterns found to output
            print (" *", k +":", "-> ",v,"")
            patterns_found = patterns_found + 1
            print("")
        if patterns_found == 0:
            print("[INFO] -> Not any found! ... [EXITING!]\n")
        else:
            f=open(brain_path, 'a')    
            f.write(str(repeats)+os.linesep) # add dict as str
            f.close()
    else:
        print("[ERROR] -> Invalid DNA pattern ... [EXITING!]\n")

def teach_ai_automata_mode(): # search patterns by bruteforcing ranges & generate local database
    search_patterns_lesson_with_an_ai()

def search_patterns_lesson_with_an_ai():
    print("\n"+"-"*30)
    print("\n[TRAIN-AI] [AUTOMATA] [STOP] this mode; pressing 'CTRL+z'.\n")
    ranges = input("[TRAIN-AI] [AUTOMATA] [SEARCH] Set range (x<y) for pattern deep searching (ex: 2-8): ")
    print ("")
    valid_range, ranged_permutations = check_for_deep_searching_ranges(ranges)
    if str(valid_range) == "OK!":
        ranged_ending = False
        print("-"*15)
        print("\n[TRAIN-AI] [AUTOMATA] [SEARCH] Number of [PERMUTATIONS] estimated: [ "+str(ranged_permutations)+" ]\n")
        print("-"*15+"\n")
        num_pat = 0
        while ranged_ending == False: # try to STOP it using: CTRL-z
            try:
                pattern, ranged_ending = generate_random_pattern(ranges, ranged_permutations) # generate random seed
                if pattern:
                    num_pat = num_pat + 1
                    print("[TRAIN-AI] [AUTOMATA] [LOOP] [SEARCH] Generating [RANDOM!] ["+str(num_pat)+"/"+str(ranged_permutations)+"] pattern: [ " + str(pattern) + " ]\n")
                    if not num_pat == ranged_permutations:
                        search_pattern_on_lesson(pattern)
                    else:
                        search_pattern_on_lesson(pattern)
                        print("[TRAIN-AI] [AUTOMATA] [RESULTS]: REVIEWED -> [ "+str(ranged_permutations)+" PERMUTATIONS ] ... -> [EXITING!]\n")
                        ranged_ending = True
            except:
                pass
    else:
        print("-"*15+"\n")
        print("[TRAIN-AI] [AUTOMATA] [ERROR] -> [INVALID!] Deep Learning [RANGE] -> "+valid_range+" ... [EXITING!]\n")

def generate_random_pattern(ranges, ranged_permutations):
    ranged_length = 0
    try:
        range_low = int(ranges.split("-")[0])
        range_high = int(ranges.split("-")[1])
        for i in range(range_low, range_high+1):
            ranged_length = ranged_length + 1
            if ranged_length == ranged_permutations: # all possible variables have been bruteforced/checked! -> exit
                pattern = None
                ranged_ending = True
                return pattern, ranged_ending
            else:
                ranged_ending = False
                seed = [random.randrange(0, 4) for _ in range(i)] # generate "random" seed
                if seed not in seeds_checked:
                    seeds_checked.append(seed)
                    pattern = ""
                    for n in seed:
                        if n == 0:
                            pattern += "A"
                        elif n == 1:
                            pattern += "C"
                        elif n == 2:
                            pattern += "T"
                        else:
                            pattern += "G"
                    return pattern, ranged_ending
    except:
        print("[TRAIN-AI] [AUTOMATA] [ERROR] -> [INVALID!] Deep Learning [RANGE] ... [EXITING!]\n")
        pattern = None
        ranged_ending = True
        return pattern, ranged_ending

def check_for_deep_searching_ranges(ranges):
    try:
        range_low = ranges.split("-")[0]
        range_high = ranges.split("-")[1]
    except:
        valid_range = "'bad format'"
    try:
        range_low = int(range_low)
    except:
        valid_range = "'low range' should be an integer"
    try:
        range_high = int(range_high)
    except:
        valid_range = "'high range' should be an integer"
    try:
        if range_low < range_high:
            if range_low > 1: # always range > 1
                valid_range = "OK!"
            else:
                valid_range = "'low range' should be > than 1"
        else:
            valid_range = "'low range' should be < than 'high range'"
    except:
        valid_range = "'bad format'"
    try:
        ranged_permutations = math_ranged_permutations(range_low, range_high)
    except:
        ranged_permutations = 0
        valid_range = "'bad format'"
    return valid_range, ranged_permutations

def math_ranged_permutations(range_low, range_high): # calculate ranged_permutations
    ranged_permutations = 0
    for i in range(range_low, range_high+1):
        ranged_permutations = ranged_permutations + (4**i)
    return ranged_permutations

def libre_ai(): # show statistics / download new genomes / keep crossing new genomes with local database / search for new patterns (non stop!)
    if not os.path.isfile(brain_path):
        create_initial_seed_file()
    memory = examine_stored_brain_memory() 
    if memory != "":
        #print("[LIBRE-AI] [STOP] this mode; pressing 'CTRL+z'.\n")
        libre_ai_show_statistics(memory) # show statistics

def libre_ai_show_statistics(memory):
    print("[LIBRE-AI] [REPORTING] [STATISTICS] ... -> [STARTING!]\n")
    print("-"*15 + "\n")
    total_genomes = 0
    total_adenine = 0
    total_guanine = 0
    total_cytosine = 0
    total_thymine = 0
    total_any = 0
    total_patterns = 0
    secuence_length = 0
    secuences_length_list = {}
    largest = None
    largest_len = 0
    shortest_len = 0
    average = None
    shortest = None
    for k, v in genomes.items():
        secuence_length = len(v)
        secuences_length_list[k] = str(secuence_length)
        total_genomes = total_genomes + 1
        total_adenine = total_adenine + v.count("A")
        total_guanine = total_guanine + v.count("G")
        total_cytosine = total_cytosine + v.count("C")
        total_thymine = total_thymine + v.count("T")
        total_any = total_any + v.count("N")
    path = genomes_path # genome datasets raw data
    l = glob.glob(genomes_path+"*") # black magic!
    latest_collection_file = max(l, key=os.path.getctime)
    latest_collection_date = time.ctime(os.path.getmtime(latest_collection_file))
    total_nucleotids = [total_adenine, total_guanine, total_cytosine, total_thymine, total_any]
    num_total_nucleotids = total_adenine + total_guanine + total_cytosine + total_thymine + total_any
    nucleotid_more_present = max(total_nucleotids)
    print("[LIBRE-AI] [REPORTING] -STORAGE- [STATISTICS]: \n")
    extract_storage_sizes()
    print(" * [LATEST UPDATE]: '"+str(latest_collection_date)+"'\n")
    print("   + File: '"+str(latest_collection_file)+"'\n")
    print("-"*5 + "\n")
    print("[LIBRE-AI] [REPORTING] -COLLECTION- [STATISTICS]: \n")
    extract_total_patterns_learned_from_local(memory)
    print("\n"+"-"*5 + "\n")
    print("[LIBRE-AI] [REPORTING] -ANALYSIS- [STATISTICS]: \n")
    print(" * Total [DNA SECUENCES]: [ "+str(total_genomes)+" ]\n")
    largest = 0
    largest_pattern_name = []
    largest_pattern_size = []
    for k, v in secuences_length_list.items():
        if int(v) > int(largest):
            largest = v
            largest_pattern_name.append(k)
            largest_pattern_size.append(largest)
    for p in largest_pattern_name:           
        largest_pattern_name = p
    for s in largest_pattern_size:
        largest_pattern_size = s
    print("   + [LARGEST] : "+str(largest_pattern_name)+ " [ "+str(largest_pattern_size)+" bp linear RNA ]")
    prev_shortest = None
    shortest_pattern_name = []
    shortest_pattern_size = []
    for k, v in secuences_length_list.items():
        if prev_shortest == None:
            shortest = v
            shortest_pattern_name.append(k)
            shortest_pattern_size.append(shortest)
            prev_shortest = True
        else:
            if int(v) < int(shortest):
                shortest = v
                shortest_pattern_name.append(k)
                shortest_pattern_size.append(shortest)
    for p in shortest_pattern_name:           
        shortest_pattern_name = p
    for s in shortest_pattern_size:
        shortest_pattern_size = s
    print("   + [SHORTEST]: "+str(shortest_pattern_name)+ " [ "+str(shortest_pattern_size)+" bp linear RNA ]\n")
    print(" * Total [NUCLEOTIDS]: [ "+str(num_total_nucleotids)+" ]\n")
    if nucleotid_more_present == total_adenine:
        print("   + [A] Adenine  : "+str(total_adenine)+" <- [MAX]")
    else:
        print("   + [A] Adenine  : "+str(total_adenine))
    if nucleotid_more_present == total_guanine:
        print("   + [G] Guanine  : "+str(total_guanine)+" <- [MAX]")
    else:
        print("   + [G] Guanine  : "+str(total_guanine))
    if nucleotid_more_present == total_cytosine:
        print("   + [C] Cytosine : "+str(total_cytosine)+" <- [MAX]")
    else:
        print("   + [C] Cytosine : "+str(total_cytosine))
    if nucleotid_more_present == total_thymine:
        print("   + [T] Thymine  : "+str(total_thymine)+" <- [MAX]")
    else:
        print("   + [T] Thymine  : "+str(total_thymine))
    if total_any > 0:
        if nucleotid_more_present == total_any:
            print("   + [N]  *ANY*   : "+str(total_any)+" <- [MAX]")
        else:
            print("   + [N]  *ANY*   : "+str(total_any))
    print("\n"+"-"*5 + "\n")
    extract_pattern_most_present_local(memory)
    plotATCG(total_adenine,total_guanine,total_cytosine,total_thymine)

def convert_memory_to_dict(memory): # [index] = genome_name, pattern, num_rep
    memory_dict = {}
    index = 0
    for m in memory:
        regex_record = "'(.+?)': (.+?), '(.+?)'" # regex magics! - extract first each record 
        pattern_record = re.compile(regex_record)
        record = re.findall(pattern_record, m)
        for r in record: # now extract each field
            index = index + 1
            name = str(r).split("', '(")[0]
            genome_name = str(name).split("'")[1]
            repeats = str(r).split("', '(")[1]
            genome_repeats = str(repeats).split("',")[0]
            pattern = str(repeats).split("',")[1]
            genome_pattern = pattern.replace(" ", "")
            genome_pattern = genome_pattern.replace("'", "")
            genome_pattern = genome_pattern.replace(")", "")  
            memory_dict[index] = genome_name, genome_pattern, genome_repeats # generate memory_dict!
    return memory_dict

def extract_pattern_most_present_local(memory):
    memory_dict = convert_memory_to_dict(memory)
    if genomes:
        try:
            f=open(dna_codons_list_path, 'r')
            codons =  f.readlines()
            f.close()
        except:
            pass
        print("[LIBRE-AI] [REPORTING] -RESEARCHING- [STATISTICS]: \n")
        total_genomes = 0
        for k, v in genomes.items():
            total_genomes = total_genomes + 1
        if memory_dict:
            total_patterns = 0
            for m in memory:
                total_patterns = total_patterns + 1 # counter used for known patterns
            max_size_pattern_name, less_size_pattern_name, biggest_pattern_name, biggest_pattern_size, smaller_pattern_name, smaller_pattern_size, total_patterns_all_genomes, most_present_patterns_by_len_list, less_present_patterns_by_len_list = extract_patterns_most_found_in_all_genomes(memory_dict)
            print(" * Searching -[ "+str(total_patterns)+" ]- [PATTERNS LEARNED!] in -[ "+str(total_genomes)+ " ]- [DNA SECUENCES]:")
            if total_patterns_all_genomes:
                print("\n   + Total [PATTERNS FOUND!]: [ "+str(total_patterns_all_genomes)+" ]")
                biggest_pattern_name_codon = None
                for c in codons:
                    if c.split(":")[0] == str(biggest_pattern_name):
                        biggest_pattern_name_codon = str(c.split(":")[1].replace("\n",""))
                        print("\n     - [MOST-PRESENT!]: [ "+str(biggest_pattern_size)+" ] time(s) -> [ "+str(biggest_pattern_name)+" ] "+str(biggest_pattern_name_codon)+"\n")
                if biggest_pattern_name_codon == None:
                        print("\n     - [MOST-PRESENT!]: [ "+str(biggest_pattern_size)+" ] time(s) -> [ "+str(biggest_pattern_name)+" ]\n")
                other_pattern_name_codon = None
                for k, v in most_present_patterns_by_len_list.items():
                    for c in codons:
                        if c.split(":")[0] == str(v[0]):
                            other_pattern_name_codon = str(c.split(":")[1].replace("\n",""))
                            print("       * [length = "+str(k)+"] : [ "+str(v[1])+" ] time(s) -> [ "+str(v[0])+" ] "+str(other_pattern_name_codon))
                    if other_pattern_name_codon == None:
                        print("       * [length = "+str(k)+"] : [ "+str(v[1])+" ] time(s) -> [ "+str(v[0])+" ]")
                    other_pattern_name_codon = None
                smaller_pattern_name_codon = None
                for c in codons:
                    if c.split(":")[0] == str(smaller_pattern_name):
                        smaller_pattern_name_codon = str(c.split(":")[1].replace("\n",""))
                        print("\n     - [LESS-PRESENT!]: [ "+str(smaller_pattern_size)+" ] time(s) -> [ "+str(smaller_pattern_name)+" ] "+str(smaller_pattern_name_codon)+"\n")
                if smaller_pattern_name_codon == None:
                    print("\n     - [LESS-PRESENT!]: [ "+str(smaller_pattern_size)+" ] time(s) -> [ "+str(smaller_pattern_name)+" ]\n")
                other_pattern_name_codon = None
                for n, m in less_present_patterns_by_len_list.items():
                    for c in codons:
                        if c.split(":")[0] == str(m[0]):
                            other_pattern_name_codon = str(c.split(":")[1].replace("\n",""))
                            print("       * [length = "+str(n)+"] : [ "+str(m[1])+" ] time(s) -> [ "+str(m[0])+" ] "+str(other_pattern_name_codon))
                    if other_pattern_name_codon == None:
                        print("       * [length = "+str(n)+"] : [ "+str(m[1])+" ] time(s) -> [ "+str(m[0])+" ]")
                    other_pattern_name_codon = None
                max_size_pattern_name =  max(most_present_patterns_by_len_list, key=most_present_patterns_by_len_list.get)
                less_size_pattern_name = min(most_present_patterns_by_len_list, key=most_present_patterns_by_len_list.get)
                print("\n     - [LARGEST] : [ "+str(max_size_pattern_name)+" ] bp linear RNA")
                print("     - [SHORTEST]: [ "+str(less_size_pattern_name)+" ] bp linear RNA\n")
            else:
                print("\n   + Total [PATTERNS FOUND!]: [ 0 ]\n")
        try:
            f=open(universal_primer_list_path, 'r')
            UPL =  f.readlines()
            f.close()
            if UPL:
                extract_potential_primer_pairs(UPL, total_genomes, codons)
        except:
            pass
        if codons:
            extract_potential_dna_codons(codons, total_genomes)

def extract_potential_primer_pairs(UPL, total_genomes, codons):
    total_universal_primer_pairs = 0
    total_primer_pairs_found = 0
    primer_pairs_found_list = {}
    for pp in UPL:
        total_universal_primer_pairs = total_universal_primer_pairs + 1
        for k, v in genomes.items():
            pair_name = pp.split(":")[1].upper().replace("\n","")
            pair_sec = pp.split(":")[0]
            if str(pair_name) in str(v.upper()):
                pair_times = v.count(pair_name)
                total_primer_pairs_found += pair_times
                primer_pairs_found_list[pair_sec] = pair_name, total_primer_pairs_found
    print(" "+"-"*5+"\n")
    print(" * Searching -[ "+str(total_universal_primer_pairs)+" ]- [UNIVERSAL PRIMER PAIRS!] in -[ "+str(total_genomes)+ " ]- [DNA SECUENCES]:")
    if total_primer_pairs_found:
        total_primer_pairs_found_list = 0
        for m, n in primer_pairs_found_list.items():
            total_primer_pairs_found_list = total_primer_pairs_found_list + n[1]
        print("\n   + Total [UNIVERSAL PRIMER PAIRS FOUND!]: [ "+str(total_primer_pairs_found_list)+" ]\n")
        for m, n in primer_pairs_found_list.items():
             print("       * "+str(m)+" -> [ "+str(n[0])+" ] : [ "+str(n[1])+" ] time(s)")
        print ("")
    else:
        print("\n   + Total [UNIVERSAL PRIMER PAIRS FOUND!]: [ 0 ]\n")
    print(" "+"-"*5+"\n")

def extract_potential_dna_codons(codons, total_genomes):
    total_codons = 0
    total_codons_found = 0
    codons_found_list = {}
    codons_found_list_by_codon = {}
    index = 0
    for c in codons:
        total_codons = total_codons + 1
        for k, v in genomes.items():
            codon_name = c.split(":")[0].upper().replace("\n","")
            if str(codon_name) in str(v.upper()):
                index = index + 1
                codons_times = v.count(codon_name)
                total_codons_found += codons_times
                codons_found_list[index] = codons_times, c.split(":")[0], str(c.split(":")[1]), k
    print(" * Searching -[ "+str(total_codons)+" ]- [AMINO ACIDS!] in -[ "+str(total_genomes)+ " ]- [DNA SECUENCES]:")
    if total_codons_found:
        for m, n in codons_found_list.items():
            codon_sec = str(n[1])
            codon_name = str(n[2].replace("\n",""))
            if not codon_sec in codons_found_list_by_codon.keys():
                codons_found_list_by_codon[codon_sec] = codon_name, m
            else:
                for r, s in codons_found_list_by_codon.items():
                    if codon_sec == r:
                        new_v = s[1] + m
                        codons_found_list_by_codon[codon_sec] = codon_name, new_v
        codons_found_list_by_name = {}
        for g,z in codons_found_list_by_codon.items():
            if not z[0] in codons_found_list_by_name.keys():
                codons_found_list_by_name[z[0]]= z[1]
            else:
                for e, q in codons_found_list_by_name.items():
                    if z[0] == e:
                        new_s = q + z[1]
                        codons_found_list_by_name[z[0]] = new_s
        total_codons_by_codon = 0
        for p, f in codons_found_list_by_name.items():
            total_codons_by_codon = total_codons_by_codon + f
        print("\n   + Total [AMINO ACIDS FOUND!]: [ "+str(total_codons_by_codon)+" ]\n")
        most_present_codons_found = max(codons_found_list_by_name, key=codons_found_list_by_name.get)
        less_present_codons_found = min(codons_found_list_by_name, key=codons_found_list_by_name.get)
        print("     - [MOST-PRESENT!]: "+str(most_present_codons_found))
        print("     - [LESS-PRESENT!]: "+str(less_present_codons_found)+"\n")
        for p, f in codons_found_list_by_name.items():
            print("       * "+str(p)+" : "+str(f)+" time(s)")
        print ("")
    else:
        print("\n   + Total [AMINO ACIDS FOUND!]: [ 0 ]\n")
    print(" "+"-"*5+"\n")
    if total_genomes > 0:
        extract_protein_secuence(total_genomes, codons_found_list, codons)

def extract_open_reading_frames(total_genomes):
    try:
        f=open(open_reading_frames_init_path, 'r')
        frames_init =  f.readlines()
        f.close()
    except:
        pass
    try:
        e=open(open_reading_frames_end_path, 'r')
        frames_end =  e.readlines()
        e.close()
    except:
        pass
    if frames_init and frames_end:
        print(" * Searching [OPEN READING FRAMES!] in -[ "+str(total_genomes)+ " ]- [DNA SECUENCES]:")
        total_opr_found = 0
        r_found_by_pattern = 0
        opr_found_list = {}
        index = 0
        for k, v in genomes.items():
            for opr_i in frames_init:
                opr_init_name = opr_i.replace("\n","")
                if str(opr_init_name) in str(v.upper()): # open reading INIT frame found!
                    for opr_e in frames_end:
                        opr_end_name = opr_e.replace("\n","")
                        if str(opr_end_name) in str(v.upper()): # open reading END frame found!
                            regex_opr = str(opr_init_name) +"(.+?)"+str(opr_end_name) # regex magics! - extract secuence between ocr_i and ocr_e
                            pattern_record = re.compile(regex_opr)
                            record = re.findall(pattern_record, str(v.upper()))
                            for r in record: # now extract each field
                                total_opr_found = total_opr_found + 1
                                r_found_by_pattern = v.count(opr_init_name+r+opr_end_name)
                                index = index + 1
                                opr_found_list[index] = k, r_found_by_pattern, opr_init_name, r, opr_end_name # [index]: genome, num_times, opr_i, pattern, opr_e
        if total_opr_found > 0:                     
            print("\n   + Total [OPEN READING FRAMES FOUND!]: [ "+str(total_opr_found)+" ]\n")
            most_present_opr_found = max(opr_found_list, key=opr_found_list.get)
            largest_pattern = 0
            largest_pattern_found = None
            for m, n in opr_found_list.items():
                opr_found_init = str(n[2])
                opr_found_pattern = str(n[3])
                opr_found_end = str(n[4])
                opr_found_times = str(n[1])
                opr_found_genome = str(n[0])
                opr_found_pattern_len = len(opr_found_pattern)
                if opr_found_pattern_len > largest_pattern:
                    largest_pattern = opr_found_pattern_len
                    largest_pattern_found = opr_found_init, opr_found_pattern, opr_found_end, opr_found_genome
                if m == most_present_opr_found: 
                    most_present_opr_found_init = str(n[2])
                    most_present_opr_found_pattern = str(n[3])
                    most_present_opr_found_end = str(n[4])
                    most_present_opr_found_times = str(n[1])
                    most_present_opr_found_genome = str(n[0])
            print("     - [MOST-PRESENT!]: [ "+str(most_present_opr_found_times)+" ] time(s) found in [ "+str(most_present_opr_found_genome)+" ] is -> [ "+str(most_present_opr_found_init)+"-{?}-"+str(most_present_opr_found_end)+" ]:\n")
            print(str("       * "+str(most_present_opr_found_init+most_present_opr_found_pattern+most_present_opr_found_end)))
            print("\n     - [LARGEST]: [ "+str(len(largest_pattern_found[1]))+" bp linear RNA ] found in [ "+str(largest_pattern_found[3])+" ] is -> [ "+str(largest_pattern_found[0])+"-{?}-"+str(largest_pattern_found[2])+" ]:\n")
            print(str("       * "+str(largest_pattern_found[0]+largest_pattern_found[1]+largest_pattern_found[2])+"\n"))
        else:
            print("\n   + Total [OPEN READING FRAMES FOUND!]: [ 0 ]\n")
    else:
        print("\n   + Total [OPEN READING FRAMES FOUND!]: [ 0 ]\n")
    
def extract_protein_secuence(total_genomes, codons_found_list, codons):
    print(" * Searching [PROTEINS!] in -[ "+str(total_genomes)+ " ]- [DNA SECUENCES]:\n")
    total_protein_secuences_found = 0
    protein_secuences_list = {}
    index = 0
    p = {}
    for c in codons:
        codon_sec = c.split(":")[0]
        codon_name = c.split(":")[1].replace("\n","")
        p[codon_sec] = codon_name
    for k, v in genomes.items():
        ps = ""
        dna = str(v)
        for i in range(0, len(dna)-(3+len(dna)%3), 3): # searching protein secuence
            if "Stop" in p[dna[i:i+3]]:
                break
            ps += p[dna[i:i+3]].split("(")[1].split(")")[0]
        index = index + 1
        total_protein_secuences_found = total_protein_secuences_found + 1
        protein_secuences_list[index] = ps, k
        ps = "" # clean protein secuence
    if total_protein_secuences_found > 0:
        protein_most_present = {}
        for value in protein_secuences_list.values(): 
            if value[0] in protein_most_present.keys():
                protein_most_present[value[0]] = protein_most_present[value[0]] + 1
            else:
                protein_most_present[value[0]] = 1
        most_present_protein_found = max(protein_most_present, key=protein_most_present.get)
        print("   + Total [PROTEINS FOUND!]: [ "+str(total_protein_secuences_found)+" ]\n")
        largest_protein_secuence = 0
        largest_protein_secuence_found = None
        most_present_protein_found_counter = 0
        for m, n in protein_secuences_list.items():
            if most_present_protein_found == n[0]:
                most_present_protein_found_counter = most_present_protein_found_counter + 1
            protein_secuence_pattern_len = len(str(n[0]))
            if protein_secuence_pattern_len > largest_protein_secuence:
                largest_protein_secuence = protein_secuence_pattern_len
                largest_protein_secuence_found = m, n
        print("     - [MOST-PRESENT!]: [ "+str(most_present_protein_found_counter)+" ] time(s) is -> [ "+str(most_present_protein_found)+" ]\n")
        protein_chemical_formula = ""
        f = open(protein_formula_path, "r")
        formulas = f.readlines()
        f.close()
        for a in most_present_protein_found:
            for f in formulas:
                if a == f.split(":")[0]:
                    protein_chemical_formula += str(f.split(":")[1].replace("\n","")+"+")
        pcfl = len(protein_chemical_formula)
        protein_chemical_final_formula =  protein_chemical_formula[:pcfl-1].translate(SUB)
        print("       *", protein_chemical_final_formula+"\n") 
        print("     - [LARGEST]: [ "+str(len(largest_protein_secuence_found[1][0]))+" bp linear RNA ] found in [ "+str(largest_protein_secuence_found[1][1])+" ] is -> [ "+str(largest_protein_secuence_found[1][0])+" ]\n")
        largest_protein_chemical_formula = ""
        for a in largest_protein_secuence_found[1][0]:
            for f in formulas:
                if a == f.split(":")[0]:
                    largest_protein_chemical_formula += str(f.split(":")[1].replace("\n","")+"+")
        pcfl = len(largest_protein_chemical_formula)
        largest_protein_chemical_final_formula = largest_protein_chemical_formula[:pcfl-1].translate(SUB)
        print("       *", largest_protein_chemical_final_formula+"\n")             
    else:
        print("\n   + Total [PROTEINS FOUND!]: [ 0 ]\n")
    print(" "+"-"*5+"\n")
    if codons_found_list:
        extract_open_reading_frames(total_genomes)

def extract_patterns_most_found_in_all_genomes(memory_dict):
    present_patterns = []
    for m, p in memory_dict.items():
        pattern = p[1]
        if pattern not in present_patterns:
            present_patterns.append(pattern)
    index = 0 # genome num index
    for pattern in present_patterns:
        index = index + 1
        try_pattern_against_all_genomes_by_pattern(pattern, index)
    total_patterns_all_genomes = 0
    largest_size_by_pattern = {}
    largest_size_by_pattern_index = 0
    for k,v in repeats.items():
        largest_size_by_pattern_index = largest_size_by_pattern_index + 1
        largest_size_by_pattern[largest_size_by_pattern_index] = v[0], v[2]
    total_patterns_by_pattern = 0
    list_total_patterns_by_pattern = {}
    for i, v in largest_size_by_pattern.items():
        total_patterns_by_pattern = total_patterns_by_pattern + v[1]
        list_total_patterns_by_pattern[v[0]] = total_patterns_by_pattern
    biggest_pattern_name = None
    biggest_pattern_size = 0
    smaller_pattern_name = None
    smaller_pattern_size = 0
    max_size_pattern = 0
    for r, z in list_total_patterns_by_pattern.items():
        total_patterns_all_genomes = total_patterns_all_genomes + z
        pattern_length = len(r)
        if pattern_length > max_size_pattern:
           max_size_pattern_name = r
        if biggest_pattern_name == None:
           biggest_pattern_name = r
           smaller_pattern_name = r
           biggest_pattern_size = z
           smaller_pattern_size = z
           less_size_pattern_name = r
           less_size_pattern_size = z
        else:
           if pattern_length < less_size_pattern_size:
               less_size_pattern_size = pattern_length
               less_size_pattern_name = r
           if z > biggest_pattern_size:
               biggest_pattern_name = r
               biggest_pattern_size = z
           else:
               if z < smaller_pattern_size:
                   smaller_pattern_name = r
                   smaller_pattern_size = z
    most_present_patterns_by_len_list = extract_most_present_pattern_by_len(list_total_patterns_by_pattern)
    less_present_patterns_by_len_list = extract_less_present_pattern_by_len(list_total_patterns_by_pattern)
    return max_size_pattern_name, less_size_pattern_name, biggest_pattern_name, biggest_pattern_size, smaller_pattern_name, smaller_pattern_size, total_patterns_all_genomes, most_present_patterns_by_len_list, less_present_patterns_by_len_list

def extract_most_present_pattern_by_len(list_total_patterns_by_pattern):
    most_present_patterns_by_len_list = {}
    for k, v in list_total_patterns_by_pattern.items():
        pattern_len = len(k)
        if pattern_len in most_present_patterns_by_len_list.keys():
            if v > most_present_patterns_by_len_list[pattern_len][1]:
                most_present_patterns_by_len_list[pattern_len] = k, v
        else:
            most_present_patterns_by_len_list[pattern_len] = k, v
    return most_present_patterns_by_len_list

def extract_less_present_pattern_by_len(list_total_patterns_by_pattern):
    less_present_patterns_by_len_list = {}
    for k, v in list_total_patterns_by_pattern.items():
        pattern_len = len(k)
        if pattern_len in less_present_patterns_by_len_list.keys():
            if v < less_present_patterns_by_len_list[pattern_len][1]:
                less_present_patterns_by_len_list[pattern_len] = k, v
        else:
            less_present_patterns_by_len_list[pattern_len] = k, v
    return less_present_patterns_by_len_list

def extract_storage_sizes():
    total_dataset_size = 0
    total_files_size = 0
    total_list_size = 0
    for file in glob.iglob(genomes_path + '*/*/*', recursive=True): # extract datasets sizes
        if(file.endswith(".genome")):
            total_dataset_size = total_dataset_size + len(file)
        try:
            f=open(brain_path, "r") # extract brain sizes
            total_brain_size = len(f.read())
            f.close()
        except:
            total_brain_size = 0
        try:
            f=open(genomes_list_path, "r") # extract genomes list sizes
            total_list_size = len(f.read())
            f.close()
        except:
            total_list_size = 0
    if total_dataset_size > 0:
        total_files_size = int(total_files_size) + int(total_dataset_size)
        dataset_s, dataset_size_name = convert_size(total_dataset_size)
        total_dataset_size = '%s %s' % (dataset_s,dataset_size_name)
    if total_brain_size > 0:
        total_files_size = int(total_files_size) + int(total_brain_size)
        brain_s, brain_size_name = convert_size(total_brain_size)
        total_brain_size = '%s %s' % (brain_s,brain_size_name)
    if total_list_size > 0:
        total_files_size = int(total_files_size) + int(total_list_size)
        list_s, list_size_name = convert_size(total_list_size)
        total_list_size = '%s %s' % (list_s,list_size_name)
    total_s, total_size_name = convert_size(total_files_size)
    total_files_size = '%s %s' % (total_s,total_size_name)
    print(" * Total [FILE SIZES]: "+str(total_files_size)+"\n")
    if total_dataset_size:
        print("   + [DATASET]: "+str(total_dataset_size)+"\n")
    if total_list_size:
        print("   + [LIST]: "+str(total_list_size)+"\n")
    if total_brain_size:
        print("   + [BRAIN]: "+str(total_brain_size)+"\n")

def extract_total_patterns_learned_from_local(memory):
    total_patterns = 0
    for m in memory:
        total_patterns = total_patterns + 1
    print(" * [SETTINGS] Using [MAX. LENGTH] for range [PATTERN] = [ "+str(max_length)+" ]\n")
    if total_patterns > 0:
        print("   + [PATTERNS LEARNED!]: [ "+str(total_patterns)+" ]\n")
    else:
        print("   + [PATTERNS LEARNED!]: [ "+str(total_patterns)+" ]")
    generate_pattern_len_report_structure(memory)
    return memory

def list_genomes_on_database():
    print("[LIST] [REPORTING] [DNA SECUENCES] ... -> [STARTING!]\n")
    f=open(dna_codons_list_path, 'r')
    codons =  f.readlines()
    f.close()
    print("-"*15 + "\n")
    f=open(open_reading_frames_init_path, 'r')
    frames_init =  f.readlines()
    f.close()
    f=open(open_reading_frames_end_path, 'r')
    frames_end =  f.readlines()
    f.close()
    f = open(protein_formula_path, "r")
    formulas = f.readlines()
    f.close()
    f=open(genomes_list_path, 'w')
    p = {}
    for k, v in genomes.items():
        total_protein_secuences_found = 0
        print ("="*20+"\n")
        f.write(str("="*20+"\n\n"))
        print ("* "+str(k))
        print ("\n  + Total [NUCLEOTIDS FOUND!]: [ "+str(len(v)-1)+" bp linear RNA ]\n")
        print ("    - [A] Adenine  :", str(v.count("A")))
        print ("    - [G] Guanine  :", str(v.count("G")))
        print ("    - [C] Cytosine :", str(v.count("C")))
        print ("    - [T] Thymine  :", str(v.count("T")))
        f.write(str("* "+str(k)+"\n"))
        f.write(str("\n  + Total [NUCLEOTIDS FOUND!]: [ "+str(len(v)-1)+" bp linear RNA ]\n"))
        f.write(str("    - [A] Adenine  : " + str(v.count("A"))+"\n"))
        f.write(str("    - [G] Guanine  : " + str(v.count("G"))+"\n"))
        f.write(str("    - [C] Cytosine : " + str(v.count("C"))+"\n"))
        f.write(str("    - [T] Thymine  : " + str(v.count("T"))+"\n"))
        if v.count("N") > 0:
            print ("    - [N]  *ANY*   :", str(v.count("N")))
            f.write(str("    - [N]  *ANY*   : "+ str(v.count("N"))+"\n"))
        total_codons = 0
        for c in codons:
            codon_counter = v.count(str(c.split(":")[0]))
            total_codons = total_codons + codon_counter
            codon_sec = c.split(":")[0]
            codon_name = c.split(":")[1].replace("\n","")
            p[codon_sec] = codon_name
        print ("\n  + Total [AMINO ACIDS FOUND!]: [ "+str(total_codons)+" ]\n")
        f.write(str("\n  + Total [AMINO ACIDS FOUND!]: [ "+str(total_codons)+" ]\n"))
        for c in codons:
            codon_sec = str(c.split(":")[0])
            codon_name = str(c.split(":")[1].replace("\n",""))
            codon_counter = str(v.count(str(c.split(":")[0])))
            print ("    - ["+codon_sec+"] "+codon_name+" :", codon_counter)
            f.write(str("    - ["+codon_sec+"] "+codon_name+" : "+ codon_counter)+"\n")
        ps = ""
        dna = str(v)
        for i in range(0, len(dna)-(3+len(dna)%3), 3): # searching protein secuence
            if "Stop" in p[dna[i:i+3]]:
                break
            ps += p[dna[i:i+3]].split("(")[1].split(")")[0]
        total_protein_secuences_found = total_protein_secuences_found + 1
        print ("\n  + Total [PROTEINS FOUND!]: [ "+str(total_protein_secuences_found)+" ]\n")
        f.write(str("\n  + Total [PROTEINS FOUND!]: [ "+str(total_protein_secuences_found)+" ]\n"))
        protein_chemical_formula = ""
        for a in ps:
            for formula in formulas:
                if a == formula.split(":")[0]:
                    protein_chemical_formula += str(formula.split(":")[1].replace("\n","")+"+")
        pcfl = len(protein_chemical_formula)
        protein_chemical_final_formula = protein_chemical_formula[:pcfl-1].translate(SUB)
        print ("    - ["+ps+"] : "+protein_chemical_final_formula)
        f.write(str("    - ["+ps+"] : "+protein_chemical_final_formula)+"\n")
        ps = "" # clean protein secuence
        if frames_init and frames_end:
            total_opr_found = 0
            r_found_by_pattern = 0
            opr_found_list = {}
            index = 0
            for opr_i in frames_init:
                opr_init_name = opr_i.replace("\n","")
                if str(opr_init_name) in str(v.upper()): # open reading INIT frame found!
                    for opr_e in frames_end:
                        opr_end_name = opr_e.replace("\n","")
                        if str(opr_end_name) in str(v.upper()): # open reading END frame found!
                            regex_opr = str(opr_init_name) +"(.+?)"+str(opr_end_name) # regex magics! - extract secuence between ocr_i and ocr_e
                            pattern_record = re.compile(regex_opr)
                            record = re.findall(pattern_record, str(v.upper()))
                            for r in record: # now extract each field
                                total_opr_found = total_opr_found + 1
                                r_found_by_pattern = v.count(opr_init_name+r+opr_end_name)
                                index = index + 1
                                opr_found_list[index] = k, r_found_by_pattern, opr_init_name, r, opr_end_name # [index]: genome, num_times, opr_i, pattern, opr_e
            print ("\n  + Total [OPEN READING FRAMES FOUND!]: [ "+str(total_opr_found)+" ]")
            f.write(str("\n  + Total [OPEN READING FRAMES FOUND!]: [ "+str(total_opr_found)+" ] \n"))
            for m, n in opr_found_list.items():
                #print("    - ["+str(n[2])+str(n[3])+str(n[4])+"] : [ "+str(n[1])+" ] time(s)")
                f.write(str("    - ["+str(n[2])+str(n[3])+str(n[4])+"] : "+ str(n[1]))+"\n")
        print ("")
        f.write("\n")
    print("-"*15 + "\n")
    print ("[LIST] [INFO] [SAVED!] at: '"+str(genomes_list_path)+"'... -> [EXITING!]\n")
    f.close()

def examine_stored_brain_memory():
    memory = [] # list used as hot-memory
    f=open(brain_path, 'r')
    for line in f.readlines():
        if line not in memory:
            memory.append(line)
    f.close()
    if memory == "": # first time run!
        print ("[LIBRE-AI] [INFO] Not any [BRAIN] present ... -> [BUILDING ONE!]\n")
        print("-"*15 + "\n")
        for i in range(2, 11+1):
            seed = [random.randrange(0, 4) for _ in range(i)] # generate "static" genesis seed
            if seed not in seeds_checked:
                seeds_checked.append(seed)
                pattern = ""
                for n in seed:
                    if n == 0:
                        pattern += "A"
                    elif n == 1:
                        pattern += "C"
                    elif n == 2:
                        pattern += "T"
                    else:
                        pattern += "G"
                print("[LIBRE-AI] [SEARCH] Generating [RANDOM] pattern: " + str(pattern) + "\n")
                create_new_pattern(pattern) # create new pattern
        print("-"*15 + "\n")
        print ("[LIBRE-AI] [INFO] A new [BRAIN] has been created !!! ... -> [ADVANCING!]\n")
        f=open(brain_path, 'r')
        memory = f.read().replace('\n',' ')
        f.close()
    return memory
def generate_pattern_len_report_structure(memory):
    pattern_len_data = []# related with [MAX. LENGTH] range
    pattern_len_quantity = 50
    for i in range(pattern_len_quantity):
        pattern_len_data.append(0)
    for m in memory:
        try:
            pattern_len = m.split(", '")[1]
            pattern_len = pattern_len.split("')")[0]
            pattern_len = len(pattern_len)
        except:
            pattern_len = 0 # discard!
        for i in range(pattern_len_quantity):
            if pattern_len_data[i] == i:
                pattern_len_data[i] = pattern_len_data[i] + 1
            else:
                pass
    for i in range(pattern_len_quantity):
        if pattern_len_data[i] > 0:
            print("     - [length = "+str(i)+"] : [ "+str(pattern_len_data[i])+" ]") 

def plotATCG(total_adenine,total_guanine,total_cytosine,total_thymine):
    plot_limit = 100
    total = total_adenine + total_guanine + total_cytosine + total_thymine
    percentage_adenine = round((total_adenine/total)*plot_limit,5)
    percentage_guanine = round((total_guanine/total)*plot_limit,5)
    percentage_cytosine = round((total_cytosine/total)*plot_limit,5)
    percentage_thymine = round((total_thymine/total)*plot_limit,5)
    adenine_text_position = percentage_adenine/2
    guanine_text_position = percentage_guanine/2
    cytosine_text_position = percentage_cytosine/2
    thymine_text_position = percentage_thymine/2
    figure = plt.figure()
    subplot = figure.add_subplot(aspect='equal')
    subplot.add_patch(patches.Rectangle((plot_limit/2-percentage_adenine, plot_limit/2), percentage_adenine, percentage_adenine,fc="pink"))
    subplot.text(plot_limit/2-percentage_adenine+adenine_text_position, plot_limit/2+adenine_text_position,"adenine "+str(percentage_adenine)+"%",horizontalalignment='center', fontsize=adenine_text_position)
    subplot.add_patch(patches.Rectangle((plot_limit/2-percentage_guanine,plot_limit/2-percentage_guanine), percentage_guanine, percentage_guanine,fc="cyan"))
    subplot.text(plot_limit/2-percentage_guanine+guanine_text_position,plot_limit/2-percentage_guanine+guanine_text_position,"guanine "+str(percentage_guanine)+"%",horizontalalignment='center', fontsize=guanine_text_position)
    subplot.add_patch(patches.Rectangle((plot_limit/2,plot_limit/2), percentage_cytosine, percentage_cytosine,fc="gray"))
    subplot.text(plot_limit/2+cytosine_text_position,plot_limit/2+cytosine_text_position,"cytosine "+str(percentage_cytosine)+"%",horizontalalignment='center', fontsize=cytosine_text_position)
    subplot.add_patch(patches.Rectangle((plot_limit/2,plot_limit/2-percentage_thymine), percentage_thymine, percentage_thymine,fc="orange"))
    subplot.text(plot_limit/2+thymine_text_position,plot_limit/2-percentage_thymine+thymine_text_position,"thymine "+str(percentage_thymine)+"%",horizontalalignment='center', fontsize=thymine_text_position)
    plt.ylim((0,plot_limit))
    plt.xlim((0,plot_limit))
    plt.show()

def print_banner():
    print("\n"+"="*50)
    print(" ____  _       _   _    _     ")
    print("|  _ \(_) __ _| \ | |  / \    ")
    print("| | | | |/ _` |  \| | / _ \   ")
    print("| |_| | | (_| | |\  |/ ___ \  ")
    print("|____/|_|\__,_|_| \_/_/   \_\ by psy")
    print('\n"Search and Recognize patterns in DNA sequences"')
    print("\n"+"="*50)
    print("+ GENOMES DETECTED:", str(num_files))
    print("="*50)
    print("\n"+"-"*15+"\n")
    print(" * VERSION: ")
    print("   + "+VERSION+" - (rev:"+RELEASE+")")
    print("\n * SOURCES:")
    print("   + "+SOURCE1)
    print("   + "+SOURCE2)
    print("\n * CONTACT: ")
    print("   + "+CONTACT+"\n")
    print("-"*15+"\n")
    print("="*50)

# sub_init #
num_files=0
for file in glob.iglob(genomes_path + '**/*', recursive=True):
    if(file.endswith(".genome")): 
        num_files = num_files + 1
        f=open(file, 'r')  
        genome =  f.read().replace('\n',' ')
        genomes[file.replace("datasets/","")] = genome.upper() # add genome to main dict
        f.close()
print_banner() # show banner
option = input("\n+ CHOOSE: (S)earch, (L)ist, (T)rain or (R)eport: ").upper()
print("")
print("="*50+"\n")
if option == "S": # search pattern
    search_pattern_with_human()
elif option == "L": # list genomes
    list_genomes_on_database()
elif option == "T": # teach AI
    teach_ai()
else: # libre AI
    libre_ai()
print ("="*50+"\n")
