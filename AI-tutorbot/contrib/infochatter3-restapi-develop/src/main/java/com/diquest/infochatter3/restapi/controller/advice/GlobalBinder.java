package com.diquest.infochatter3.restapi.controller.advice;

import org.springframework.beans.propertyeditors.StringTrimmerEditor;
import org.springframework.web.bind.WebDataBinder;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.InitBinder;

@ControllerAdvice
public class GlobalBinder {

  @InitBinder
  public void initBinder(WebDataBinder binder) {
    /*
     * Controller 에 전달된 String 자료형 값 Trim 처리
     * {@link StringTrimmerEditor} 의 첫번째 인자 값이
     * true: 공백인 경우 Null 처리함
     * false: 공백인 경우 Null 처리하지 않음
     */
    binder.registerCustomEditor(String.class, new StringTrimmerEditor(false));
  }

}
