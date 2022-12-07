package com.diquest.infochatter3.restapi.model;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import com.diquest.infochatter3.restapi.util.ConvertUtil;

public abstract class DqmlA {

  public abstract String getDqmlData(String key);

  public abstract Object getDebugData(String key);

  protected abstract String getAnswerData(String key);

  // 사용자발화
  public String getQuery() {
    return getDqmlData("QUERY");
  }

  // 사용자발화
  public String getOriginQuery() {
    return ConvertUtil.objectToString(getDebugData("originQuery"));
  }

  // 오타정보
  public String getProcessedQuery() {
    return ConvertUtil.objectToString(getDebugData("processedQuery"));
  }

  // 형태소, dqml
  public String getMrp() {
    return getDqmlData("POS_LIST");
  }

  // 의도분석결과
  public String getDaAnal() {
    return getDqmlData("DOACT");
  }

  // 신뢰도
  public String getReliability() {
    return getDqmlData("RELIABILITY");
  }

  public String getReliabilityRatio() {
    String reli = getReliability();
    if (reli == null || reli.length() == 0) {
      return null;
    }
    Double reliRatio = Double.parseDouble(reli) / 100;

    return ConvertUtil.objectToString(reliRatio);
  }

  // 형태소 상세
  public String getMorphDtl() {
    return getDqmlData("DEBUG_MORPH");
  }

  public String getDlgMdl() {
    return getDqmlData("MODEL_ID");
  }

  // 개체명, dqml
  public String getNe() {
    return getDqmlData("NE_LIST");
  }

  // 개체명 상세
  public String getNeDtl() {
    return getDqmlData("DEBUG_NE");
  }

  // 키워드
  public String getQryKwd() {
    return getDqmlData("QRY_KWD");
  }

  // 화행, dqml
  public String getSpeeChact() {
    return getDqmlData("SPEECH_ACT_INFO");
  }

  // 화행상세
  public String getSaDtl() {
    return getDqmlData("DEBUG_SPEECH_ACT");
  }

  public String getQryAnal() {
    return getDqmlData("RECOMMEND_QUERY");
  }

  // 키워드
  // 유사어

  // 알고리즘별 정확도

  // 알고리즘 비율
  // 임계점
  // Top N

  // 통합결과 리스트
  public List<Map<String, Double>> getEsmbTotalList() {
    String esmbTotalClassJson = ConvertUtil.objectToString(getDebugData("esmbTotalClassJson"));

    List<Map<String, String>> temp = ConvertUtil.jsonToList(esmbTotalClassJson);

    return roundHalfUp(temp);
  }

  // KNN 결과 리스트
  public List<Map<String, String>> getEsmbKnnList() {
    String esmbKnnClassJson = ConvertUtil.objectToString(getDebugData("esmbKnnClassJson"));

    List<Map<String, String>> temp = ConvertUtil.jsonToList(esmbKnnClassJson);
    List<Map<String, String>> test = new ArrayList<Map<String, String>>();

    if (temp != null) {
      for (Map<String, String> item : temp) {
        Map<String, String> test2 = new HashMap<String, String>();
        for (String key : item.keySet()) {
          String value = item.get(key);
          if ("weight".equals(key)) {
            BigDecimal bigDecimal = new BigDecimal(value);
            bigDecimal = bigDecimal.setScale(6, BigDecimal.ROUND_HALF_UP);
            value = String.valueOf(bigDecimal);
          }
          test2.put(key, value);
        }
        test.add(test2);
      }
    }
    return test;
  }


  // NB 결과 리스트
  public List<Map<String, Double>> getEsmbNbList() {
    String esmbNbClassJson = ConvertUtil.objectToString(getDebugData("esmbNbClassJson"));

    List<Map<String, String>> temp = ConvertUtil.jsonToList(esmbNbClassJson);

    return roundHalfUp(temp);
  }

  // DL 결과 리스트
  public List<Map<String, Double>> getEsmbDlList() {
    String esmbDlClassJson = ConvertUtil.objectToString(getDebugData("esmbDlClassJson"));
    List<Map<String, String>> temp = ConvertUtil.jsonToList(esmbDlClassJson);
    return roundHalfUp(temp);
  }

