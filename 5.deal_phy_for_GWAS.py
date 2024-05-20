import glob
import os

fs = glob.glob("C:/laboratory_files/942份谷子材料表型/*.txt")

for files in fs:
    print(files)
    traits = []
    dic = {}
    file = open(files)
    for line in file:
        if line.startswith("Sample"):
            _line = line.rstrip().split('\t')
            traits += _line[0:]
        else:
            _line = line.rstrip().split('\t')
            if _line[0] not in dic:
                dic[_line[0]] = []
            dic[_line[0]] += _line[1:]

    for i, v in enumerate(traits[1:]):
        _v = v.replace('|', '_')
        out = open(f"C:/laboratory_files/942份谷子材料表型/deal_for_GWAS/{_v}.txt", 'w')
        for k in dic.keys():
            value = dic[k]
            out.write(k + '\t' + k + '\t' + value[i] + '\n')

        out.close()
    file.close()
