
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
 * <p>Original spec-file type: ImportNarrativeInParams</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "ws_name",
    "path",
    "format",
    "obj_name"
})
public class ImportNarrativeInParams {

    @JsonProperty("ws_name")
    private String wsName;
    @JsonProperty("path")
    private String path;
    @JsonProperty("format")
    private String format;
    @JsonProperty("obj_name")
    private String objName;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("ws_name")
    public String getWsName() {
        return wsName;
    }

    @JsonProperty("ws_name")
    public void setWsName(String wsName) {
        this.wsName = wsName;
    }

    public ImportNarrativeInParams withWsName(String wsName) {
        this.wsName = wsName;
        return this;
    }

    @JsonProperty("path")
    public String getPath() {
        return path;
    }

    @JsonProperty("path")
    public void setPath(String path) {
        this.path = path;
    }

    public ImportNarrativeInParams withPath(String path) {
        this.path = path;
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

    public ImportNarrativeInParams withFormat(String format) {
        this.format = format;
        return this;
    }

    @JsonProperty("obj_name")
    public String getObjName() {
        return objName;
    }

    @JsonProperty("obj_name")
    public void setObjName(String objName) {
        this.objName = objName;
    }

    public ImportNarrativeInParams withObjName(String objName) {
        this.objName = objName;
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
        return ((((((((((("ImportNarrativeInParams"+" [wsName=")+ wsName)+", path=")+ path)+", format=")+ format)+", objName=")+ objName)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
