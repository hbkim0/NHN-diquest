package com.diquest.infochatter3.restapi.util;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;

/** 형변환, 계산 일괄처리 유틸 */

public class ConvertUtil {

  private ConvertUtil() {

  }

  private static final ObjectMapper jsonMapper = new ObjectMapper();

  public static Map<String, String> jsonToMap(String json) {
    TypeReference<Map<String, Object>> typeRef = new TypeReference<Map<String, Object>>() {};
    try {
      if (json != null) {
        return jsonMapper.readValue(json, typeRef);
      } else {
        return new HashMap<String, String>();
      }
    } catch (IOException e) {
      throw new RuntimeException(e);
    }
  }

  public static String ObjectToJson(Object obj) {
    try {
      return jsonMapper.writeValueAsString(obj);
    } catch (JsonProcessingException e) {
      throw new RuntimeException(e);
    }
  }

  public static String mapToJson(Map<String, String> map) {
    try {
      return jsonMapper.writeValueAsString(map);
    } catch (JsonProcessingException e) {
      throw new RuntimeException(e);
    }
  }

  public static Map<String, Object> jsonToMapObject(String json) {
    TypeReference<Map<String, Object>> typeRef = new TypeReference<Map<String, Object>>() {};
    try {
      if (json != null && json.length() > 0) {
        return jsonMapper.readValue(json, typeRef);
      } else {
        return new HashMap<String, Object>();
      }
    } catch (IOException e) {
      throw new RuntimeException(e);
    }
  }

  public static List<Map<String, String>> jsonToList(String json) {
    if (json == null || json.length() == 0) {
      return new ArrayList<Map<String, String>>();
    }

    List<Map<String, String>> temp = null;
    try {
      temp = jsonMapper.readValue(json, new TypeReference<List<Map<String, String>>>() {});
    } catch (IOException e) {
      e.printStackTrace();
    }
    return temp;
  }

  public static List<Map<String, Object>> jsonToListObject(String json) {
    if (json == null) {
      return new ArrayList<Map<String, Object>>();
    }

    List<Map<String, Object>> temp = null;
    try {
      temp = jsonMapper.readValue(json, new TypeReference<List<Map<String, Object>>>() {});
    } catch (IOException e) {
      e.printStackTrace();
    }
    return temp;
  }

  public static List<String> jsonToStringList(String json) {
    if (json == null) {
      return new ArrayList<String>();
    }

    List<String> temp = null;
    try {
      temp = jsonMapper.readValue(json, new TypeReference<List<String>>() {});
    } catch (IOException e) {
      e.printStackTrace();
    }
    return temp;
  }

  public static Integer StringToInteger(String source) {
    return source == null || source.length() == 0 ? null : Integer.parseInt(source);
  }

  public static String objectToString(Object t) {
    return t == null ? null : String.valueOf(t);
  }


  public static String getRatioString(String value) {
    if (value == null || value.length() == 0) {
      return null;
    }
    return objectToString(Double.parseDouble(value) / 100);
  }

  public static Double getRatio(Integer value) {
    if (value == null) {
      return null;
    }
    return value.doubleValue() / 100;
  }
}
