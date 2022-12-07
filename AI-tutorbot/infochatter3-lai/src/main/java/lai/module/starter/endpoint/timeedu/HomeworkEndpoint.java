package lai.module.starter.endpoint.timeedu;

import java.util.List;
import org.bson.Document;
import org.bson.types.ObjectId;
import static com.mongodb.client.model.Filters.eq;
import com.mongodb.client.MongoClient;
import com.mongodb.client.MongoClients;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;
import com.diquest.lai.module.Endpoint;
import com.diquest.lai.module.EndpointMapping;

import lai.module.starter.config.ConnectionConfig;
import lai.module.starter.endpoint.timeedu.model.HomeworkInput;
import lai.module.starter.endpoint.timeedu.model.HomeworkOutput;

@Endpoint
public class HomeworkEndpoint {

	@EndpointMapping(mapping = "숙제", description = "타임교육 튜터봇 학생 및 숙제 정보")
	public HomeworkOutput output(HomeworkInput input) {

		String url = ConnectionConfig.MONGODB_URL;
		HomeworkOutput output = new HomeworkOutput();
		try (MongoClient mongoClient = MongoClients.create(url)) {
			MongoDatabase database = mongoClient.getDatabase("atlantis");
			MongoCollection<Document> students = database.getCollection("students");
			Document doc = students.find(eq("user_id", input.getUserId())).first();
			
			output.setUserName(doc.get("name").toString());
			output.setBookTitle(doc.get("workbook_name").toString());
			output.setCorrectCount(doc.get("correct_count").toString());
			output.setCorrectCountAll(doc.get("correct_count_all").toString());
			output.setCorrectRate(doc.getInteger("correct_rate"));
			output.setPageDone(doc.get("page_done").toString());
			
			List<Integer> pagesToday = doc.getList("pages_today", Integer.class);
			List<Integer> pagesTomorrow = doc.getList("pages_tomorrow", Integer.class);
			
			// totalPage 하드코딩
			int totalPage = 100;
			if (doc.get("workbook_name").toString().startsWith("팩토")) totalPage = 120;
			else if (doc.get("workbook_name").toString().startsWith("TP")) totalPage = 75;
			int lastPageToday = pagesToday.size() == 0 ? 0 : pagesToday.get(pagesToday.size()-1);
			output.setPageRemained(Integer.toString(totalPage - lastPageToday));
			
			output.setPagesToday(pagesToday.toString().replaceAll("\\[|\\]", ""));
			output.setPagesTodayCount(Integer.toString(pagesToday.size()));
			output.setPagesTomorrow(pagesTomorrow.toString().replaceAll("\\[|\\]", ""));
			output.setPersonType(doc.get("person_type").toString());

		} catch (Exception e) {
			e.printStackTrace();
		}
		return output;
	}
}
