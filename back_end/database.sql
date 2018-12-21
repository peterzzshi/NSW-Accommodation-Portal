-- create domain EmailString as varchar(64) check (value like '%@%');
-- create domain ShortString as varchar(16);
-- create domain MediumString as varchar(64);
-- create domain LongString as varchar(256);
-- drop domain urlstring;
-- create domain URLString as varchar(128) check (value like 'https://%');
-- create domain Item_status as char(1)
-- 	check (value in (
-- 		'S', -- Success
-- 		'A', -- Accept
-- 		'U', -- Unsuccess
-- 		'P' -- Pending
-- ));
-- create domain TextString as varchar(16384);
-- create domain PhoneNumber as varchar(32);

-- create domain Position as decimal(9,6);
-- drop domain Position;

drop table if exists Post;
drop table if exists Unavailable_date;
drop table if exists house_type;
drop table if exists Item_comment;
drop table if exists Message;
drop table if exists Transaction;
drop table if exists bed_type ;
drop table if exists Amenities;
drop table if exists Item_photo;
drop table if exists Item;
drop table if exists user_photo;
drop table if exists User_information;



-- User information table --


create table User_information (
    id                  serial unique,
    email               EmailString unique ,
    password            VARCHAR(32) not null,
    name                varchar(32) not null,
    gender              char(1) check (gender in ('M','F')),
    date_of_birth       date not null,
    self_description    varchar(128),
    create_date         timestamp not null,
    unread_message      int,
    unread_trip         int,
    verified            boolean,
    phone               PhoneNumber,
    primary key         (id, email)
);


insert into User_information(email, password, name, gender, date_of_birth, self_description, create_date, unread_message, unread_trip, verified)
values ('comp9900@cse.com', 'dalaodaiwo', 'test_user1', 'M', '2018-09-03', 'just for test', '2018-09-03', '0', '0','1');
insert into User_information(email, password, name, gender, date_of_birth, self_description, create_date, unread_message, unread_trip, verified)
values ('comp9900_1@cse.com', 'dalaodaiwo', 'test_user2', 'M', '2018-09-03', 'just for test1', '2018-09-03', '0', '0', '1');
insert into User_information (email,
                              password,
                              name,
                              gender,
                              date_of_birth,
                              self_description,
                              create_date,
                              unread_message,
                              unread_trip,
                              verified,
                              phone)
values ('1105958064@qq.com', 'dalaodaiwo', 'hoster', 'F', '2018-09-12', 'public all the house', '2018-09-12', '0', '0', '1', '');


create table user_photo (
    id                  serial,
    user_id             integer references User_information(id) not null,
    position            URLString,
    delete_url          urlstring,
    primary key         (id, user_id)
);

insert into user_photo(user_id, position)
VALUES (3, 'https://a0.muscache.com/im/pictures/20180027/bb9ccce5_original.jpg?aki_policy=large');



-- Amenities index table --
create table Amenities (
    id                  serial,
    name                MediumString,
    primary key         (id)
);

insert into Amenities(name)
values
       ('Wireless Internet'),
       ('Air conditioning'),
       ('TV'),
       ('Laptop friendly workspace'),
       ('Hot water'),
       ('Heating'),
       ('Free parking'),
       ('Lift'),
       ('Kitchen'),
       ('Smoke detector');

-- bed type table --
create table bed_type (
    id                  serial,
    name                ShortString,
    primary key         (id)
);

insert into bed_type(name)
values
       ('single'),
       ('double'),
       ('queen'),
       ('king'),
       ('sofa bed'),
       ('floor mattresses');


create table house_type (
    id                  serial,
    name                shortstring,
    primary key         (id)
);

insert into house_type (name)
values ('house'),
       ('apartment'),
       ('townhouse');



-- Item information table --
create table Item (
    id                  serial unique ,
    hoster_id           integer references User_information(id) not null,
    name                MediumString not null,
    description         TextString,
    create_date         date,

--     longitude           decimal(9,6),
--     latitude            decimal(9,6),
    country             ShortString not null,
    city                longstring not null,
    suburb              longstring not null,
    address             MediumString not null,
    post_code           int,
    type                int not null,

    price               decimal not null,

    --rating--
    accuracy            int,
    communication       int,
    cleanliness         int,
    location            int,
    check_in            int,
    value               int,
    rating_number       int,

    room_arrangement    int[][],
    common_spaces       int[],

    bath_number         int,
    max_people          int,

    amenities           int[],

    unavailable_data    date[],

    primary key         (id)
);

insert into Item(hoster_id, name, description, create_date, country, city, suburb, address, post_code, type, price,
                 accuracy, communication, cleanliness, location, check_in, value, rating_number,
                 room_arrangement, common_spaces, bath_number, max_people, amenities)
values ('2', 'Mansion Block Chic', 'This place is awesome! A 2 bedroom London style Mansion Block (or NYC style) apartment in the heart of Sydney, ' ||
                                   'located in a quiet street moments from Oxford St, Hyde Park, CBD, Surry Hills & Kings Cross. Newly renovated & 100% beautiful.',
           '2018-09-04', 'Australia', 'Sydney', 'Darlinghurst', '4/23 Stanley St', '2035', '1', '109', '50', '50', '50', '50',
           '50', '50', '10', '{{1}}', '{}', '1', '2', '{1,2,3,4,5,6}');


