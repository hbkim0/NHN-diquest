package lai.module.starter.endpoint.timeedu.model;

import com.diquest.lai.module.Param;

public class HomeworkInput {
	@Param(description = "아이디", required = true, sample = "ai01")
	private String userId;

	public String getUserId() {
		return userId;
	}
	
	public void setUserId(String userId) {
		this.userId = userId;
	}

}
