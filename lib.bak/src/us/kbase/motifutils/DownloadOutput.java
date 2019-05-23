
package us.kbase.motifutils;

import java.util.HashMap;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: DownloadOutput</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "destination_dir"
})
public class DownloadOutput {

    @JsonProperty("destination_dir")
    private String destinationDir;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("destination_dir")
    public String getDestinationDir() {
        return destinationDir;
    }

    @JsonProperty("destination_dir")
    public void setDestinationDir(String destinationDir) {
        this.destinationDir = destinationDir;
    }

    public DownloadOutput withDestinationDir(String destinationDir) {
        this.destinationDir = destinationDir;
        return this;
    }

    @JsonAnyGetter
    public Map<String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public String toString() {
        return ((((("DownloadOutput"+" [destinationDir=")+ destinationDir)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
