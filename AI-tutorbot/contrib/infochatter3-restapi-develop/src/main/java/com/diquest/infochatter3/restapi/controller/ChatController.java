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

@Api(description = "???????????????")
@RequestMapping(value = {"/chat"}, method = {RequestMethod.POST}, consumes = {"application/json"},
    produces = {"application/json"})
@RestController
public class ChatController {

  @Autowired
  private Infochatter3Client client;

  @ApiOperation("????????????")
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

  @ApiOperation("????????????")
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

  @ApiOperation("????????????")
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

  @ApiOperation("???????????? - ??????")
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

  // @ApiOperation("????????????-poc")
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
  // // ??????????????? ?????? ???????????? ??????
  // if (transitionInfo == null || transitionInfo.length() == 0) {
  // // ?????? ?????? ???????????? ??????.
  // if (!creq.getAgentName().equals("??????")) {
  // // ?????? ??????????????? ????????? ????????? ???????????? ??????.
  // QueryRequest qreqCommon = creq.asQueryRequest();
  // qreqCommon.setSessionId(null);
  // qreqCommon.setAgentName("??????");
  // QueryResponse qresCommon = this.client.chat().query(qreqCommon);
  // debug = qresCommon.getDebugInfo();
  // }
  //
  // // 1-3??? ????????? ???????????? ??????????????? ??????.
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
  // // 1??? ??????????????? ?????? ??????????????? ?????? ???????????? ??????
  // if (!topAgts.get(0).equals(qreq.getAgentName())) {
  // // 1-3?????? ?????? ??????????????? ????????? ??????.
  // if (topAgts.contains(qreq.getAgentName())) {
  // topAgts.remove(qreq.getAgentName());
  // }
  //
  // // exception??? ?????? ???????????? ??????.
  // if (topAgts.contains("exception")) {
  // topAgts.remove("exception");
  // }
  // out.setTopAgts(topAgts);
  // }
  // }
  // }
  // return out;
  // }

  @ApiOperation("???????????????")
  @RequestMapping({"/reset"})
  public ChatResponse reset(@RequestBody ChatRequest creq) throws Exception {
    QueryRequest qreq = creq.asQueryRequest();
    this.client.chat().clearContext(qreq);
    return ChatResponse.builder().repoId(creq.getRepoId()).agentName(creq.getAgentName())
        .userId(creq.getUserId()).sessionId(creq.getSessionId()).build();
  }

  @ApiOperation("????????????")
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

  @ApiOperation("health ??????")
  @RequestMapping({"/health"})
  public void health(@RequestBody HealthRequest creq) throws Exception {
    if (this.client.serverControl().health(creq.getSessionId(), creq.getRepoId()) != 0) {
      throw new UnavailableException("???????????? ????????? ??? ????????????.");
    }
  }

  @ApiOperation("health ??????-?????????")
  @RequestMapping({"/health/solutions"})
  public HealthResponse healthSolution() throws Exception {
    return client.serverControl().healthSolutions();
  }

  @ApiOperation("FAQ ?????????")
  @RequestMapping({"/faq"})
  public FaqResponse faqList(@RequestBody FaqRequest in) throws Exception {
    FaqResponse faqResp = this.client.faq().getFaqList(in);
    return faqResp;
  }

  @ApiOperation("?????? ?????? ??? ??????")
  @RequestMapping({"/perf-rv/saveSatisfactionNum"})
  public ReviewLogResponse saveSatisfactionNum(@RequestBody SatisfactionRequest in)
      throws Exception {
    ReviewLogRequest reviewReq = in.asReviewLogRequest();
    ReviewLogResponse resp = this.client.chat().addReview(reviewReq);
    return resp;
  }

  @ApiOperation("?????? ??????")
  @RequestMapping({"/perf-rv/saveInquiry"})
  public ReviewLogResponse saveInquiry(@RequestBody InquiryRequest in) throws Exception {
    ReviewLogRequest reviewReq = in.asReviewLogRequest();
    ReviewLogResponse resp = this.client.chat().addReview(reviewReq);
    return resp;
  }

  @ApiOperation("???????????? ??????")
  @RequestMapping({"/getAgtInfo"})
  public AgtInfoResponse getAgtInfo(@RequestBody AgentInfoRequest areq) throws Exception {

    AgentInfoResponse aresp = this.client.chat().getAgtInfo(areq);



    return AgtInfoResponse.builder().repoId(aresp.getRepoId()).agentName(aresp.getAgentName())
        .userId(aresp.getUserId()).sessionId(aresp.getSessionId())
        .satisfactionRange(aresp.getSatisfactionRange()).dissatisfaction(aresp.getDissatisfaction())
        .questionType(aresp.getQuestionType().split(",")).build();
  }


  // @ApiOperation("???????????????_????????????")
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
