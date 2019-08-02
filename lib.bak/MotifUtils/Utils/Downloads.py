def MotifSetToMEME(MSO):
    #fname = #set random/logical path, maybe include name as a param
    #get_object_params = {} #grab motifset object

    #Initiliaze meme format
   #fname = #set random/logical path, maybe include name as a param
    #get_object_params = {} #grab motifset object

    #Initiliaze meme format
    MEMEText = 'MEME version 4\n\n'
    sortedAlph = sorted(MSO['Alphabet'])
    alphStr = ''.join(sortedAlph)
    MEMEText += alphStr + '\n'
    MEMEText += '\n'
    MEMEText += 'strands: + -\n\n'
    MEMEText += 'Background letter frequencies\n'
    for letter in sortedAlph:
        MEMEText += letter + ' ' + str(MSO['Background'][letter]) + ' '
    MEMEText += '\n\n'

    for motif in MSO['Motifs']:
        MEMEText += 'MOTIF ' + motif['Iupac_sequence'] + '\n'
        MEMEText += 'letter-probability matrix: alength= 4 w= '
        MEMEText += str(len(motif['Iupac_sequence'])) + ' nsites= '
        if motif['Motif_Locations'] is not None:
            MEMEText += str(len(motif['Motif_Locations']))
        else:
            MEMEText += '0'
        MEMEText += ' E= 0.0\n'
        #TODO: PVAL! -> ADD TO MSO -> PARSE IT HERE
        #MEMEText +=
        #print(len(motif['Iupac_sequence']))
        #print(len(motif['PWM']['T']))
        #exit()
        for i in range(0,len(motif['Iupac_sequence'])):
            for letter in sortedAlph:
                #print(i)
                try:
                    MEMEText += str(motif['PWM'][letter][i]) + ' '
                except IndexError:
                    print(len(motif['Iupac_sequence']))
                    print(len(motif['PWM'][letter]))
                    print(letter)
            MEMEText += '\n'
        MEMEText += '\n'
    return MEMEText
