package com.diquest.infochatter3.restapi.model;

import java.io.Serializable;
import java.util.Map;
import com.diquest.infochatter3.restapi.util.ConvertUtil;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;
import io.swagger.annotations.ApiModelProperty;
import lombok.AccessLevel;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.ToString;

@JsonPropertyOrder({"repoId", "agentName", "userId", "sessionId", "messages"})
@Getter
@Setter
@ToString
@NoArgsConstructor
@AllArgsConstructor
@Builder(toBuilder = true)
public class ChatNewResponse implements Serializable {

  /**
   * 저장소아이디
   */
  private String repoId;


  /**
   * 사용자아이디
   */
  private String userId;

  /**
   * 세션아이디
   */
  private String sessionId;

  /**
   * 메시지 목록
   */

  private String answerName;

  private String answer;

  private String answerDetail;

  /**
   * 에이전트 변경 여부
   */
  private String changeAgt;

  /**
   * 답변 감정정보
   */
  private String emotion;

  private String query;

  // 디버그 info 정보.
  @ApiModelProperty(value = "분석유형")
  private String processType;

  @ApiModelProperty(value = "URL")
  private String url;

  @ApiModelProperty(value = "dqml")
  @Getter(AccessLevel.PRIVATE)
  private Map<String, String> dqml;

  @ApiModelProperty(value = "디버그 정보")
  @Getter(AccessLevel.PRIVATE)
  private Map<String, Object> debugInfo;
  
  private String testParam;

  public String getDqmlData(String key) {
    return this.dqml == null ? null : getDqml().get(key);
  }

  public Object getDebugData(String key) {
    return this.debugInfo == null ? null : getDebugInfo().get(key);
  }

  // 의도분석결과
  public String getDaAnal() {
    return getDqmlData("DOACT");
  }

  // 개체명, dqml
  public String getNe() {
    return getDqmlData("NE_LIST");
  }

  // 현재상태
  public String getCurMdlNm() {
    return ConvertUtil.objectToString(getDebugData("curMdlNm"));
  }

  // 현재상태
  public String getCurStusNm() {
    return ConvertUtil.objectToString(getDebugData("curStusNm"));
  }
}
