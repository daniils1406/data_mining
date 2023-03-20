package connection;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class PostgresProvider {
    public static Connection getConnection() {
        try {
            Class.forName(PostgresProperties.DRIVER);
        } catch (ClassNotFoundException e) {
            throw new RuntimeException(e);
        }
        Connection connection;
        try {
            connection= DriverManager.getConnection(PostgresProperties.URL, PostgresProperties.USERNAME, PostgresProperties.PASSWORD);
        } catch (SQLException e) {
            throw new RuntimeException(e);
        }
        return connection;
    }
}