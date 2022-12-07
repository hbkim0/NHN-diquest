package lai.module.starter.endpoint.timeedu;

import org.json.simple.JSONObject;
import org.json.simple.JSONValue;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLEncoder;

import com.diquest.lai.module.Endpoint;
import com.diquest.lai.module.EndpointMapping;

import lai.module.starter.config.ConnectionConfig;
import lai.module.starter.endpoint.timeedu.model.ExplanationInput;
import lai.module.starter.endpoint.timeedu.model.ExplanationOutput;

@Endpoint
public class ExplanationEndpoint {
	
	@EndpointMapping(mapping = "해설", description = "타임교육 튜터봇 해설 이미지")
	public ExplanationOutput output(ExplanationInput input) {
		
		HttpURLConnection conn = null;
		ExplanationOutput output = new ExplanationOutput();
		try {

		    String bookTitle = URLEncoder.encode(input.getBookTitle(), "utf-8");
		    String page = URLEncoder.encode(input.getPage(), "utf-8");
		    String problem = URLEncoder.encode(input.getProblem(), "utf-8");
		    
			URL url = new URL(ConnectionConfig.SCORING_SERVICE_URL+"api/v1/problems/explain?workbook_name="+bookTitle+"&page_num="+page+"&prob_num="+problem);
			conn = (HttpURLConnection) url.openConnection();
			conn.setRequestMethod("GET");
			conn.setRequestProperty("Accept", "application/json");
			conn.setConnectTimeout(3000);
			conn.setReadTimeout(3000);
			conn.setDoOutput(true);
		    
		    BufferedReader br = new BufferedReader(new InputStreamReader(conn.getInputStream()));
		    JSONObject responseJson = (JSONObject) JSONValue.parse(br.readLine());
		    output.setSuccess(1);
		    output.setSolvingUrl(ConnectionConfig.SCORING_SERVICE_URL+responseJson.get("solving_url").toString());
		    output.setSimilarUrl(ConnectionConfig.SCORING_SERVICE_URL+responseJson.get("similar_url").toString());

		    br.close();
		    conn.disconnect();

		} catch (Exception e) {
			output.setSuccess(0);
			output.setSolvingUrl("Error: Exception occured. bookTitle: "+input.getBookTitle()+", page: "+input.getPage()+", problem: "+input.getProblem());
		}
	
		return output;
	}
}
