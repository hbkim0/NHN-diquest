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
public class HealthRequest implements Serializable {

  /**
   * 대화세션 ID
   */
  private String sessionId;

  private String repoId;

  public QueryRequest asQueryRequest() {
    QueryRequest qreq = new QueryRequest();
    if (this.sessionId != null) {
      qreq.setSessionId(this.sessionId);
    }

    return qreq;
  }

}
