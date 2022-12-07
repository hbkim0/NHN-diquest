package com.diquest.infochatter3.restapi.model;

import com.fasterxml.jackson.annotation.JsonPropertyOrder;
import java.io.Serializable;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.ToString;

@JsonPropertyOrder({"retcode", "retmsg"})
@Getter
@Setter
@ToString
@NoArgsConstructor
@AllArgsConstructor
public class ErrorResponse implements Serializable {

  /**
   * 결과코드
   * <p>
   * retcode = Result Code
   */
  private String retcode;

  /**
   * 결과메시지
   * <p>
   * retmsg = Result Message
   */
  private String retmsg;

}
