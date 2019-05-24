/*
A KBase module: MotifUtils
*/

module MotifUtils {
    /* workspace name of the object */
    typedef string workspace_name;

    /* An X/Y/Z style reference */
    typedef string obj_ref;

    /* Input/Output motif format
        @range("MEME", "JASPAR", "GIBBS", "HOMER", "TRANSFAC", "MFMD")
    */
    typedef string motif_format;

    /* Ref to a sequence set
        @id ws KBaseGeneRegulation.MotifSet
    */
    typedef string MotifSetRef;

    typedef structure {
        string path;
        string shock_id;
        string ftp_url;
    } File;

    /*
        Functionality of Motif Utils:
            1. upload external motif finder outputs to KBase MotifSet object (Import Motifs frontend)
            2. parse a  container local file of an accepted motif application output into a motif set object
            3. save a container local file of accepted motif application output to a motif set object
            4. download motifset object as a motif application output file (Download Motifs frontend)

        Add future implementation here: https://github.com/kbasecollaborations/MotifUtils
    */

    /*
        sequence_id - id of sequence motif was found in associated sequenceset
        start - start of motif in the sequence
        end - end of motif in the sequence
        orientation - +/-
        sequence - actual motif sequence, might not match exactly to IUPAC
    */

    typedef structure {
      string sequence_id;
      int start;
      int end;
      string orientation;
      string sequence;
    } Motif_Location;

    /*
        one of PWM or PFM must be included
        PWM - position weight matrix of motif
        PFM - position frequency matrix of motif
        Iupac_signature - motif represented in Iupac notation
        Motif_Locations - list of locations where motif has been found
    */
    typedef structure {
      mapping<string, list<float>> PWM;
      mapping<string, list<float>> PFM;
      string Iupac_sequence;
      list<Motif_Location> Motif_Locations;
    } Motif;

    /*
        Condition - description of conditionused to select sequences
        SequenceSet_ref - reference to sequenceset used to find motifs
        Motifs - list of motifs
        Alphabet - list of letters used in sequences, e.g. ['A','C','G','T'] for DNA
        Background - background frequencies of letters in alphabet
    */
    typedef structure {
      string Condition;
      string SequenceSet_ref;
      list<Motif> Motifs;
      list<string> Alphabet;
      mapping<string, float> Background;
    } MotifSet;

    typedef structure{
        string report_name;
        string report_ref;
    } UIOutParams;

    typedef structure{
        motif_format format;
        string path;
        string obj_name;
        workspace_name ws_name;
    } uploadParams;

    funcdef uploadMotifSet(uploadParams params)
      returns (UIOutParams out) authentication required;

    typedef structure{
        motif_format format;
        File file;
        workspace_name ws_name;
    } parseParams;

    funcdef parseMotifSet(parseParams params)
      returns (MotifSet out) authentication required;

    typedef structure{
        motif_format format;
        File file;
        string obj_name;
        workspace_name ws_name;
    } saveParams;

    funcdef saveMotifSet(saveParams params)
      returns (MotifSetRef out) authentication required;

    typedef structure{
        motif_format format;
        MotifSetRef motifset;
        workspace_name ws_name;
    } downloadParams;

    funcdef downloadMotifSet(downloadParams params)
      returns (UIOutParams out) authentication required;
};