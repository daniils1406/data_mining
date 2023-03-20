import com.fasterxml.jackson.databind.ObjectMapper;
import connection.PostgresProvider;
import lombok.SneakyThrows;


import java.io.IOException;
import java.net.*;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.sql.Connection;

import java.sql.Statement;

import java.util.LinkedList;
import java.util.List;



public class Main {


    static Connection connection = PostgresProvider.getConnection();
    static ObjectMapper mapper = new ObjectMapper();



    public static List<String> getFriendsOfSomeUser(String idOfUser) throws IOException, InterruptedException {
        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create("https://api.vk.com/method/friends.get?user_id=" + idOfUser + "&access_token=vk1.a.pTujU8aFCFLx6ptR1n35yVJ7A3BJ4cj09o_4XOr4xVhZgoG-DsWGrlLj3WMH2rMj7GKZKKZCAi5CHN_FG6b4ng6wLoxi4sNVr6UNwy1GPsTAQnjOuF35oOMj0ItIla0usQY8pyrAp-OBcC66ZSDgyx9q62SiwB2A9KWUEJWTj7LvzON52sJc5i9rY0yInJgQ&v=5.131"))
                .GET()
                .build();
        HttpResponse response = client.send(request, HttpResponse.BodyHandlers.ofString());
        String string = response.body().toString();
        Friends friends = mapper.readValue(string.substring(12, string.length() - 1), Friends.class);
        return friends.getItems();
    }

    @SneakyThrows
    public static void main(String[] args) {


        Statement statement = connection.createStatement();


        List<String> friendsLevel1 = getFriendsOfSomeUser("159783779");
        for (int i = 0; i < friendsLevel1.size(); i++) {
            List<String> friendsLevel2=new LinkedList<>();
            try {
                friendsLevel2 = getFriendsOfSomeUser(friendsLevel1.get(i));
            } catch (Exception e) {
            }
            if(friendsLevel2!=null){
                for (int j = 0; j < friendsLevel2.size(); j++) {
                    List<String> friendsLevel3=new LinkedList<>();
                    try {
                        friendsLevel3 = getFriendsOfSomeUser(friendsLevel2.get(j));
                    } catch (Exception e) {
                    }
                    if(friendsLevel3!=null){
                        for (int q = 0; q < friendsLevel3.size(); q++) {
                            String sqlInsert = "INSERT INTO friends VALUES (" + friendsLevel2.get(j) + "," + friendsLevel3.get(q) + ")";
                            statement.execute(sqlInsert);
                        }
                        String sqlInsert = "INSERT INTO friends VALUES (" + friendsLevel1.get(i) + "," + friendsLevel2.get(j) + ")";
                        statement.execute(sqlInsert);
                    }
                }
            }

            String sqlInsert = "INSERT INTO friends VALUES (" + 159783779 + "," + friendsLevel1.get(i) + ")";
            statement.execute(sqlInsert);
            System.out.println("159783779 "+friendsLevel1.get(i));
        }

//        List<String> friendsLevel1 = getFriendsOfSomeUser("159783779");
//        for (int i = 0; i < friendsLevel1.size(); i++) {
//            List<String> friendsLevel2 = null;
//            try {
//                friendsLevel2 = getFriendsOfSomeUser(friendsLevel1.get(i));
//            } catch (Exception e) {
//            }
//            if(friendsLevel2!=null){
//                for (int j = 0; j < friendsLevel2.size(); j++) {
//                    String sqlInsert = "INSERT INTO friends VALUES (" + friendsLevel1.get(i) + "," + friendsLevel2.get(j) + ")";
//                    statement.execute(sqlInsert);
//                }
//            }
//            String sqlInsert = "INSERT INTO friends VALUES (" + 159783779 + "," + friendsLevel1.get(i) + ")";
//            statement.execute(sqlInsert);
//        }


//        ResultSet resultSet=statement.executeQuery("select DISTINCT friend FROM friends");

//        ResultSet resultSet=statement.executeQuery("select DISTINCT VKuser FROM friends");
//        List<String> allUsers=new LinkedList<>();
//        while (resultSet.next()){
//            allUsers.add(resultSet.getString("VKuser"));
//        }
//        System.out.println(allUsers.size());
//        for(int i=0;i<allUsers.size();i++){
//            ResultSet resultSetOfAllFriends=statement.executeQuery("SELECT count(*) FROM friends where VKuser='"+allUsers.get(i)+"'");
//            resultSetOfAllFriends.next();
//            String countOfFriends=resultSetOfAllFriends.getString("count");
//            ResultSet resultSetOfAllReferences=statement.executeQuery("SELECT count(*) FROM friends where friend='"+allUsers.get(i)+"'");
//            resultSetOfAllReferences.next();
//
//            statement.execute("INSERT INTO data VALUES ("+allUsers.get(i)+", "+countOfFriends+","+resultSetOfAllReferences.getString("count")+")");
//        }
    }

}
