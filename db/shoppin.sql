create table UserStates(
    UserStateID int primary key,
    UserStates varchar(255) not null
);

insert into UserStates values(1,"Active");
insert into UserStates values(2,"Inactive");
insert into UserStates values(3,"Banned");
insert into UserStates values(4,"Blocked");

create table Users(
    UserName varchar(255) primary key,
    UserPassword varchar(255) not null,
    Email varchar(255) unique,
    Phone varchar(255) unique,
    UserStateID int references UserStates(UserStateID) 
);

insert into Users values("testuser","test123","test@mail.com","0987654321",1);

create table UserAddress(
    UserName varchar(255) references Users(UserName),
    UserAddress varchar(255),
    AddressPriority varchar(255),
    AddressDescription varchar(255),
    primary key(UserName,UserAddress)
);

create table Admins(
    AdminName varchar(255) primary key,
    UserName varchar(255) references Users(UserName)
);

create table Sellers(
    SellerName varchar(255) primary key,
    UserName varchar(255) references Users(UserName)
);

insert into Sellers values("Shoppin Seller","testuser");

create table Shops(
    ShopName varchar(255) primary key,
    SellerName varchar(255) references Sellers(SellerName)
);

insert into Shops values("Shoppin Shop","Shoppin Seller");

create table Products(
    ProductID int primary key,
    ProductName varchar(255),
    ShopName varchar(255) references Shops(ShopName),
    ProductType varchar(255),
    ProductDescription varchar(255),
    Storage int,
    Price int
);

insert into Products values(1159142,"Agile Web Development with Rails","Shoppin Shop","Books","This is Description",80,849);
insert into Products values(2375753,"Flask Web Development","Shoppin Shop","Books","This is Description",21,576);
insert into Products values(643503,"CakePHP Application Development","Shoppin Shop","Books","This is Description",90,2141);
insert into Products values(547307,"Alex Homer, ASP.NET 2.0 Visual Web Developer 2005","Shoppin Shop","Books","This is Description",80,849);
insert into Products values(1431415,"PHP Oracle Web Development","Shoppin Shop","Books","This is Description",321,1111);
insert into Products values(2166584,"WordPress for Web Developers: An Introduction for Web Professionals","Shoppin Shop","Books","This is Description",11,3123);
insert into Products values(643521,"MODx Web Development","Shoppin Shop","Books","This is Description",551,312);
insert into Products values(682493,"Grok 1.0 Web Development","Shoppin Shop","Books","This is Description",31,3789);
insert into Products values(682507,"Professional JavaScript for Web Developers","Shoppin Shop","Books","This is Description",66,789);
insert into Products values(740977,"Art of Java Web Development: Struts, Tapestry, Commons, Velocity, JUnit, Axis, Cocoon, InternetBeans, WebWork","Shoppin Shop","Books","This is Description",21,576);
insert into Products values(826704,"Agile Web Development with Rails","Shoppin Shop","Books","This is Description",43,575);
insert into Products values(1159094,"Beginning PHP 6, Apache, MySQL 6 Web Development","Shoppin Shop","Books","This is Description",243,954);

create table Buyers(
    BuyerName varchar(255) primary key,
    UserName varchar(255) references Users(UserName)
);

create table Shippers(
    ShipperID int primary key,
    ShipperName varchar(255)
);

create table OrderStates(
    OrderStateID int auto_increment primary key,
    OrderStates varchar(255) not null
);

create table Orders(
    OrderID int,
    ProductID int references Products(ProductID),
    OrderDate varchar(255),
    BuyerName varchar(255) references Buyers(BuyerName),
    SellerName varchar(255) references Sellers(SellerName),
    Quantity int,
    DiscountRate int,
    DiscountType varchar(255),
    primary key(OrderID,ProductID)
);

create table OrderStatusTime(
    OrderStatusTime varchar(255),
    OrderID int references Orders(OrderID),
    OrderStateID int references OrderStates(OrderStateID),
    primary key(OrderStatusTime,OrderID,OrderStateID)
);

create table CartItems(
    TimeAdded varchar(255),
    BuyerName varchar(255) references Buyers(BuyerName),
    ProductID varchar(255) references Products(ProductID),
    Quantity int,
    primary key(TimeAdded,BuyerName,ProductID)
);

create table Reviews(
    BuyerName varchar(255) references Buyers(BuyerName),
    ProductID int references Products(ProductID),
    ReviewDate varchar(255),
    NumStars int,
    Comment varchar(255),
    primary key(BuyerName,ProductID)
);