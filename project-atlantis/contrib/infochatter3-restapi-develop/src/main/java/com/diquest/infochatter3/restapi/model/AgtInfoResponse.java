package com.diquest.infochatter3.restapi.model;

import java.io.Serializable;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.ToString;

@JsonPropertyOrder({"repoId", "agtNm", "userId", "sessId", "qry"})
@Getter
@Setter
@ToString
@NoArgsConstructor
@AllArgsConstructor
@Builder(toBuilder = true)
public class AgtInfoResponse implements Serializable {

  /**
   * 저장소아이디
   */
  private String repoId;

  /**
   * 에이전트명
   */
  private String agentName;

  /**
   * 사용자아이디
   */
  private String userId;

  /**
   * 세션아이디
   */
  private String sessionId;

  /**
   * 만족도 범위
   */
  private String satisfactionRange;

  /**
   * 불만족 기준 점수
   */
  private String dissatisfaction;

  /**
   * 문의 유형
   */
  private String[] questionType;

  /**
   * 에이전트 테마
   */
  private String thema;

}