  // SVM 결과 리스트
  public List<Map<String, Double>> getEsmbSvmList() {
    String esmbSvmClassJson = ConvertUtil.objectToString(getDebugData("esmbSvmClassJson"));
    List<Map<String, String>> temp = ConvertUtil.jsonToList(esmbSvmClassJson);
    return roundHalfUp(temp);
  }

  // 패턴 결과 리스트
  public String getEsmbPattern() {
    return ConvertUtil.objectToString(getDebugData("esmbPatternDoact"));
  }

  // 색인어추출결과
  public String getDoactExtracted() {
    String doactExtracted = ConvertUtil.objectToString(getDebugData("doactExtractedJson"));
    if (doactExtracted != null && doactExtracted.length() > 0) {
      doactExtracted = doactExtracted.replace("[", "").replace("]", "");
    }
    return doactExtracted;
  }

  // 최종검색식
  public List<String> getDoactExpVal() {
    String doactExpValJson = ConvertUtil.objectToString(getDebugData("doactExpValJson"));
    List<String> temp = ConvertUtil.jsonToStringList(doactExpValJson);

    for (int i = 0; i < temp.size(); i++) {
      if (temp.get(i) != null && temp.get(i).length() > 0) {
        String str = temp.get(i);
        temp.set(i, str.replace("<b>", "").replace("</b>", ""));
      }
    }

    return temp;
  }

  // 의도분서검색결과
  public List<Map<String, String>> getDoactGroupResults() {
    String doactInfoClassJson = ConvertUtil.objectToString(getDebugData("doactInfoClassJson"));
    return ConvertUtil.jsonToList(doactInfoClassJson);
  }

  // 답변유형 모델 ID
  public String getAnsType() {
    return ConvertUtil.objectToString(getDebugData("ansType"));
  }

  // 대화모델명
  public String getStusMdlNm() {
    return ConvertUtil.objectToString(getDebugData("stusMdlNm"));
  }

  // 상태ID
  public String getStusNm() {
    return ConvertUtil.objectToString(getDebugData("stusNm"));
  }

  // 진입의도
  public String getStatusEntrDa() {
    return ConvertUtil.objectToString(getDebugData("statusEntrDa"));
  }

  // 답변ID
  public String getStusAnsID() {
    return ConvertUtil.objectToString(getDebugData("stusAnsID"));
  }

  // 우회여부
  public String getStusBypsYn() {
    return ConvertUtil.objectToString(getDebugData("stusBypsYn"));
  }

  // 재귀여부
  public String getStusSelfTrnsYn() {
    return ConvertUtil.objectToString(getDebugData("stusSelfTrnsYn"));
  }

  // 받는 회귀 여부
  public String getStusRtnBrkPtYn() {
    return ConvertUtil.objectToString(getDebugData("stusRtnBrkPtYn"));
  }

  // 보내는 회귀 여부
  public String getStusRtnPtYn() {
    return ConvertUtil.objectToString(getDebugData("stusRtnPtYn"));
  }

  // 이전상태
  public String getLastStusNm() {
    return ConvertUtil.objectToString(getDebugData("lastStusNm"));
  }

  // 현재상태
  public String getCurStusNm() {
    return ConvertUtil.objectToString(getDebugData("curStusNm"));
  }

  // 이전의도
  public String getLastDoactNm() {
    return ConvertUtil.objectToString(getDebugData("lastDoactNm"));
  }

  // 현재의도
  public String getCurDoactNm() {
    return ConvertUtil.objectToString(getDebugData("curDoactNm"));
  }

  // 이전문맥 ctxMdlSysCtxClassJson + ctxCmonSysCtxClassJson
  public List<String> getCtxMdl_CmonSysCtx() {
    String ctxMdlSysCtxClassJson =
        ConvertUtil.objectToString(getDebugData("ctxMdlSysCtxClassJson"));
    List<Map<String, Object>> mdlTemp = ConvertUtil.jsonToListObject(ctxMdlSysCtxClassJson);

    String ctxCmonSysCtxClassJson =
        ConvertUtil.objectToString(getDebugData("ctxCmonSysCtxClassJson"));
    List<Map<String, Object>> cmonTemp = ConvertUtil.jsonToListObject(ctxCmonSysCtxClassJson);

    List<String> tagList = new ArrayList<>();
    if (mdlTemp != null && mdlTemp.size() > 0) {
      for (Map<String, Object> item : mdlTemp) {
        tagList.add(ConvertUtil.objectToString(item.get("tag")));
      }
    }

    if (cmonTemp != null && cmonTemp.size() > 0) {
      for (Map<String, Object> item : cmonTemp) {
        tagList.add(ConvertUtil.objectToString(item.get("tag")));
      }
    }

    return tagList;
  }

