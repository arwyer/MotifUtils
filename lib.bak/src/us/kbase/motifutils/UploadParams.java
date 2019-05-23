
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
 * <p>Original spec-file type: UploadParams</p>
 * <pre>
 * -commenting out for now
 * typedef structure{
 * } ExportParams;
 * typedef structure{
 * } ExportOutput;
 * funcdef ExportMotifSet()
 *   returns ()  authentication required;
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "ws_name",
    "object_name",
    "filepath",
    "format"
})
public class UploadParams {

    @JsonProperty("ws_name")
    private String wsName;
    @JsonProperty("object_name")
    private String objectName;
    @JsonProperty("filepath")
    private String filepath;
    @JsonProperty("format")
    private String format;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("ws_name")
    public String getWsName() {
        return wsName;
    }

    @JsonProperty("ws_name")
    public void setWsName(String wsName) {
        this.wsName = wsName;
    }

    public UploadParams withWsName(String wsName) {
        this.wsName = wsName;
        return this;
    }

    @JsonProperty("object_name")
    public String getObjectName() {
        return objectName;
    }

    @JsonProperty("object_name")
    public void setObjectName(String objectName) {
        this.objectName = objectName;
    }

    public UploadParams withObjectName(String objectName) {
        this.objectName = objectName;
        return this;
    }

    @JsonProperty("filepath")
    public String getFilepath() {
        return filepath;
    }

    @JsonProperty("filepath")
    public void setFilepath(String filepath) {
        this.filepath = filepath;
    }

    public UploadParams withFilepath(String filepath) {
        this.filepath = filepath;
        return this;
    }

    @JsonProperty("format")
    public String getFormat() {
        return format;
    }

    @JsonProperty("format")
    public void setFormat(String format) {
        this.format = format;
    }

    public UploadParams withFormat(String format) {
        this.format = format;
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
        return ((((((((((("UploadParams"+" [wsName=")+ wsName)+", objectName=")+ objectName)+", filepath=")+ filepath)+", format=")+ format)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
