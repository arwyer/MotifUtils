from copy import deepcopy

def GetBackground():
    seqfile = '/kb/module/work/tmp/SeqSet.fa'
    count = 0
    sfile = open(seqfile)
    FreqDict = {'A':0,'G':0,'C':0,'T':0}
    for line in sfile:
        print(line)
        if count%2 == 1:
            FreqDict['A'] += line.count('A')
            FreqDict['C'] += line.count('C')
            FreqDict['G'] += line.count('G')
            FreqDict['T'] += line.count('T')
        count += 1
    total = FreqDict['A'] + FreqDict['C'] + FreqDict['G'] + FreqDict['T']
    Background = {}

    Background['A'] = float(FreqDict['A'])/total
    Background['C'] = float(FreqDict['C'])/total
    Background['G'] = float(FreqDict['G'])/total
    Background['T'] = float(FreqDict['T'])/total

    return Background

def CheckLength(motifset, min, max):
    topop = []
    for i,motif in enumerate(motifset['Motifs']):
        if len(motif['Iupac_sequence']) < min or len(motif['Iupac_sequence']) > max:
            topop.append(i)
    topop.sort(reverse=True)
    for p in topop:
        motifset['Motifs'].pop(p)


#TODO: extract sequence from output files, add to motif object
def BuildSetDict():
    seqfile = '/kb/module/work/tmp/SeqSet.fa'
    count = 0
    sfile = open(seqfile)
    seqDict = {}
    id = ''
    for line in sfile:
        if count%2 == 0:
            id = line.replace('\n','').replace('>','')
        else:
            seqDict[id] = line.replace('\n','')
        count += 1
    return seqDict

def ExtractSequence(start,end,orientation,id,SeqDict):
    complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A','N':'N'}
    if orientation == '+':
        print(id)
        print(SeqDict[id])
        return SeqDict[id][start:end]
    else:
        tempseq = SeqDict[id][start:end]
        newSeq = ''
        for b in tempseq:
            newSeq += complement[b]
        newSeq = newSeq[::-1]
        return newSeq


def ConvertMotif(motif,MotifSet):
    newMotif = {}
    newMotif['Motif_Locations'] = []
    SeqDict = BuildSetDict()
    for loc in motif['Locations']:
        new_loc = {}
        #new_loc['Feature_id'] = loc[0]
        new_loc['sequence_id'] = loc[0]
        new_loc['start'] = int(loc[1])
        new_loc['end'] = int(loc[2])
        new_loc['orientation'] = loc[3]
        new_loc['sequence']= ExtractSequence(int(loc[1]),int(loc[2]),loc[3],loc[0],SeqDict)
        newMotif['Motif_Locations'].append(new_loc.copy())
    newMotif['Iupac_sequence'] = motif['Iupac_signature']
    newMotif['PWM'] = {}
    newMotif['PFM'] = {}

    for letter in MotifSet['Alphabet']:
        newMotif['PWM'][letter] = []
        newMotif['PFM'][letter] = []
    if len(motif['pwm']) != len(motif['Iupac_signature']):
        print('LENGTH MISMATCH ORIGINAL')
    for row in motif['pwm']:
        for pair in row:
            newMotif['PWM'][pair[0]].append(pair[1])
    if len(newMotif['PWM']['A']) != len(newMotif['Iupac_sequence']):
        print('LENGTH MISMATCH NEW')
    return newMotif

def parseMotifList(MotifList, MotifSet):
    for motif in MotifList:
        MotifSet['Motifs'].append(deepcopy(ConvertMotif(motif,MotifSet)))