  // 현재문맥 - list
  public String getCtxCurSysCtx() {
    return ConvertUtil.objectToString(getDebugData("ctxCurSysCtxClassJson"));
  }

  // 이전답변
  public String getLastAnsUtter() {
    return ConvertUtil.objectToString(getDebugData("lastAnsUtter"));
  }

  // 현재답변
  public String getCurAnsUtter() {
    return ConvertUtil.objectToString(getDebugData("curAnsUtter"));
  }

  // 답변정보
  public String getAnsUtter() {
    return ConvertUtil.objectToString(getDebugData("ansUtter"));
  }

  // 현재 발화 추출개체 - 현재문맥 key 동일함
  public String getOjCtxCurSysCtx() {
    return ConvertUtil.objectToString(getDebugData("ctxCurSysCtxClassJson"));
  }

  // 시스템 저장 개체 - 이전문맥 key 동일함
  public String getOjCtxMdlSysCtx() {
    return ConvertUtil.objectToString(getDebugData("ctxMdlSysCtxClassJson"));
  }

  // 개체 저장순서
  public List<String> getNeCtxSeq() {
    String neCtxSeqJson = ConvertUtil.objectToString(getDebugData("neCtxSeqJson"));
    return ConvertUtil.jsonToStringList(neCtxSeqJson);
  }


  // 상태 히스토리
  public List<String> getCtxStusHist() {
    String ctxStusHistJson = ConvertUtil.objectToString(getDebugData("ctxStusHistJson"));
    return ConvertUtil.jsonToStringList(ctxStusHistJson);
  }

  // 상태 스펙
  public List<String> getCtxStusStack() {
    String ctxStusStackJson = ConvertUtil.objectToString(getDebugData("ctxStusStackJson"));
    return ConvertUtil.jsonToStringList(ctxStusStackJson);
  }

  // 전이조건(매칭된 전이조건)
  public String getTransitionInfo() {
    return ConvertUtil.objectToString(getDebugData("transitionInfo"));
  }

  // 전이조건(출발/도착 모델, 상태)
  public List<Map<String, String>> getTrnsInfo() {
    String trnsInfoClassJson = ConvertUtil.objectToString(getDebugData("trnsInfoClassJson"));
    return ConvertUtil.jsonToList(trnsInfoClassJson);
  }

  // 모델(CORPUS) 객체
  public String getCtxModel() {
    return ConvertUtil.objectToString(getDebugData("ctxModel"));
  }

  // 답변 검색결과 단건
  public Map<String, String> getServInfo() {
    String servInfoClassJson = ConvertUtil.objectToString(getDebugData("servInfoClassJson"));
    List<Map<String, String>> temp = ConvertUtil.jsonToList(servInfoClassJson);

    if (temp != null && temp.size() > 0) {
      return temp.get(0);
    }

    return null;
  }

  // 답변 검색결과
  public List<Map<String, String>> getServInfoList() {
    String servInfoClassJson = ConvertUtil.objectToString(getDebugData("servInfoClassJson"));
    return ConvertUtil.jsonToList(servInfoClassJson);
  }

  // 색인어추출결과
  public String getServExtracted() {
    String servExtractedJson = ConvertUtil.objectToString(getDebugData("servExtractedJson"));
    if (servExtractedJson != null && servExtractedJson.length() > 0) {
      servExtractedJson = servExtractedJson.replace("[", "").replace("]", "");
    }
    return servExtractedJson;
  }

