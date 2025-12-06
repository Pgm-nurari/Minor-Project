-- FinSight Dummy Data Insertion Script
-- This script populates the database with test data

USE finsight_db;

-- Clear existing data (in reverse order of dependencies)
SET FOREIGN_KEY_CHECKS = 0;

TRUNCATE TABLE transactionitem;
TRUNCATE TABLE transaction_table;
TRUNCATE TABLE Budget;
TRUNCATE TABLE Sub_Event;
TRUNCATE TABLE Event;
TRUNCATE TABLE User;
TRUNCATE TABLE Department;
TRUNCATE TABLE Role;
TRUNCATE TABLE Event_Type;
TRUNCATE TABLE Transaction_Nature;
TRUNCATE TABLE Payment_Mode;
TRUNCATE TABLE Transaction_Category;
TRUNCATE TABLE Account_Category;

SET FOREIGN_KEY_CHECKS = 1;

-- 1. Insert Departments
INSERT INTO Department (Dept_ID, Name) VALUES
(1, 'Computer Science'),
(2, 'Commerce'),
(3, 'Visual Media'),
(4, 'Management'),
(5, 'Engineering');

-- 2. Insert Roles
INSERT INTO Role (Role_ID, Role_Name) VALUES
(101, 'Admin'),
(102, 'Event Manager'),
(103, 'Finance Manager');

-- 3. Insert Event Types
INSERT INTO Event_Type (Event_Type_ID, Event_Type_Name) VALUES
(1, 'Conference'),
(2, 'Workshop'),
(3, 'Seminar'),
(4, 'Cultural Event'),
(5, 'Sports Event');

-- 4. Insert Transaction Natures
INSERT INTO Transaction_Nature (Nature_ID, Nature_Name) VALUES
(1, 'Revenue'),
(2, 'Expense');

-- 5. Insert Payment Modes
INSERT INTO Payment_Mode (Mode_ID, Mode_Name) VALUES
(1, 'Cash'),
(2, 'UPI'),
(3, 'Credit Card'),
(4, 'Debit Card'),
(5, 'Bank Transfer'),
(6, 'Cheque');

-- 6. Insert Transaction Categories
INSERT INTO Transaction_Category (Transaction_Category_ID, Category_Name) VALUES
(1, 'Registration Fees'),
(2, 'Sponsorship'),
(3, 'Venue Rental'),
(4, 'Equipment Rental'),
(5, 'Marketing'),
(6, 'Refreshments'),
(7, 'Prizes'),
(8, 'Staff Payments'),
(9, 'Miscellaneous');

-- 7. Insert Account Categories
INSERT INTO Account_Category (Account_Category_ID, Category_Name) VALUES
(1, 'Assets'),
(2, 'Liabilities'),
(3, 'Income'),
(4, 'Expenses'),
(5, 'Equity');

-- 8. Insert Users (Passwords are hashed for 'Password@123')
-- Note: Replace these with actual hashed passwords from werkzeug.security
INSERT INTO User (Username, Email, Password, Role, Dept_ID, Verified) VALUES
('Admin User', 'admin@finsight.com', 'scrypt:32768:8:1$YK4GvXmZR2wkLMaA$0e3d8a1e2f3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2', 101, 1, 1),
('John Doe', 'john.doe@finsight.com', 'scrypt:32768:8:1$YK4GvXmZR2wkLMaA$0e3d8a1e2f3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2', 102, 1, 1),
('Jane Smith', 'jane.smith@finsight.com', 'scrypt:32768:8:1$YK4GvXmZR2wkLMaA$0e3d8a1e2f3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2', 103, 2, 1),
('Mike Johnson', 'mike.johnson@finsight.com', 'scrypt:32768:8:1$YK4GvXmZR2wkLMaA$0e3d8a1e2f3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2', 102, 3, 1),
('Sarah Williams', 'sarah.williams@finsight.com', 'scrypt:32768:8:1$YK4GvXmZR2wkLMaA$0e3d8a1e2f3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2', 103, 4, 1),
('David Brown', 'david.brown@finsight.com', 'scrypt:32768:8:1$YK4GvXmZR2wkLMaA$0e3d8a1e2f3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2', 102, 5, 1),
('Emily Davis', 'emily.davis@finsight.com', 'scrypt:32768:8:1$YK4GvXmZR2wkLMaA$0e3d8a1e2f3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2', 103, 1, 1),
('Chris Wilson', 'chris.wilson@finsight.com', 'scrypt:32768:8:1$YK4GvXmZR2wkLMaA$0e3d8a1e2f3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2', 102, 2, 0);

-- 9. Insert Events
INSERT INTO Event (Finance_Manager, Event_Manager, Name, Event_Type_ID, Date, Days, Dept_ID) VALUES
(3, 2, 'Tech Summit 2025', 1, '2025-01-15', 2, 1),
(5, 4, 'Photography Workshop', 2, '2025-02-20', 1, 3),
(7, 6, 'Innovation Conference', 1, '2025-03-10', 3, 5),
(3, 2, 'AI & ML Seminar', 3, '2024-12-01', 1, 1),
(5, 4, 'Cultural Fest 2025', 4, '2025-04-15', 5, 3);

