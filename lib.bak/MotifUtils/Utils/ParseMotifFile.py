import GibbsUtil as GU
import HomerUtil as HU
import MemeUtil as MU
import MotifSetUtil as MSU

def BuildMotifSetFromFile(format,path,location,dump):
    supportedFormats = ['gibbs','homer','meme','jaspar']

    valid = False
    for s in supportedFormats:
        if s.lower() = format.lower():
            valid = True
    if not valid:
        print('Format %s is not supported' % (format))
        formatStr = ' '.join(supportedFormats)
        print('Supported formats are: %s' % (formatStr))
        exit()

    try:
        #Meme is simple, 1 file with all motifs
        #Homer is a little more complicated- 1 file for motifs, 1 file for Locations
        #gibbs might need to support multiple files for different lengths of motif
        #User uploads zip/tar with all the files? - problem getting name
        #optional parameters might be the way to go!
        #Gets clunky, but

        #All of these make path/format.json
        motifList = []
        if format.lower() == 'gibbs':
            motifList = GU.parse_gibbs_output(path)
        if format.lower() == 'homer':
            if location == 'NULL':
                print('Motif Location file must be specified for Homer')
                exit()
            motifList = HU.parse_homer_output(path,location)
        if format.lower() == 'meme':
            motifList = MU.parse_meme_output(path)
        if len(motifList) == 0:
            print('No motifs found, exiting')
            exit()
        MSO = {}
        MSO['Condition'] = 'Temp'
        MSO['FeatureSet_ref'] = '123'
        MSO['Motifs'] = []
        MSO['Alphabet'] = ['A','C','G','T']
        MSO['Background'] = {}
        for letter in MSO['Alphabet']:
            MSO['Background'][letter] = 0.0
        MSU.parseMotifList(fullMotifList,MSO)
        objname = 'MotifSet' + str(int((datetime.utcnow() - datetime.utcfromtimestamp(0)).total_seconds()*1000))

        #Pass motif set into this
        save_objects_params = {}
        #save_objects_params['id'] = self.ws_info[0]
        #save_objects_params['id'] = long(params['workspace_name'].split('_')[1])
        save_objects_params['id'] = dfu.ws_name_to_id(params['ws_name'])
        save_objects_params['objects'] = [{'type': 'KBaseGwasData.MotifSet' , 'data' : MSO , 'name' : params['object_name']}]

        info = dfu.save_objects(save_objects_params)[0]
        motif_set_ref = "%s/%s/%s" % (info[6], info[0], info[4])

    except IOError as e:
        if e.errno == errno.ENOENT:
            print('%s - does not exist' % (path))
        elif e.errno == errno.EACCES:
            print('%s - cannot be read' % (path))
        else:
            print('%s - error opening file' % (path))
        exit()
