/*
A KBase module: MotifUtils
*/

module MotifUtils {

/*
NOTES:
What do we need to be able to do with a MotifSet?
Convert and save motifset in common format(JASPAR, etc.)
Save motifSet to shock
Pull motifset from shock
Save motifSet to workspace


functions:
save - take a motifset
upload - take an external format(JASPAR) and convert it to KBase motifset
download - take a motifset object and create an external format(JASPAR)
export - download file from shock to workspace as an object?

dfu.save_objects -> use this when you want to make an object
dfu.get_objects -> use this to get object from shock

destination_ref - ws_name / object_name
convert ws_name to id, used by save_objects
*/




/*
*/
typedef structure{
  string obj_ref;
} UploadOutput;

typedef structure{
  string ws_name;
  string source_ref;
  string format;
  string outname;
} DownloadParams;

typedef structure{
  string destination_path;
} DownloadOutput;

typedef structure{
  string ws_name;
  string staging_path;
  string local_path;
  string shock_id;
  string format;
  string obj_name;
} ImportNarrativeInParams;

typedef structure{
  string obj_ref;
} ImportNarrativeOutParams;

typedef structure{
  string path;
  string ws_name;
  string obj_name;
} UploadJASPARInParams;

typedef structure{
  string path;
  string ws_name;
  string obj_name;
} UploadTRANSFACInParams;

/*
optional - absolute_locations
*/
typedef structure{
  string path;
  string ws_name;
  string obj_name;
  mapping<string, string> absolute_locations;
} UploadMEMEInParams;

typedef structure{
  string path;
  string ws_name;
  string obj_name;
} UploadGibbsInParams;

typedef structure{
  string path;
  string ws_name;
  string obj_name;
  string location_path;
} UploadHomerInParams;

funcdef UploadFromGibbs(UploadMEMEInParams params)
  returns (UploadOutput output)  authentication required;

funcdef UploadFromHomer(UploadHomerInParams params)
  returns (UploadOutput output)  authentication required;

funcdef UploadFromMEME(UploadGibbsInParams params)
  returns (UploadOutput output)  authentication required;

funcdef UploadFromJASPAR(UploadJASPARInParams params)
  returns (UploadOutput output)  authentication required;

funcdef UploadFromTRANSFAC(UploadTRANSFACInParams params)
  returns (UploadOutput output)  authentication required;

funcdef DownloadMotifSet(DownloadParams params)
  returns (DownloadOutput output)  authentication required;

funcdef importFromNarrative(ImportNarrativeInParams params)
  returns (ImportNarrativeOutParams out) authentication required;


};
