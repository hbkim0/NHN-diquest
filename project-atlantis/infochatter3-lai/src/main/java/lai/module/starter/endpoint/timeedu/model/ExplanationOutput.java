package lai.module.starter.endpoint.timeedu.model;

import com.diquest.lai.module.Param;

public class ExplanationOutput {
	
	@Param(description = "응답 성공", required = true)
	private int success;
	
	@Param(description = "문제 해설 URL", required = true)
	private String solvingUrl;
	
	@Param(description = "유사 문제 URL", required = true)
	private String similarUrl;
	
	public void setSuccess(int success) {
		this.success = success;
	}
	
	public void setSolvingUrl(String solvingUrl) {
		this.solvingUrl = solvingUrl;
	}
	
	public void setSimilarUrl(String similarUrl) {
		this.similarUrl = similarUrl;
	}

}
