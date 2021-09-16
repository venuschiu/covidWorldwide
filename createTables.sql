CREATE TABLE country_dim (
    ID int NOT NULL,
    country_name varchar(255) NOT NULL,      
    CONSTRAINT PK_Person PRIMARY KEY (ID)
); 

CREATE TABLE date_dim (
    ID int NOT NULL,
    LastName varchar(255) NOT NULL,
    FirstName varchar(255),
    Age int,
    CONSTRAINT PK_Person PRIMARY KEY (ID)
); 
