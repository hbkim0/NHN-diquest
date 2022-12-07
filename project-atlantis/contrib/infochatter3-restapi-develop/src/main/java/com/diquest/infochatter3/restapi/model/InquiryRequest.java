package com.diquest.infochatter3.restapi.model;

import java.io.Serializable;
import com.diquest.infochatter3.client.module.chat.entity.ReviewLogRequest;
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
public class InquiryRequest implements Serializable {

  /**
   * 로그 id
   */
  public String id;

  /**
   * 저장소 id
   */
  public String repoId;

  /**
   * 에이전트명
   */
  public String agtNm;

  /**
   * 사용자아이디
   */
  public String userId;

  /**
   * 의도명
   */
  public String daName;

  /**
   * 입력발화
   */
  public String qry;

  /**
   * 문의 유형
   */
  public String inquiryType;

  /**
   * 문의 제목
   */
  public String inquiryTitle;

  /**
   * 문의 내용
   */
  public String inquiryContents;
  /**
   * 신뢰도
   */
  public Integer reli;

  /**
   * 답변명
   */
  public String answerName;

  /**
   * 답변
   */
  public String answer;

  /**
   * 세션아이디
   */
  public String sessId;

  /**
   * 동작 타입 (추가=I,삭제=D,수정=U)
   */
  public String actType;

  public ReviewLogRequest asReviewLogRequest() {
    ReviewLogRequest rereq = new ReviewLogRequest();
    if (!("I".equals(this.actType))) {
      rereq.setId(this.id);
    }
    if (this.repoId != null) {
      rereq.setRepoId(this.repoId);
    }
    if (this.agtNm != null) {
      rereq.setAgentName(this.agtNm);
    }
    if (this.userId != null) {
      rereq.setUserId(this.userId);
    }
    if (this.sessId != null) {
      rereq.setSessionId(this.sessId);
    }
    if (this.qry != null) {
      rereq.setQry(this.qry);
    }
    if (this.daName != null) {
      rereq.setDaName(this.daName);
    }
    if (this.reli != null) {
      rereq.setReli(this.reli.toString());
    }
    if (this.answer != null) {
      rereq.setAnswer(this.answer);
    }
    if (this.answerName != null) {
      rereq.setAnswerName(this.answerName);
    }
    if (this.inquiryType != null) {
      rereq.setInquiryType(this.inquiryType.toString());
    }
    if (this.inquiryTitle != null) {
      rereq.setInquiryTitle(this.inquiryTitle.toString());
    }
    if (this.inquiryContents != null) {
      rereq.setInquiryContents(this.inquiryContents.toString());
    }

    rereq.setActType(actType);

    return rereq;
  }

}