-- 10. Insert Sub-Events
INSERT INTO Sub_Event (Sub_Event_Manager, Name, Event_Type_ID, Date, Time, Dept_ID, Event_ID) VALUES
(2, 'Keynote Speech', 3, '2025-01-15', '09:00:00', 1, 1),
(2, 'Panel Discussion', 3, '2025-01-15', '14:00:00', 1, 1),
(4, 'Basic Photography', 2, '2025-02-20', '10:00:00', 3, 2),
(4, 'Advanced Editing', 2, '2025-02-20', '15:00:00', 3, 2),
(6, 'Startup Pitches', 1, '2025-03-10', '11:00:00', 5, 3);

-- 11. Insert Budgets
INSERT INTO Budget (Amount, Notes, Event_ID, Sub_Event_ID) VALUES
(150000.00, 'Total budget for Tech Summit', 1, NULL),
(50000.00, 'Budget for Photography Workshop', 2, NULL),
(200000.00, 'Innovation Conference Budget', 3, NULL),
(30000.00, 'Budget for keynote speaker', NULL, 1),
(20000.00, 'Panel discussion expenses', NULL, 2);

-- 12. Insert Transactions for Event 1 (Tech Summit)
INSERT INTO transaction_table (User_ID, Event_ID, Sub_Event_ID, Bill_No, Party_Name, Nature_ID, Mode_ID, Date, Transaction_Category_ID, Account_Category_ID) VALUES
(2, 1, NULL, 'INV001', 'Tech Corp Sponsorship', 1, 5, '2024-12-15', 2, 3),
(2, 1, NULL, 'INV002', 'Student Registrations', 1, 2, '2024-12-20', 1, 3),
(2, 1, NULL, 'BILL001', 'Convention Center', 2, 6, '2024-12-10', 3, 4),
(2, 1, 1, 'BILL002', 'Dr. Smith (Speaker)', 2, 5, '2024-12-12', 8, 4),
(2, 1, NULL, 'BILL003', 'Marketing Agency', 2, 3, '2024-12-18', 5, 4);

-- 13. Insert Transaction Items
INSERT INTO transactionitem (Transaction_ID, Description, Amount) VALUES
(1, 'Gold Sponsorship Package', 50000.00),
(2, 'Early Bird Registrations (50 students)', 25000.00),
(2, 'Regular Registrations (30 students)', 18000.00),
(3, 'Venue rental for 2 days', 35000.00),
(3, 'Audio/Visual equipment', 15000.00),
(4, 'Keynote speaker fee', 25000.00),
(4, 'Travel and accommodation', 8000.00),
(5, 'Social media campaign', 12000.00),
(5, 'Print materials', 5000.00);

-- 14. Insert Transactions for Event 2 (Photography Workshop)
INSERT INTO transaction_table (User_ID, Event_ID, Sub_Event_ID, Bill_No, Party_Name, Nature_ID, Mode_ID, Date, Transaction_Category_ID, Account_Category_ID) VALUES
(4, 2, NULL, 'INV003', 'Workshop Registration Fees', 1, 2, '2025-01-10', 1, 3),
(4, 2, NULL, 'BILL004', 'Camera Equipment Rental', 2, 1, '2025-01-15', 4, 4),
(4, 2, 3, 'BILL005', 'Professional Photographer Fee', 2, 5, '2025-02-18', 8, 4);

-- 15. Insert Transaction Items for Event 2
INSERT INTO transactionitem (Transaction_ID, Description, Amount) VALUES
(6, 'Workshop registration (20 participants)', 30000.00),
(7, 'DSLR cameras (5 units)', 8000.00),
(7, 'Lighting equipment', 4000.00),
(8, 'Workshop instructor fee', 15000.00);

-- 16. Insert Transactions for Event 4 (Completed Event - AI & ML Seminar)
INSERT INTO transaction_table (User_ID, Event_ID, Sub_Event_ID, Bill_No, Party_Name, Nature_ID, Mode_ID, Date, Transaction_Category_ID, Account_Category_ID) VALUES
(2, 4, NULL, 'INV004', 'Seminar Registrations', 1, 2, '2024-11-15', 1, 3),
(2, 4, NULL, 'BILL006', 'Seminar Hall Booking', 2, 5, '2024-11-20', 3, 4),
(2, 4, NULL, 'BILL007', 'Refreshments', 2, 1, '2024-12-01', 6, 4),
(2, 4, NULL, 'BILL008', 'Certificates Printing', 2, 1, '2024-11-25', 9, 4);

-- 17. Insert Transaction Items for Event 4
INSERT INTO transactionitem (Transaction_ID, Description, Amount) VALUES
(9, 'Student registrations (40 students)', 20000.00),
(10, 'Seminar hall for 1 day', 8000.00),
(11, 'Tea and snacks for 50 people', 3500.00),
(12, 'Participation certificates (50 pcs)', 2000.00);

-- Display summary
SELECT 'Dummy data insertion completed!' AS Status;
SELECT 'Departments:', COUNT(*) FROM Department;
SELECT 'Roles:', COUNT(*) FROM Role;
SELECT 'Users:', COUNT(*) FROM User;
SELECT 'Events:', COUNT(*) FROM Event;
SELECT 'Sub-Events:', COUNT(*) FROM Sub_Event;
SELECT 'Transactions:', COUNT(*) FROM transaction_table;
SELECT 'Transaction Items:', COUNT(*) FROM transactionitem;
