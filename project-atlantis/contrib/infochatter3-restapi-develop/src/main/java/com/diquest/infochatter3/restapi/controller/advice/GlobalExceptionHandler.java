package com.diquest.infochatter3.restapi.controller.advice;

import com.diquest.infochatter3.client.exception.CommandException;
import com.diquest.infochatter3.restapi.model.ErrorResponse;
import javax.servlet.http.HttpServletResponse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.support.MessageSourceAccessor;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseStatus;

/**
 * 전역 예외처리 핸들러
 */
@ControllerAdvice
public class GlobalExceptionHandler {

  @Autowired
  private MessageSourceAccessor messageSource;

  /**
   * 모든 에러
   */
  @ExceptionHandler(Exception.class)
  @ResponseStatus(value = HttpStatus.INTERNAL_SERVER_ERROR)
  public ErrorResponse exception(Exception e) {
    String retmsg = messageSource.getMessage("Exception", new Object[]{e.getMessage()});
    return new ErrorResponse("9999", retmsg);
  }

  /**
   * 자바클라이언트 처리오류
   */
  @ExceptionHandler(CommandException.class)
  public ErrorResponse commandException(HttpServletResponse response, CommandException e) {
    switch (e.getCode()) {
      // NLU 과정 오류
      case -11001:
      case -11002:
      case -11003:
      case -11004:
      case -11005:
      case -11006:
        response.setStatus(HttpServletResponse.SC_INTERNAL_SERVER_ERROR);
        return new ErrorResponse("0511", messageSource.getMessage("CommandException.NLU"));
      // 대화상태 과정 오류
      case -12001:
      case -12002:
      case -12003:
      case -12004:
      case -12005:
      case -12006:
        response.setStatus(HttpServletResponse.SC_INTERNAL_SERVER_ERROR);
        return new ErrorResponse("0512", messageSource.getMessage("CommandException.DM"));
      // 답변생성 과정 오류
      case -13001:
      case -13002:
      case -13003:
      case -13004:
      case -13005:
      case -13006:
      case -13007:
        response.setStatus(HttpServletResponse.SC_INTERNAL_SERVER_ERROR);
        return new ErrorResponse("0513", messageSource.getMessage("CommandException.DM"));
      // 에이전트 통신 오류
      case -14001:
      case -14003:
        response.setStatus(HttpServletResponse.SC_INTERNAL_SERVER_ERROR);
        return new ErrorResponse("0514", messageSource.getMessage("CommandException.DM"));
      // 그 외 통신,워커할당등 오류
      case -60003:
      case -60004:
      case -60005:
      case -60006:
      case -60011:
      case -70001:
        response.setStatus(HttpServletResponse.SC_SERVICE_UNAVAILABLE);
        return new ErrorResponse("0503", messageSource.getMessage("CommandException.ERR"));
      case -70000:
      case -99999:
      default:
        response.setStatus(HttpServletResponse.SC_INTERNAL_SERVER_ERROR);
        return new ErrorResponse("0500", e.getMessage());
    }
  }

}
