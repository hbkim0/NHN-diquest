package com.diquest.infochatter3.restapi.controller;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import javax.servlet.UnavailableException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.util.CollectionUtils;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;
import com.diquest.infochatter3.client.Infochatter3Client;
import com.diquest.infochatter3.client.module.chat.entity.AgentInfoRequest;
import com.diquest.infochatter3.client.module.chat.entity.AgentInfoResponse;
import com.diquest.infochatter3.client.module.chat.entity.AutoCompleteRequest;
import com.diquest.infochatter3.client.module.chat.entity.AutoCompleteResponse;
import com.diquest.infochatter3.client.module.chat.entity.AutoCompleteResponse.AutoComplete;
import com.diquest.infochatter3.client.module.chat.entity.QueryRequest;
import com.diquest.infochatter3.client.module.chat.entity.QueryResponse;
import com.diquest.infochatter3.client.module.chat.entity.ReviewLogRequest;
import com.diquest.infochatter3.client.module.chat.entity.ReviewLogResponse;
import com.diquest.infochatter3.client.module.faq.entity.FaqRequest;
import com.diquest.infochatter3.client.module.faq.entity.FaqResponse;
import com.diquest.infochatter3.client.module.server.entity.HealthResponse;
import com.diquest.infochatter3.restapi.model.AgtInfoResponse;
import com.diquest.infochatter3.restapi.model.ChatNewResponse;
import com.diquest.infochatter3.restapi.model.ChatRequest;
import com.diquest.infochatter3.restapi.model.ChatResponse;
import com.diquest.infochatter3.restapi.model.ChatResponse.Layout;
import com.diquest.infochatter3.restapi.model.ChatStartRequest;
import com.diquest.infochatter3.restapi.model.HealthRequest;
import com.diquest.infochatter3.restapi.model.InquiryRequest;
import com.diquest.infochatter3.restapi.model.SatisfactionRequest;
import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;

@Api(description = "대화서비스")
@RequestMapping(value = {"/chat"}, method = {RequestMethod.POST}, consumes = {"application/json"},
    produces = {"application/json"})
@RestController
public class ChatController {

  @Autowired
  private Infochatter3Client client;

  @ApiOperation("세션시작")
  @RequestMapping({"/startup"})
  public ChatResponse startup(@RequestBody ChatStartRequest creq) throws Exception {
    QueryRequest qreq = creq.asQueryRequest();
    QueryResponse qres = this.client.chat().greeting(qreq);
    List<Layout> messages = new ArrayList<>();
    Layout layout = new Layout();
    layout.setText(qres.getAnswer());
    messages.add(layout);
    return ChatResponse.builder().repoId(creq.getRepoId()).agentName(creq.getAgentName())
        .userId(creq.getUserId()).sessionId(qres.getSessionId()).messages(messages).build();
  }

  @ApiOperation("자동완성")
  @RequestMapping({"/autocomplete"})
  public ChatResponse autocomplete(@RequestBody ChatRequest creq) throws Exception {
    AutoCompleteRequest qreq = AutoCompleteRequest.builder().repoId(creq.getRepoId())
        .agentName(creq.getAgentName()).query(creq.getQuery()).maxSize(5).build();
    AutoCompleteResponse qres = this.client.chat().autocomplete(qreq);
    List<Layout> messages = new ArrayList<>();
    if (!CollectionUtils.isEmpty(qres.getAutoCompletes())) {
      Iterator var5 = qres.getAutoCompletes().iterator();

      while (var5.hasNext()) {
        AutoComplete autocomplete = (AutoComplete) var5.next();
        Layout layout = new Layout();
        layout.setText(autocomplete.getText());
        messages.add(layout);
      }
    }

    return ChatResponse.builder().repoId(creq.getRepoId()).agentName(creq.getAgentName())
        .userId(creq.getUserId()).sessionId(creq.getSessionId()).messages(messages).build();
  }

  @ApiOperation("대화질의")
  @Deprecated
  @RequestMapping({"/message"})
  public ChatResponse message(@RequestBody ChatRequest creq) throws Exception {
    QueryRequest qreq = creq.asQueryRequest();
    QueryResponse qres = this.client.chat().query(qreq);

    List<Layout> messages = new ArrayList<>();
    Layout layout = new Layout();
    layout.setText(qres.getAnswer());
    messages.add(layout);

    List<Layout> detailMessages = new ArrayList<>();
    Layout layout2 = new Layout();
    layout2.setText(qres.getAnswerDetail());
    detailMessages.add(layout2);

    if (creq.getSessionId() == null) {
      creq.setSessionId(qres.getSessionId());
    }

    ChatResponse out = ChatResponse.builder().repoId(creq.getRepoId())
        .agentName(creq.getAgentName()).userId(creq.getUserId()).sessionId(creq.getSessionId())
        .messages(messages).changeAgt(qres.getDqml().get("changeAgt"))
        .chatActive(qres.getDqml().get("chatActive")).emotion(qres.getEmotion())
        .detailMessages(detailMessages).answerName(qres.getAnswerName()).build();

    if ("Y".equals(creq.getDebugYn())) {
      out.setProcessType(qres.getProcessType());
      out.setQuery(qres.getQuery());
      out.setDqml(qres.getDqml());
      out.setDebugInfo(qres.getDebugInfo());
    }
    
    out.setTestParameter("TEST");

    return out;
  }