  // 최종검색식 리스트 servExpKeyJson/servExpValJson
  public List<String> getServExpKey() {
    String servExpKeyJson = ConvertUtil.objectToString(getDebugData("servExpValJson"));
    List<String> temp = ConvertUtil.jsonToStringList(servExpKeyJson);

    for (int i = 0; i < temp.size(); i++) {
      if (temp.get(i) != null && temp.get(i).length() > 0) {
        String str = temp.get(i);
        temp.set(i, str.replace("<b>", "").replace("</b>", ""));
      }
    }

    return temp;
  }

  // 단기기억문맥
  public List<Map<String, String>> getStusShrtCtx() {
    String stusShrtCtxClassJson = ConvertUtil.objectToString(getDebugData("stusShrtCtxClassJson"));
    return ConvertUtil.jsonToList(stusShrtCtxClassJson);
  }

  // 필요문맥
  public List<Map<String, String>> getStusSlotCtx() {
    String stusSlotCtxClassJson = ConvertUtil.objectToString(getDebugData("stusSlotCtxClassJson"));
    return ConvertUtil.jsonToList(stusSlotCtxClassJson);
  }

  // 선택문맥
  public List<Map<String, String>> getStusSeltCtx() {
    String stusSeltCtxClassJson = ConvertUtil.objectToString(getDebugData("stusSeltCtxClassJson"));
    return ConvertUtil.jsonToList(stusSeltCtxClassJson);
  }

  // 거부문맥
  public List<Map<String, String>> getStusRjctCtx() {
    String stusRjctCtxClassJson = ConvertUtil.objectToString(getDebugData("stusRjctCtxClassJson"));
    return ConvertUtil.jsonToList(stusRjctCtxClassJson);
  }


  // 오분류의심
  public String getMissMatchYn() {
    return getDqmlData("MISS_MATCH_YN");
  }

  // 의도분석
  public List<String> getDaList() {
    String doactInfoClassJson = ConvertUtil.objectToString(getDebugData("esmbTotalClassJson"));
    if (doactInfoClassJson == null) {
      return null;
    }

    List<Map<String, String>> temp = ConvertUtil.jsonToList(doactInfoClassJson);

    List<String> categoryList = new ArrayList<>();
    if (temp != null && temp.size() > 0) {
      for (Map<String, String> item : temp) {
        Set<String> keySet = item.keySet();
        for (String category : keySet) {
          categoryList.add(category);
        }
      }
    }

    return categoryList;
  }

  public String getUrl() {
    return getAnswerData("url");
  }

  public List<String> getUrls() {
    String url = getUrl();
    if (url == null || url.length() == 0) {
      return null;
    }
    return Arrays.asList(url.split(","));
  }

  public List<Map<String, String>> getDoactAnalyzeInfo() {
    String stusRjctCtxClassJson = ConvertUtil.objectToString(getDqmlData("DOACT_ANALYZE_INFO"));
    return ConvertUtil.jsonToList(stusRjctCtxClassJson);
  }

  // 전이 상태 히스토리
  public List<String> getCtxStusHistFullJson() {
    String ctxStusHistFullJson = ConvertUtil.objectToString(getDebugData("ctxStusHistFullJson"));
    if (ctxStusHistFullJson == null) {
      return null;
    }

    return ConvertUtil.jsonToStringList(ctxStusHistFullJson);
  }

  public List<String> getCtxLastStusHistJson() {
    String ctxLastStusHistJson = ConvertUtil.objectToString(getDebugData("ctxLastStusHistJson"));
    if (ctxLastStusHistJson == null) {
      return null;
    }

    return ConvertUtil.jsonToStringList(ctxLastStusHistJson);
  }

  private List<Map<String, Double>> roundHalfUp(List<Map<String, String>> temp) {
    List<Map<String, Double>> test = new ArrayList<Map<String, Double>>();

    if (temp != null) {
      for (Map<String, String> item : temp) {
        Map<String, Double> test2 = new HashMap<String, Double>();
        for (String key : item.keySet()) {
          BigDecimal bigDecimal = new BigDecimal(item.get(key));
          bigDecimal = bigDecimal.setScale(6, BigDecimal.ROUND_HALF_UP);
          test2.put(key, bigDecimal.doubleValue());
        }
        test.add(test2);
      }
    }

    return test;
  }
}
