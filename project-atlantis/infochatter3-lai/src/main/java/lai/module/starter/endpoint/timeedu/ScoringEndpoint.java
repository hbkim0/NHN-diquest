package lai.module.starter.endpoint.timeedu;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.LinkedList;
import java.util.List;
import java.util.StringJoiner;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.JSONValue;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

import com.diquest.lai.module.Endpoint;
import com.diquest.lai.module.EndpointMapping;

import lai.module.starter.config.ConnectionConfig;
import lai.module.starter.endpoint.timeedu.model.ScoringInput.Image;
import lai.module.starter.endpoint.timeedu.model.ScoringInput.Submit;
import lai.module.starter.endpoint.timeedu.model.ScoringOutput.Recognition;
import lai.module.starter.endpoint.timeedu.model.ScoringOutput.RecognitionOutput;
import lai.module.starter.endpoint.timeedu.model.ScoringOutput.ResultOutput;

@Endpoint
public class ScoringEndpoint {
		
	@SuppressWarnings("unchecked")
	@EndpointMapping(mapping = "자동채점.추론", description = "타임교육 튜터봇 자동채점 추론")
	public RecognitionOutput inference(Image input) {
		
		HttpURLConnection conn = null;
		RecognitionOutput output = new RecognitionOutput();
		List<Recognition> list = new LinkedList<Recognition>();
		try {
		    JSONObject reqBody = new JSONObject();
		    reqBody.put("user_id", input.getUserId());
		    reqBody.put("input_url", input.getImgUrl());
		    reqBody.put("log", 1);
		    
			URL url = new URL(ConnectionConfig.SCORING_SERVICE_URL+"api/v1/infer/dnr");
			conn = (HttpURLConnection) url.openConnection();
			conn.setRequestMethod("POST");
			conn.setRequestProperty("Content-Type", "application/json");
			conn.setRequestProperty("Accept", "application/json");
			conn.setConnectTimeout(3000);
			conn.setReadTimeout(3000);
			conn.setDoOutput(true);
			
		    OutputStreamWriter os = new OutputStreamWriter(conn.getOutputStream());
		    os.write(reqBody.toString());
		    os.flush();
		    
		    BufferedReader br = new BufferedReader(new InputStreamReader(conn.getInputStream()));
		    JSONObject responseJson = (JSONObject) JSONValue.parse(br.readLine());
		    JSONObject workbook = (JSONObject) responseJson.get("workbook");
		    JSONObject page = (JSONObject) responseJson.get("page");
		    
		    output.setSuccess(1);
		    output.setLogId(responseJson.get("log_id").toString());
		    output.setWorkbookName(workbook.get("name").toString());
		    output.setPageId(page.get("_id").toString());
		    output.setPageNum(page.get("page_num").toString());
		    output.setBoxedUrl(ConnectionConfig.SCORING_SERVICE_URL+responseJson.get("boxed_url").toString());
		    JSONArray prediction = (JSONArray) responseJson.get("predictions");
		    for(int i = 0; i < prediction.size(); i++) {
		    	JSONObject slice = (JSONObject) prediction.get(i);
		    	JSONArray answers = (JSONArray) slice.get("answers");
		    	StringJoiner sj = new StringJoiner(", ");
		    	for(Object o : answers) {
		    		sj.add(o.toString());
		    	}
		    	list.add(new Recognition(slice.get("prob_num").toString(), sj.toString()));
		    }

		    br.close();
		    conn.disconnect();

		} catch (Exception e) {
			output.setSuccess(0);
			list.add(new Recognition("Error", "Exception occured. imgUrl: "+input.getImgUrl()));
		}
		output.setRecognitionList(list);

		return output;  
	}
	
	@SuppressWarnings("unchecked")
	@EndpointMapping(mapping = "자동채점.정답확인", description = "타임교육 튜터봇 자동채점 정답 확인")
	public ResultOutput scoring(Submit input) {
		
		HttpURLConnection conn = null;
		ResultOutput output = new ResultOutput();
		
		try {
			JSONParser parser = new JSONParser();
			Object obj = parser.parse(input.getSubmit());
		    JSONObject reqBody = (JSONObject) obj;
		    reqBody.put("user_id", input.getUserId());
		    
			URL url = new URL(ConnectionConfig.SCORING_SERVICE_URL+"api/v1/infer/score");
			conn = (HttpURLConnection) url.openConnection();
			conn.setRequestMethod("POST");
			conn.setRequestProperty("Content-Type", "application/json");
			conn.setRequestProperty("Accept", "application/json");
			conn.setDoOutput(true);
			
		    OutputStreamWriter os = new OutputStreamWriter(conn.getOutputStream());
		    os.write(reqBody.toString());
		    os.flush();
		    
		    BufferedReader br = new BufferedReader(new InputStreamReader(conn.getInputStream()));
		    JSONArray responseJson = (JSONArray) JSONValue.parse(br.readLine());
		    StringJoiner sj = new StringJoiner(", ");
		    
		    output.setSuccess(1);
		    output.setHasWrong(0);
		    for(int i = 0; i < responseJson.size(); i++) {
		    	JSONObject slice = (JSONObject) responseJson.get(i);
		    	if(slice.get("correct").toString().equals("0")) {
		    		output.setHasWrong(1);
		    		sj.add(slice.get("prob_num")+"번");
		    	}
		    }
		    output.setWrongAnswer(sj.toString());

		    br.close();
		    conn.disconnect();

		} catch (Exception e) {
			output.setSuccess(0);
			output.setHasWrong(1);
			output.setWrongAnswer("Error: Wrong Submit. submit: "+input.getSubmit());
		}
		return output;	  
	}
}