  @ApiOperation("대화질의 - 신규")
  @RequestMapping({"/message/new"})
  public ChatNewResponse messageNew(@RequestBody ChatRequest creq) throws Exception {
    QueryRequest qreq = creq.asQueryRequest();
    QueryResponse qres = this.client.chat().query(qreq);

    ChatNewResponse out =
        ChatNewResponse.builder().repoId(creq.getRepoId()).userId(creq.getUserId())
            .sessionId(qres.getSessionId()).changeAgt(qres.getDqml().get("changeAgt"))
            .answer(qres.getAnswer()).emotion(qres.getEmotion())
            .answerDetail(qres.getAnswerDetail()).answerName(qres.getAnswerName()).build();

    if ("Y".equals(creq.getDebugYn())) {
      out.setProcessType(qres.getProcessType());
      out.setQuery(qres.getQuery());
      out.setDqml(qres.getDqml());
      out.setDebugInfo(qres.getDebugInfo());
    }
    
    out.setTestParam("TEST");

    return out;
  }

  // @ApiOperation("대화질의-poc")
  // @RequestMapping({"/message/poc"})
  // public ChatPocResponse messagePoc(@RequestBody ChatRequest creq) throws Exception {
  //
  // QueryRequest qreq = creq.asQueryRequest();
  // QueryResponse qres = this.client.chat().query(qreq);
  //
  // ChatPocResponse out = ChatPocResponse.builder().repoId(qres.getRepoId())
  // .agentName(qres.getAgentName()).userId(qres.getUserId()).sessionId(qres.getSessionId())
  // .messages(qres.getAnswer()).changeAgt(qres.getDqml().get("changeAgt"))
  // .chatActive(qres.getDqml().get("chatActive")).emotion(qres.getEmotion())
  // .detailMessages(qres.getAnswerDetail()).answerName(qres.getAnswerName()).build();
  //
  // if ("Y".equals(creq.getDebugYn())) {
  // out.setProcessType(qres.getProcessType());
  // out.setQuery(qres.getQuery());
  // out.setDqml(qres.getDqml());
  // out.setDebugInfo(qres.getDebugInfo());
  // }
  //
  //
  // Map<String, Object> debug = qres.getDebugInfo();
  // String transitionInfo = ConvertUtil.objectToString(debug.get("transitionInfo"));
  // // 시나리오가 아닌 경우에만 사용
  // if (transitionInfo == null || transitionInfo.length() == 0) {
  // // 공통 제외 에이전트 질의.
  // if (!creq.getAgentName().equals("공통")) {
  // // 공통 에이전트에 발화를 던져서 디버그맵 추출.
  // QueryRequest qreqCommon = creq.asQueryRequest();
  // qreqCommon.setSessionId(null);
  // qreqCommon.setAgentName("공통");
  // QueryResponse qresCommon = this.client.chat().query(qreqCommon);
  // debug = qresCommon.getDebugInfo();
  // }
  //
  // // 1-3위 의도를 추출해서 에이전트명 추출.
  // String esmbTotalClassJson = ConvertUtil.objectToString(debug.get("esmbTotalClassJson"));
  // List<Map<String, String>> temp = ConvertUtil.jsonToList(esmbTotalClassJson);
  // if (temp != null && temp.size() > 0) {
  // Set<String> tempSet = new LinkedHashSet<>();
  // int size = temp.size() < 3 ? temp.size() : 3;
  // for (int i = 0; i < size; i++) {
  // Map<String, String> item = temp.get(i);
  // Set<String> keySet = item.keySet();
  // List<String> keyList = new ArrayList<String>(keySet);
  // String da = keyList.get(0);
  // String agt = da.split(">")[0];
  // tempSet.add(agt);
  // }
  //
  // List<String> topAgts = new ArrayList<>(tempSet);
  //
  // // 1위 에이전트가 현재 에이전트가 아닌 경우에만 전달
  // if (!topAgts.get(0).equals(qreq.getAgentName())) {
  // // 1-3위에 현재 에이전트가 있다면 제거.
  // if (topAgts.contains(qreq.getAgentName())) {
  // topAgts.remove(qreq.getAgentName());
  // }
  //
  // // exception은 해당 목록에서 제거.
  // if (topAgts.contains("exception")) {
  // topAgts.remove("exception");
  // }
  // out.setTopAgts(topAgts);
  // }
  // }
  // }
  // return out;
  // }

