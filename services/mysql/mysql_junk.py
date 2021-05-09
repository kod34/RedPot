#!/usr/bin/python3

import mysql.connector
from faker import Faker
from datetime import datetime
from datetime import date
import random
import hashlib
import json

lines = open('/etc/mysql/debian.cnf').read().splitlines()
line3 = lines[3]
line4 = lines[4]
sqluname=line3[11:]
sqlpassword=line4[11:]

countries = ['it_IT', 'en_US', 'ja_JP', 'en_GB', 'en_AU', 'en_CA', 'fr_FR', 'en_NZ', 'es.ES', 'pl_PL', 'en_TH']

myconn = mysql.connector.connect(
   host = "localhost",
   user = sqluname,
   passwd = sqlpassword,
   )

mycursor = myconn.cursor()

db1 = "Bootstrap" 

mycursor.execute("DROP DATABASE IF EXISTS "+db1) # To avoid errors
mycursor.execute("CREATE DATABASE "+db1)

mydb1 = mysql.connector.connect(
   host = "localhost",
   user = sqluname,
   passwd = sqlpassword,
   database =  db1
   )

mycursordb1 = mydb1.cursor()

#Customers
mycursordb1.execute("""CREATE TABLE Customers(
   `CustomerID` varchar(120) NOT NULL,
   `ContactName` varchar(120),
   `Address` varchar(120),
   `Company` varchar(120),
   `City` varchar(120),
   `Country` varchar(120),
   `Phone` varchar(120),
   `Email` varchar(120),
   `Password` varchar(120),
   `CreditCard` varchar(120),
   `CreditCardExpireDate` DATE,
   PRIMARY KEY (`CustomerID`),
   INDEX (`City`)
   )"""
   )

sqlcustomers = """INSERT INTO Customers (CustomerID, ContactName, Address, Company, City, Country, Phone, Email, Password, CreditCard, CreditCardExpireDate)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s)"""

valcustomers = []

for x in range(235):
   country1 = Faker(random.choice(countries))
   valcustomers.append((str(country1.random_int())+str(country1.random_int()),
      country1.first_name()+" "+country1.last_name(),
      country1.address(),
      country1.company(),
      country1.city(),
      country1.country(),
      country1.phone_number(),
      country1.ascii_email(),
      hashlib.md5(country1.password().encode('utf-8')).hexdigest(),
      country1.credit_card_number(),
      country1.date_between_dates(date_start=datetime(2015,1,1), date_end=datetime(2025,1,1))
      )
   )

mycursordb1.executemany(sqlcustomers, valcustomers)

#Developers
mycursordb1.execute("""CREATE TABLE `Developers` (
   `EmployeeID`      varchar(120)         NOT NULL,
   `LastName`        varchar(120)         NOT NULL,
   `FirstName`       varchar(120)         NOT NULL,
   `BirthDate`       DATE,
   `HireDate`        DATE,
   `Address`         varchar(120),
   `City`            varchar(120),
   `PostalCode`      varchar(120),
   `Country`         varchar(120),
   `HomePhone`       varchar(120),
   `Salary`          INT,
   `Email`           varchar(120),
   `Password`        varchar(120),
   INDEX (`LastName`),
   INDEX (`PostalCode`),
   PRIMARY KEY (`EmployeeID`)
   )"""
   )

sqldevelopers = """INSERT INTO Developers (
EmployeeID,
LastName,
FirstName,
BirthDate,
HireDate,
Address,
City,
PostalCode,
Country,
HomePhone,
Salary,
Email,
Password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

valdevelopers = []

for x in range(21):
   country2 = Faker(random.choice(countries))
   valdevelopers.append((str(country2.random_int())+str(country2.random_int()),
      country2.last_name(),
      country2.first_name(),
      country2.date_between_dates(date_start=datetime(1980,1,1),date_end=datetime(2000,12,31)),
      country2.date_between_dates(date_start=datetime(2011,1,1), date_end=date.today()),
      country2.address(),
      country2.city(),
      country2.postcode(),
      country2.country(),
      country2.phone_number(),
      country2.random_int(),
      country2.ascii_email(),
      hashlib.md5(country2.password().encode('utf-8')).hexdigest()
      )
   )

mycursordb1.executemany(sqldevelopers, valdevelopers)

#Suppliers
mycursordb1.execute("""CREATE TABLE `Suppliers` (
   `SupplierID`  varchar(120) NOT NULL,
   `CompanyName` varchar(120) NOT NULL,
   `ContactName` varchar(120),
   `Address` varchar(120),
   `City` varchar(120),
   `PostalCode` varchar(120),
   `Country` varchar(120),
   `Phone` varchar(120),
   `HomePage` TEXT,
    PRIMARY KEY (`SupplierID`),
    INDEX (`CompanyName`),
    INDEX (`PostalCode`)
    )"""
    )

sqlsuppliers = """INSERT INTO Suppliers (SupplierID, CompanyName, ContactName, Address, City, PostalCode, Country, Phone, HomePage)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""

valsuppliers = []

