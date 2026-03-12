 import javax.swing.*; import java.awt.*; import java.awt.event.*; import java.sql.*; import java.util.*; 
// ================= Room (Base Class) ================= 
abstract class Room {     private int roomNumber;     private double price;     private boolean available;     public Room(int roomNumber, double price, boolean available) {         this.roomNumber = roomNumber; 
        this.price = price; 
        this.available = available; 
    } 
    public int getRoomNumber() {         return roomNumber; 
    } 
    public boolean isAvailable() { 
        return available; 
    } 
    public void setAvailable(boolean available) {         this.available = available; 
    } 
    public double getBasePrice() { 
        return price; 
 } 
    public abstract double calculatePrice(int days); 
} 
// ============== Luxury Room (Subclass) ============== class LuxuryRoom extends Room { 
    public LuxuryRoom(int roomNumber, double price, boolean available) {         super(roomNumber, price, available); 
    } 
    @Override     public double calculatePrice(int days) {         return getBasePrice() * days * 1.2; // 20% extra     } 
} 
// ============== Economy Room (Subclass) ============== class EconomyRoom extends Room { 
    public EconomyRoom(int roomNumber, double price, boolean available) {         super(roomNumber, price, available); 
    } 
    @Override     public double calculatePrice(int days) {         return getBasePrice() * days; 
    } 
} 
// ============== Main Application Class ============== public class HotelBookingApp extends JFrame {     private Connection con; 
    private JComboBox<String> roomTypeBox; 
    private JTextField nameField, contactField, daysField;     private JTextArea outputArea;     private ArrayList<Room> rooms;     public HotelBookingApp() {         // Connect to Database         connectDB();         // Initialize room data 
        rooms = new ArrayList<>(); 
        rooms.add(new LuxuryRoom(101, 3000, true));         rooms.add(new LuxuryRoom(102, 3500, true));         rooms.add(new EconomyRoom(201, 1500, true));         rooms.add(new EconomyRoom(202, 1800, true)); 
        // ==== GUI Layout ====         setTitle(" Hotel Booking System - Cherry's App");         setSize(1000, 1000);         setLayout(new BorderLayout());         setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE); 
        // ==== Input Panel ==== 
        JPanel inputPanel = new JPanel(new GridLayout(6, 2, 5, 5)); 
       inputPanel.setBorder(BorderFactory.createTitledBorder("Booking Details"));         inputPanel.add(new JLabel("Customer Name:"));         nameField = new JTextField();         inputPanel.add(nameField);         inputPanel.add(new JLabel("Contact:"));         contactField = new JTextField();         inputPanel.add(contactField);         inputPanel.add(new JLabel("Room Type:")); 
        roomTypeBox = new JComboBox<>(new String[]{"Luxury Room", "Economy Room"}); 
        inputPanel.add(roomTypeBox);         inputPanel.add(new JLabel("No. of Days:"));         daysField = new JTextField();         inputPanel.add(daysField); 
 
JButton bookButton = new JButton("Book Room"); 
        JButton cancelButton = new JButton("Cancel Booking");         JButton viewButton = new JButton("Check Availability");         inputPanel.add(bookButton);         inputPanel.add(cancelButton);         inputPanel.add(viewButton);         // ==== Output Area ====         outputArea = new JTextArea();         outputArea.setEditable(false); 
        JScrollPane scroll = new JScrollPane(outputArea);         add(inputPanel, BorderLayout.NORTH);         add(scroll, BorderLayout.CENTER);         // ==== Button Actions ====         bookButton.addActionListener(e -> bookRoom());         cancelButton.addActionListener(e -> cancelBooking());         viewButton.addActionListener(e -> showAvailableRooms()); 
    } 
    // ================= JDBC Connection 
================= 
    private void connectDB() { 
        try { 
            String url = "jdbc:mysql://localhost:3306/hotel_booking"; 
            String user = "root"; 
            String password = "root"; 
con = DriverManager.getConnection(url, user, password); 
} catch (SQLException e) { 
            JOptionPane.showMessageDialog(this, "Database Connection Failed!", "Error", JOptionPane.ERROR_MESSAGE); 
        } 
    } 
    // ================= Book Room ================= 
    private void bookRoom() { 
        String name = nameField.getText();         String contact = contactField.getText(); 
        int days;         try { 
            days = Integer.parseInt(daysField.getText()); 
        } catch (Exception e) {             outputArea.setText(" Please enter a valid number of days!"); 
            return; 
        } 
        String type = (String) roomTypeBox.getSelectedItem();         Room selected = null;         for (Room r : rooms) { 
            if (r.isAvailable() && ((type.equals("Luxury Room") && r instanceof LuxuryRoom) || 
                    (type.equals("Economy Room") && r instanceof EconomyRoom))) { 
                selected = r;                 break; 
} 
}         if (selected == null) {             outputArea.setText(" No available rooms of this type!"); 
            return; 
        } 
        double totalPrice = selected.calculatePrice(days);         selected.setAvailable(false);         int bookingID = (int) (Math.random() * 10000); 
        try { 
            PreparedStatement ps = con.prepareStatement( 
                    "INSERT INTO bookings VALUES (?, ?, ?, ?, ?, ?)");             ps.setInt(1, bookingID);             ps.setInt(2, selected.getRoomNumber());             ps.setString(3, name);             ps.setString(4, contact);             ps.setInt(5, days);             ps.setDouble(6, totalPrice);             ps.executeUpdate(); 
            ps.close(); 
            outputArea.setText(" Booking Successful!\n\n" 
                    + "Customer: " + name + "\nRoom No: " + selected.getRoomNumber() 
                    + "\nDays: " + days + "\nTotal Price: ₹" + totalPrice); 
        } catch (SQLException e) { 
outputArea.setText(" Database Error: " + e.getMessage()); 
} 
    } 
    // ================= Cancel Booking ================= 
    private void cancelBooking() { 
        String roomNum = JOptionPane.showInputDialog("Enter Room Number to Cancel:");         if (roomNum == null || roomNum.isEmpty()) return; 
        try { 
            int roomNumber = Integer.parseInt(roomNum); 
            PreparedStatement ps = con.prepareStatement( 
                    "DELETE FROM bookings WHERE roomNumber = ?"); 
            ps.setInt(1, roomNumber);             int rows = ps.executeUpdate(); 
            ps.close();             if (rows > 0) {                 for (Room r : rooms) { 
                    if (r.getRoomNumber() == roomNumber) r.setAvailable(true); 
                } 
                outputArea.setText(" Booking canceled for Room " + roomNumber); 
            } else { 
                outputArea.setText(" No booking found for Room " + roomNumber); 
            } 
        } catch (Exception e) {             outputArea.setText(" Error: " + e.getMessage()); 
        } 
    } 
    // ================= Show Availability 
================= 
    private void showAvailableRooms() { 
        StringBuilder sb = new StringBuilder("🏨 Available Rooms:\n");         for (Room r : rooms) { 
            if (r.isAvailable()) { 
                sb.append("Room No: ").append(r.getRoomNumber()) 
                        .append(" | Type: ").append(r instanceof LuxuryRoom ? 
"Luxury" : "Economy") 
                        .append(" | Price per day: ₹").append(r.getBasePrice()) 
                        .append("\n"); 
            } 
        } 
        outputArea.setText(sb.toString()); 
    } 
    // ================= Main Method ================= 
    public static void main(String[] args) {         SwingUtilities.invokeLater(() -> {             new HotelBookingApp().setVisible(true); 
        }); 
    } 
} 

