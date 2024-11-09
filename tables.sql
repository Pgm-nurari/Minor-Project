-- 1. Department Table
CREATE TABLE Department (
    Dept_ID INT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL
);

-- 2. Role Table
CREATE TABLE Role (
    Role_ID INT PRIMARY KEY,
    Role_Name VARCHAR(50) NOT NULL
);

-- 3. User Table
CREATE TABLE User (
    User_ID INT PRIMARY KEY,
    Username VARCHAR(50) NOT NULL,
    Email VARCHAR(100) NOT NULL UNIQUE,
    Password VARCHAR(255) NOT NULL,
    Role INT,
    FOREIGN KEY (Role) REFERENCES Role(Role_ID)
);

-- 4. Event_Type Table
CREATE TABLE Event_Type (
    Event_Type_ID INT PRIMARY KEY,
    Event_Type_Name VARCHAR(50) NOT NULL
);

-- 5. Event Table
CREATE TABLE Event (
    Event_ID INT PRIMARY KEY,
    User_ID INT,
    Name VARCHAR(100) NOT NULL,
    Event_Type_ID INT,
    Date DATE NOT NULL,
    Days INT NOT NULL,
    Dept_ID INT,
    FOREIGN KEY (User_ID) REFERENCES User(User_ID),
    FOREIGN KEY (Event_Type_ID) REFERENCES Event_Type(Event_Type_ID),
    FOREIGN KEY (Dept_ID) REFERENCES Department(Dept_ID)
);

-- 6. Sub-Event Table
CREATE TABLE Sub_Event (
    Sub_Event_ID INT PRIMARY KEY,
    User_ID INT,
    Name VARCHAR(100) NOT NULL,
    Event_Type_ID INT,
    Date DATE NOT NULL,
    Time TIME NOT NULL,
    Dept_ID INT,
    Event_ID INT,
    FOREIGN KEY (User_ID) REFERENCES User(User_ID),
    FOREIGN KEY (Event_Type_ID) REFERENCES Event_Type(Event_Type_ID),
    FOREIGN KEY (Dept_ID) REFERENCES Department(Dept_ID),
    FOREIGN KEY (Event_ID) REFERENCES Event(Event_ID)
);

-- 7. Transaction_Nature Table
CREATE TABLE Transaction_Nature (
    Nature_ID INT PRIMARY KEY,
    Nature_Name VARCHAR(50) NOT NULL
);

-- 8. Payment_Mode Table
CREATE TABLE Payment_Mode (
    Mode_ID INT PRIMARY KEY,
    Mode_Name VARCHAR(50) NOT NULL
);

-- 9. Transaction_Category Table
CREATE TABLE Transaction_Category (
    Transaction_Category_ID INT PRIMARY KEY,
    Category_Name VARCHAR(100) NOT NULL
);

-- 10. Account_Category Table
CREATE TABLE Account_Category (
    Account_Category_ID INT PRIMARY KEY,
    Category_Name VARCHAR(100) NOT NULL
);

-- 11. Individual Event Transaction Table
CREATE TABLE Individual_Event_Transaction (
    Transaction_ID INT PRIMARY KEY,
    User_ID INT,
    Event_ID INT,
    Amount DECIMAL(10, 2) NOT NULL,
    Nature_ID INT,
    Mode_ID INT,
    Date DATE NOT NULL,
    Description TEXT,
    Bill_No VARCHAR(50),
    Party_Name VARCHAR(100),
    Transaction_Category_ID INT,
    Account_Category_ID INT,
    FOREIGN KEY (User_ID) REFERENCES User(User_ID),
    FOREIGN KEY (Event_ID) REFERENCES Event(Event_ID),
    FOREIGN KEY (Nature_ID) REFERENCES Transaction_Nature(Nature_ID),
    FOREIGN KEY (Mode_ID) REFERENCES Payment_Mode(Mode_ID),
    FOREIGN KEY (Transaction_Category_ID) REFERENCES Transaction_Category(Transaction_Category_ID),
    FOREIGN KEY (Account_Category_ID) REFERENCES Account_Category(Account_Category_ID)
);

-- 12. Financial Statement Table
CREATE TABLE Financial_Statement (
    Statement_ID INT PRIMARY KEY,
    Event_ID INT,
    Statement_Name VARCHAR(50) NOT NULL,
    FOREIGN KEY (Event_ID) REFERENCES Event(Event_ID)
);

-- 13. Profit and Loss Table
CREATE TABLE Profit_and_Loss (
    Statement_ID INT,
    Particular VARCHAR(100) NOT NULL,
    Nature_ID INT,
    Amount DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (Statement_ID) REFERENCES Financial_Statement(Statement_ID),
    FOREIGN KEY (Nature_ID) REFERENCES Transaction_Nature(Nature_ID)
);

-- 14. Balance Sheet Table
CREATE TABLE Balance_Sheet (
    Statement_ID INT,
    Liabilities_and_Equities VARCHAR(100),
    Assets VARCHAR(100),
    Amount DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (Statement_ID) REFERENCES Financial_Statement(Statement_ID)
);