for x in range(11):
   country3 = Faker(random.choice(countries))
   valsuppliers.append((str(country3.random_int())+str(country3.random_int()),
      country3.company(),
      country3.first_name()+" "+country3.last_name(),
      country3.address(),
      country3.city(),
      country3.postcode(),
      country3.country(),
      country3.phone_number(),
      country3.uri_page()
      )
   )

mycursordb1.executemany(sqlsuppliers, valsuppliers)

#Products
mycursordb1.execute("""CREATE TABLE `Products` (
   `ProductID` SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
   `ProductName` varchar(120) NOT NULL,
   `SupplierID`  varchar(120) NOT NULL,
   `QuantityPerUnit`varchar(120),
   `UnitPrice` DECIMAL(10,2) UNSIGNED DEFAULT 0,
   `UnitsInStock` SMALLINT  DEFAULT 0,
   `UnitsOnOrder` SMALLINT UNSIGNED DEFAULT 0,
   `Discontinued` BOOLEAN NOT NULL DEFAULT FALSE,
   PRIMARY KEY (`ProductID`),
   INDEX (`ProductName`)
   )"""
   )

sqlproducts = """INSERT INTO Products(
ProductName,
SupplierID,
QuantityPerUnit,
UnitPrice,
UnitsInStock,
UnitsOnOrder,
Discontinued
)
VALUES (%s, %s, %s, %s, %s, %s, %s)"""

valproducts = []

products = json.loads(open('services/mysql/Products.json').read())

for product in products:
   valproducts.append((product,
      str(Faker().random_int())+str(Faker().random_int()),
      Faker().pyint(min_value=10, max_value=32),
      random.choice(range(499, 999999, 10))/100,
      Faker().pyint(min_value=20, max_value=120),
      Faker().pyint(min_value=5, max_value=20),
      Faker().boolean()
   )
   )

mycursordb1.executemany(sqlproducts, valproducts)

#shippers
mycursordb1.execute("""CREATE TABLE `Shippers` (
   `ShipperID` VARCHAR(120)  NOT NULL ,
   `CompanyName` varchar(120) NOT NULL,
   `Phone` varchar(120),
   PRIMARY KEY (`ShipperID`)
   )"""
   )

sqlshippers = """INSERT INTO Shippers (ShipperID, CompanyName, Phone)
VALUES (%s, %s, %s)"""

valshippers = []

for x in range(4):
   country4 = Faker(random.choice(countries))
   valshippers.append((country4.random_int(),
      country4.company(),
      country4.phone_number()
      )
   )


mycursordb1.executemany(sqlshippers, valshippers)

#Orders
mycursordb1.execute("""CREATE TABLE `Orders` (
   `OrderID`        varchar(120) NOT NULL ,
   `CustomerID`     varchar(120),
   `OrderDate`      DATE,
   `ShipVia`        VARCHAR(120),
   `ShipName`       varchar(120),
   `ShipAddress`    varchar(120),
   `ShipCity`       varchar(120),
   `ShipPostalCode` varchar(120),
   `ShipCountry`    varchar(120),
   PRIMARY KEY (`OrderID`),
   INDEX (`OrderDate`),
   INDEX (`ShipPostalCode`)
   )"""
   )

sqlorders = """INSERT INTO Orders(
OrderID,
CustomerID,
OrderDate,
ShipVia,
ShipName,
ShipAddress,
ShipCity,
ShipPostalCode,
ShipCountry
)VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""

valorders = []

for x in range(114):
   country5 = Faker(random.choice(countries))
   valorders.append(
      (str(country5.random_int())+str(country5.random_int()),
      str(country5.random_int())+str(country5.random_int()),
      country5.date_between_dates(date_start=datetime(2009,1,1),date_end=date.today()),
      str(country5.random_int())+str(country5.random_int()),
      country5.first_name()+" "+country5.last_name(),
      country5.address(),
      country5.city(),
      country5.postcode(),
      country5.country()
      )
   )

mycursordb1.executemany(sqlorders, valorders)


#OrderDetails
mycursordb1.execute("""CREATE TABLE `OrderDetails` (
   `OrderID`   varchar(120)           NOT NULL ,
   `ProductID` SMALLINT UNSIGNED      NOT NULL,
   `UnitPrice` REAL     UNSIGNED  NOT NULL DEFAULT 999999.99,
   `Quantity`  SMALLINT(2) UNSIGNED   NOT NULL DEFAULT 1,
   `Discount`  varchar(3)             NOT NULL DEFAULT 0, 
   PRIMARY KEY (`OrderID`, `ProductID`)
   )"""
   )

sqldetails = """INSERT INTO OrderDetails (OrderID, ProductID, UnitPrice, Quantity, Discount)
VALUES (%s, %s, %s, %s, %s)"""

valdetails = []

for x in range(114):
   country6 = Faker(random.choice(countries))
   valdetails.append((
      str(country6.random_int())+str(country6.random_int()),
      country6.pyint(min_value=1, max_value=76),
      random.choice(range(499, 9999, 10))/10,
      country6.pyint(min_value=1, max_value=10),
      str(country6.pyint(min_value=0, max_value=30, step=5))+"%"
      )
   )


mycursordb1.executemany(sqldetails, valdetails)

mydb1.commit()
