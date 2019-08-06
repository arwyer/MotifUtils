from copy import deepcopy
import os
from installed_clients.GenomeFileUtilClient import GenomeFileUtil
from installed_clients.DataFileUtilClient import DataFileUtil
from installed_clients.SequenceSetUtilsClient import SequenceSetUtils


class MotifUtil:
    def __init__(self, config):
        self.scratch = config['scratch']
        self.GFU = GenomeFileUtil(os.environ['SDK_CALLBACK_URL'])
        self.DFU = DataFileUtil(os.environ['SDK_CALLBACK_URL'])
        self.SSU = SequenceSetUtils(os.environ['SDK_CALLBACK_URL'])

    def build_sequence_fasta(self, params):
        self.seq_file = self.SSU.SeqSetToFasta({
            'ws_name': params['ws_name'],
            'SS_ref': params['seq_set_ref']
        })['path']

        if not os.path.exists(self.seq_file):
            raise FileNotFoundError(f'Sequence file: {self.seq_file} does not exist')

        return True

    def parse_motif_list(self, motiflist, params):
        self.build_sequence_fasta(params)
        MSO = {}

        MSO['Background'] = self.GetBackground(self.seq_file)

        MSO['Condition'] = 'Temp'
        MSO['SequenceSet_ref'] = params['seq_set_ref']
        MSO['Motifs'] = []
        MSO['Alphabet'] = ['A', 'C', 'G', 'T']

        for motif in motiflist:
            MSO['Motifs'].append(deepcopy(self.ConvertMotif(motif, MSO, self.seq_file)))

        return MSO

    def GetBackground(self, seqfile):
        count = 0
        sfile = open(seqfile)
        FreqDict = {'A': 0, 'G': 0, 'C': 0, 'T': 0}
        for line in sfile:
            if '> ' not in line and line != '\n':
                FreqDict['A'] += line.count('A')
                FreqDict['C'] += line.count('C')
                FreqDict['G'] += line.count('G')
                FreqDict['T'] += line.count('T')
            count += 1
        total = FreqDict['A'] + FreqDict['C'] + FreqDict['G'] + FreqDict['T']
        Background = {}

        Background['A'] = float(FreqDict['A']) / total
        Background['C'] = float(FreqDict['C']) / total
        Background['G'] = float(FreqDict['G']) / total
        Background['T'] = float(FreqDict['T']) / total

        return Background

    def BuildSetDict(self, seqfile):
        sfile = open(seqfile)
        seqDict = {}
        id = ''
        for line in sfile:
            if '> ' in line:
                id = line.replace('\n', '').replace('>', '').strip()
            elif line == '\n':
                pass
            else:
                seqDict[id] = line.replace('\n', '')
        return seqDict

    def ConvertMotif(self, motif, MotifSet, seqfile):
        newMotif = {}
        newMotif['Motif_Locations'] = []
        SeqDict = self.BuildSetDict(seqfile)
        for loc in motif['Locations']:
            new_loc = {}
            # new_loc['Feature_id'] = loc[0]
            new_loc['sequence_id'] = loc[0]
            new_loc['start'] = int(loc[1])
            new_loc['end'] = int(loc[2])
            new_loc['orientation'] = loc[3]
            new_loc['sequence'] = self.ExtractSequence(int(loc[1]), int(loc[2]), loc[3], loc[0], SeqDict)
            new_loc['sequence'] = ''
            newMotif['Motif_Locations'].append(new_loc.copy())
        newMotif['Iupac_sequence'] = motif['Iupac_signature']
        newMotif['PWM'] = {}
        newMotif['PFM'] = {}

        for letter in MotifSet['Alphabet']:
            newMotif['PWM'][letter] = []
            newMotif['PFM'][letter] = []
        for row in motif['pwm']:
            for pair in row:
                newMotif['PWM'][pair[0]].append(pair[1])

        return newMotif

    def ExtractSequence(self, start, end, orientation, id, SeqDict):
        complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A', 'N': 'N'}
        if orientation == '+':
            return SeqDict[id][start:end]
        else:
            tempseq = SeqDict[id][start:end]
            newSeq = ''
            for b in tempseq:
                newSeq += complement[b]
            newSeq = newSeq[::-1]
            return newSeq

        pass