update Item set name = 'heihei'
where id = 19;

-- alter table Item add column longitude decimal(9,6);
-- alter table Item drop column longitude;
-- alter table Item add column latitude decimal(9,6);
-- alter table Item add column price int;


create table Item_photo (
    id                  serial,
    item_id             integer references Item(id) not null,
    position            URLString,
    delete_url          urlstring,
    primary key         (id)
);

insert into Item_photo(item_id, position)
values ('1', 'https://a0.muscache.com/im/pictures/19b8ea3c-3661-4207-a09a-e8346fbf07a9.jpg?aki_policy=x_large');

insert into Item_photo(item_id, position)
VALUES  ('1', 'https://a0.muscache.com/im/pictures/e51b10b1-bdc2-4427-bbbe-c4b0de15b456.jpg?aki_policy=x_large');

insert into Item_photo(item_id, position)
VALUES ('1', 'https://a0.muscache.com/im/pictures/8c5bb892-2190-4420-bed1-92d9f1919324.jpg?aki_policy=x_large');

insert into Item_photo(item_id, position)
VALUES ('1', 'https://a0.muscache.com/im/pictures/0f7f63e7-95bc-4255-8a10-519e8a19e214.jpg?aki_policy=x_large');

insert into Item_photo(item_id, position)
VALUES ('1', 'https://a0.muscache.com/im/pictures/729c7866-aa4b-47e6-afcd-d33c2911d291.jpg?aki_policy=x_large');

insert into Item_photo(item_id, position)
VALUES ('1', 'https://a0.muscache.com/im/pictures/8f3f771d-0271-46da-9880-bda6950f5134.jpg?aki_policy=x_large');

insert into Item_photo(item_id, position)
VALUES ('1', 'https://a0.muscache.com/im/pictures/8c609156-de44-48f0-8ebb-f70c6903e90a.jpg?aki_policy=x_large');

-- create table Price_information (
--
-- )
-- ALTER TABLE Transaction
--   RENAME COLUMN end_dare TO end_date;



create table Transaction (
    id                  serial,
    item_id             integer references Item(id) not null,
    user_id             integer references User_information(id) not null,
    host_id             integer references User_information(id) not null,
    status              Item_status,
    date                date,
    start_date          date,
    end_date            date,
    rating_or_not       boolean,
    comment             LongString,
    primary key         (id)
);
insert into Transaction (item_id, user_id, host_id, status, date, start_date, end_date, rating_or_not, comment)
values (60, 20, 32, 'S', '2008-01-01', '2018-01-01', '2018-03-03', 'T' , '');


create table Message (
    id                  serial,
    sender              integer not null,
    receiver            integer not null,
    content             LongString,
    date                timestamp not null,
    transaction_id      integer references Transaction(id),
    read_or_not         boolean,
    primary key         (id)
);

insert into message ( sender, receiver, content, "date", read_or_not)
values (1,2,'Good morning!','2018/09/24 10:05',false );
insert into message ( sender, receiver, content, "date", read_or_not)
values (2,1,'Good evening!','2018/09/24 20:05',false );
insert into message ( sender, receiver, content, "date", read_or_not)
values (1,2,'How are you going today?','2018/09/24 21:05',false );
insert into message ( sender, receiver, content, "date", read_or_not)
values (1,3,'Thank you!','2018/09/25 9:05',false );
insert into message ( sender, receiver, content, "date", read_or_not)
values (3,1,'You are welcome!','2018/09/25 10:05',false );


drop table if exists Item_comment;
create table Item_comment (
    id                  serial,
    user_id             integer references User_information(id) not null,
    item_id             integer references Item(id) not null,
    comment             TextString,
    accuracy            int,
    communication       int,
    cleanliness         int,
    location            int,
    check_in            int,
    value               int,
    date                date,
    primary key         (id)
);


create table Unavailable_date(
    id                  serial,
    item_id             integer references Item(id) not null ,
    date                date
);


insert into Unavailable_date(item_id, date)
values (1, '2018/10/08');
insert into Unavailable_date(item_id, date)
values (1, '2018/10/10');
insert into Unavailable_date(item_id, date)
values (1, '2018/10/13');

insert into unavailable_date(item_id,date ) values (1,'2018/10/01');
insert into unavailable_date(item_id,date ) values (1,'2018/10/05');
insert into unavailable_date(item_id,date ) values (1,'2018/12/01');

create table Post(
    id                  serial,
    user_id             integer references User_information(id) not null,
    country             longstring,
    city                longstring,
    suburb              longstring,
    start_date          date,
    end_date            date,
    price_start         float,
    price_end           float,
    people_number       int,
    comment             textstring,
    post_date           date,
    primary key         (id)
);




--  create table Review(
--      id                 serial,
--      item_id            integer references Item(id) not null,
--      user_id            integer references User_information(id) not null ,
--      comment            textstring,
--
--  )
