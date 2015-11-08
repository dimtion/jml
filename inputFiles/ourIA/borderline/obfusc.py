import codecs

# 32 : espace de base
# 128
# 148 : Annulation du caractède précédant
# 160 : espace insécable
# 173 : trait d'union conditionnel
dangerous_file = codecs.open("le_mechant_truc.py", "r", "utf-8-sig")

# First : generate the obfuscated code :
m = (str(bin(ord(i)))[2:] for i in dangerous_file.read())
m = ''.join('0'*(8 - len(x)) + x for x in m)
obfucated_code = ''.join(chr(160) if x == '0' else chr(128) for x in m)

safe_file = codecs.open("le_truc.py", "r", "utf-8-sig")

# Aptent 1 : put everything in the first line of the safe code :
docstring_cut = safe_file.read().split('"""')
every_line = [l for i in range(1, len(docstring_cut), 2) for l in docstring_cut[i].split('\n')]
size_batch = len(obfucated_code) // (len(every_line) - len(docstring_cut) // 2)

for i in range(1, len(docstring_cut), 2):
    line_cut = docstring_cut[i].split('\n')
    for j in range(len(line_cut) - 1):
        line_cut[j] = line_cut[j] + obfucated_code[size_batch * (i + j): size_batch * (i+j+1)]
    # IamHERE
    docstring_cut[i] = '\n'.join(line_cut)

regonisied = '"""'.join(docstring_cut)

final_file = codecs.open("le_truc_final.py", "w", "utf-8-sig")
final_file.write(regonisied)

final_file.close()
safe_file.close()
dangerous_file.close()

import le_truc_final
