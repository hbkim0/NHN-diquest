package com.diquest.infochatter3.restapi.model;

import java.io.Serializable;
import java.util.HashMap;
import java.util.Map;
import com.diquest.infochatter3.client.module.chat.entity.QueryRequest;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.ToString;

@JsonPropertyOrder({"repoId", "agentName", "userId", "sessionId", "query"})
@Getter
@Setter
@ToString
@NoArgsConstructor
@AllArgsConstructor
@Builder(toBuilder = true)
public class ChatRequest implements Serializable {

  /**
   * 저장소아이디
   */
  private String repoId;

  /**
   * 에이전트명
   */
  private String agentName;

  /**
   * 사용자 ID
   */
  private String userId;

  /**
   * 대화세션 ID
   */
  private String sessionId;

  /**
   * 질의
   */
  private String query;

  private String debugYn;

  // 사용자 추가 입력 dqml
  private Map<String, String> extDqml;

  // 사용자 추가 입력 dqml(영속-세션이 끝날떄까지 엔진에서 유지함)
  private Map<String, String> persistDqml;

  // 사용자 추가 입력 dqml(질의로그 입력용)
  private Map<String, String> qryLogDqml;

  public QueryRequest asQueryRequest() {
    QueryRequest qreq = new QueryRequest();
    if (this.repoId != null) {
      qreq.setRepoId(this.repoId);
    }
    if (this.agentName != null) {
      qreq.setAgentName(this.agentName);
    }
    if (this.userId != null) {
      qreq.setUserId(this.userId);
    }
    if (this.sessionId != null) {
      qreq.setSessionId(this.sessionId);
    }
    if (this.query != null) {
      qreq.setQuery(this.query);
    }
    if (this.extDqml != null) {
      qreq.setExtras(extDqml);
    }

    if (this.persistDqml != null) {
      Map<String, String> prefixMap = appendPrefix("CTX", persistDqml);
      if (qreq.getExtras() == null) {
        qreq.setExtras(prefixMap);
      } else {
        qreq.getExtras().putAll(prefixMap);
      }
    }

    if (this.qryLogDqml != null) {
      Map<String, String> prefixMap = appendPrefix("DB", qryLogDqml);
      if (qreq.getExtras() == null) {
        qreq.setExtras(prefixMap);
      } else {
        qreq.getExtras().putAll(prefixMap);
      }
    }

    return qreq;
  }

  private Map<String, String> appendPrefix(String prefix, Map<String, String> map) {
    Map<String, String> prefixMap = new HashMap<>();
    for (String key : map.keySet()) {
      prefixMap.put(prefix + "." + key, map.get(key));
    }

    return prefixMap;
  }
}