  @ApiOperation("문맥초기화")
  @RequestMapping({"/reset"})
  public ChatResponse reset(@RequestBody ChatRequest creq) throws Exception {
    QueryRequest qreq = creq.asQueryRequest();
    this.client.chat().clearContext(qreq);
    return ChatResponse.builder().repoId(creq.getRepoId()).agentName(creq.getAgentName())
        .userId(creq.getUserId()).sessionId(creq.getSessionId()).build();
  }

  @ApiOperation("세션종료")
  @RequestMapping({"/end"})
  public ChatResponse end(@RequestBody ChatStartRequest creq) throws Exception {
    QueryRequest qreq = creq.asQueryRequest();
    List<Layout> messages = new ArrayList<>();
    QueryResponse qres = this.client.chat().end(qreq);
    Layout layout = new Layout();
    layout.setText(qres.getAnswer());
    messages.add(layout);
    this.client.chat().removeSession(qreq);
    return ChatResponse.builder().repoId(creq.getRepoId()).agentName(creq.getAgentName())
        .userId(creq.getUserId()).sessionId(creq.getSessionId()).messages(messages).build();
  }

  @ApiOperation("health 체크")
  @RequestMapping({"/health"})
  public void health(@RequestBody HealthRequest creq) throws Exception {
    if (this.client.serverControl().health(creq.getSessionId(), creq.getRepoId()) != 0) {
      throw new UnavailableException("서비스를 사용할 수 없습니다.");
    }
  }

  @ApiOperation("health 체크-솔루션")
  @RequestMapping({"/health/solutions"})
  public HealthResponse healthSolution() throws Exception {
    return client.serverControl().healthSolutions();
  }

  @ApiOperation("FAQ 리스트")
  @RequestMapping({"/faq"})
  public FaqResponse faqList(@RequestBody FaqRequest in) throws Exception {
    FaqResponse faqResp = this.client.faq().getFaqList(in);
    return faqResp;
  }

  @ApiOperation("별점 등록 및 수정")
  @RequestMapping({"/perf-rv/saveSatisfactionNum"})
  public ReviewLogResponse saveSatisfactionNum(@RequestBody SatisfactionRequest in)
      throws Exception {
    ReviewLogRequest reviewReq = in.asReviewLogRequest();
    ReviewLogResponse resp = this.client.chat().addReview(reviewReq);
    return resp;
  }

  @ApiOperation("문의 등록")
  @RequestMapping({"/perf-rv/saveInquiry"})
  public ReviewLogResponse saveInquiry(@RequestBody InquiryRequest in) throws Exception {
    ReviewLogRequest reviewReq = in.asReviewLogRequest();
    ReviewLogResponse resp = this.client.chat().addReview(reviewReq);
    return resp;
  }

  @ApiOperation("에이전트 정보")
  @RequestMapping({"/getAgtInfo"})
  public AgtInfoResponse getAgtInfo(@RequestBody AgentInfoRequest areq) throws Exception {

    AgentInfoResponse aresp = this.client.chat().getAgtInfo(areq);



    return AgtInfoResponse.builder().repoId(aresp.getRepoId()).agentName(aresp.getAgentName())
        .userId(aresp.getUserId()).sessionId(aresp.getSessionId())
        .satisfactionRange(aresp.getSatisfactionRange()).dissatisfaction(aresp.getDissatisfaction())
        .questionType(aresp.getQuestionType().split(",")).build();
  }


  // @ApiOperation("워크피디아_대화질의")
  // @RequestMapping({"/workpedia/message"})
  // public ChatResponse message(@RequestBody WorkpediaChatRequest creq) throws Exception {
  // QueryRequest qreq = creq.asQueryRequest();
  //
  // qreq.addExtra("userId", creq.getUserId());
  // qreq.addExtra("userName", creq.getUserName());
  //
  // qreq.addExtra("quizDataType", creq.getQuizInfo().getDataType());
  // qreq.addExtra("quizSetNo", creq.getQuizInfo().getSetNo());
  // qreq.addExtra("quizNo", creq.getQuizInfo().getNo());
  // qreq.addExtra("quizAnswer", creq.getQuizInfo().getAnswer());
  //
  // QueryResponse qres = this.client.chat().query(qreq);
  // List<Layout> messages = new ArrayList<>();
  // Layout layout = new Layout();
  // layout.setText(qres.getAnswer());
  // messages.add(layout);
  // if (creq.getSessionId() == null) {
  // creq.setSessionId(qres.getSessionId());
  // }
  //
  // return ChatResponse.builder().repoId(creq.getRepoId()).agentName(creq.getAgentName())
  // .userId(creq.getUserId()).sessionId(creq.getSessionId()).messages(messages)
  // .changeAgt(qres.getDqml().get("changeAgt")).chatActive(qres.getDqml().get("chatActive"))
  // .emotion(qres.getEmotion()).build();
  // }
}
