package com.diquest.infochatter3.restapi.model;

import java.io.Serializable;
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
public class ChatStartRequest implements Serializable {

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

    return qreq;
  }

}
