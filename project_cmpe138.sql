drop database if exists fitnessstudio;
create database fitnessstudio;
use fitnessstudio;

CREATE table client (
  client_id        varchar(25) not null,
  client_email     varchar(50) not null,
  client_pwd       varchar(65) not null,
  client_name      varchar(50) not null, 
  client_mobile	   integer not null,
  client_bmi       float(25) not null,
  client_weight	   integer not null,
  client_height    integer not null,
  client_age       integer not null,
  client_gender    varchar(25) not null,
  client_admin_id  varchar(25) not null,
  client_feedback  varchar(300),
  
  primary key (client_id),
  unique (client_email,client_mobile)
  -- can be instructor relation ka foreign key addeed on inst side
  -- foreign key added for signsup relation
  
);

CREATE TABLE admin 
(
  admin_name   varchar(25) not null,
  admin_email  varchar(25) not null,
  admin_id     varchar(6) not null, 
  admin_salary integer not null,
  admin_pwd    varchar(65) not null,
  admin_client_id  varchar(25),
  primary key (admin_id),
  unique (admin_email),
  -- Foreign key is added for Can_be_adm relation
  foreign key (admin_client_id) references client(client_id) on delete set null on update cascade
);

CREATE TABLE Fitness_seminar 
(
  FS_zoomlink varchar(225) not null,
  FS_sem_id   varchar(6) not null,
  FS_type     varchar(8), 
  FS_admin_id varchar(25),
  FS_Inst_ID  varchar(6),
  FS_Name     varchar(24) not null,
  primary key (FS_sem_id),
  unique ( FS_zoomlink),
  -- adding foreign key for schedules
  foreign key (FS_admin_id) references admin(admin_id)  on delete cascade on update cascade
  -- adding foreign key for conducts relationship
);

CREATE TABLE Instructor (
    ID varchar(6),
    Name varchar(30),
    Salary dec(10,2),
    Email varchar(25),
    Password varchar(65), 
    oneflag boolean,
    groupflag boolean,
    semflag boolean,
    Trainer_id varchar(6),
    Rating int default 0,
    primary key (ID),
    foreign key (Trainer_id) references Instructor(ID) on delete set null
    -- FK instructor to instructor recursive relationship
);

CREATE TABLE Personalized_workout_plan (
    Client_ID varchar(6),
    Preparer_ID varchar(6),
    Plan_num int,
    primary key (Client_ID, Plan_num),
    foreign key (Preparer_ID) references Instructor(ID) on delete set null,
    -- FK to instructor ID as preparer.
    foreign key (Client_ID) references client(client_id) on delete cascade on update cascade
    -- FK to client as user.
);

CREATE TABLE Workouts (
    Client_ID varchar(6),
    Preparer_ID varchar(6),
    Plan_num int,
    Workout varchar(50), 
    -- reference to a particular program
    primary key (Client_ID, Plan_num, Workout),
    foreign key (Preparer_ID) references Instructor(ID) on delete set null,
    -- FK to instructor ID as typical for multi-valued attr.
    foreign key (Client_ID, Plan_num) references Personalized_workout_plan (Client_ID, Plan_num) on delete cascade on update cascade
    -- FK to client as user.
    -- FK to plan_num as typical for multi-valued attr.

);


CREATE TABLE membership
 (
  mem_client_id    varchar(25),
  mem_level        varchar(25) not null,
  mem_cost         integer not null,
  mem_admin_id     varchar(25),
 
  primary key (mem_client_id, mem_level),
  -- adding the foreign key for has relation(identifying relationship)
  foreign key (mem_client_id) references client(client_id) on delete cascade on update cascade,
  -- adding foreign key for coordinates relation
  foreign key (mem_admin_id) references admin(admin_id) on delete cascade on update cascade
);

create table advisor
(
name varchar(20), 
ID varchar(6) not null,
email varchar(30),
password varchar(65), -- password needs to be hashed/encrypted
salary numeric(8,2), -- precision 8, scale 2 can represent 123456.78
jobType varchar(12),
primary key (ID),
unique(email)
);

create table advises(
clientID varchar(6),
advID varchar(6),
rating int default 0,
primary key(clientID, advID),
foreign key(clientID) references client(client_id)
on delete cascade
on update cascade,
foreign key(advID) references advisor(ID)
on delete cascade
on update cascade
);

create table dietary_plan
(
diet_plan_ID varchar(5),
dietitianID varchar(6),
clientID varchar(6),
primary key(diet_plan_ID),
foreign key(dietitianID) references advisor(ID)
on delete cascade
on update cascade,
foreign key(clientID) references client(client_id)
on delete cascade
on update cascade
);

create table plan_macronutrients
(
diet_plan_ID_macro varchar(5),
protein numeric(3,0) default 0,  -- e.g. 100 g per day 
carbs numeric(3,0) default 0,
fat numeric(3,0) default 0,
primary key(diet_plan_ID_macro, protein, carbs, fat),
foreign key(diet_plan_ID_macro) references dietary_plan(diet_plan_ID)
on delete cascade
on update cascade
);

create table plan_supplements(
diet_plan_ID_suppl varchar(5),
vitaminD3 numeric(2,0), -- e.g. in mcg 25
vitaminC numeric(4,0), -- roughly 100 mg per day
magnesium numeric(4,0), -- 1000 mg per day
omega3 numeric(4,0), -- 2000 mg
primary key (diet_plan_ID_suppl, vitaminD3, vitaminC, magnesium, omega3),
foreign key (diet_plan_ID_suppl) references dietary_plan(diet_plan_ID)
on delete cascade
on update cascade
);

create table Lab_test( 
test_id  varchar(6) not null,
Test_name  varchar(8),
d_ID   varchar(6) not null,
clientID varchar(6),
primary key (test_id),
foreign key (d_ID) references advisor(ID)
on delete cascade
on update cascade,
foreign key(clientID) references client(client_id)
on delete cascade
on update cascade
);
 
create table mental_coaching_plan(
M_C_plan_id  varchar(6) not null,
M_C_ID    varchar(6) not null,
clientID varchar(6),
primary key (M_C_plan_id),
foreign key (M_C_ID) references advisor(ID)
on delete cascade
on update cascade,
foreign key(clientID) references client(client_id)
on delete cascade
on update cascade
);



create table training_session 
(
session_type	varchar(20),
session_individual_group	varchar(20),
session_zoom_link	varchar(100) not null,
session_id	varchar(6) not null, 
session_admin_id	varchar(6),
session_instructor_id	varchar (6), 
primary key	(session_id),
unique	(session_zoom_link),
foreign key	(session_admin_id) references admin(admin_id) on delete cascade on update cascade,
foreign key	(session_instructor_id) references Instructor(ID) on delete cascade on update cascade
);

create table training_session_client 
(
session_id	varchar(6) not null,
client_id	varchar(6) not null,
primary key(session_id, client_id),
foreign key(session_id) references training_session(session_id) on delete cascade on update cascade,
foreign key(client_id) references client(client_id) on delete cascade on update cascade
);

INSERT into client VALUES
('123456','name1.last@gmail.com','a81dbbb32d5403b960215d29c2ed27f7f3338c327ce98ec88fe22348f2d9b003','Name1Last',1234567890,33.6,180,180,25,'MALE','A23675', 'Leave a comment'), -- password1
('123457','name2.last@gmail.com','2435d53486947696b68493fff95f2a48a3f36fa7c5c03496c71e7000ef62f953','Name2Last',1234567891,26.6,170,170,23,'MALE','A23655', 'Leave a comment'), -- password2
('123458','name3.last@gmail.com','1fc8ee2f3002e0b4c28f1935dbef9b0e8683b3717294ea5f448a53278b60cc42','Name3Last',1234567892,25.1,130,165,21,'FEMALE','A23735', 'Leave a comment'),-- password3
('123459','name4.last@gmail.com','1b26e0d4ad352a127cb5b7c8e17d457b38da0f3d7289602ab6270c6c24abf9fa','Name4Last',1234567893,20.6,170,150,22,'MALE','A23795', 'Leave a comment'),-- password4
('123460','name5.last@gmail.com','53d3737ccc46d651b356c0e39c70f884b9e72d3755f8392fbf8471dd189eaee8','Name5Last',1234567894,18.6,120,122,18,'FEMALE','A23775', 'Leave a comment'),-- password5
('123461','name6.last@gmail.com','751778c8e21fa4ae0a83aef584ae2a32e1bad66e7412bc6633c59dc3b55c5e6b','Name6Last',1234567895,13.6,120,122,21,'MALE','A23895', 'Leave a comment');-- password6

INSERT into admin VALUES
('kyra_Foerster','kyra.foerster@gmail.com','A23795',100000,'cbb417b7d2b7a5f3bef3c5ef98e662a13986bfc394684d5981b8512b814a84ac','123459'), -- kyra
('vikas_tadepu','vikas.tadepu@gmail.com','A23675',100000,'69f703d67c00e630af4c98c85afd850c7d48d63c8a5ba663131b12beb34b2564','123456'), -- vikas
('Alex_Zalzinayak','Alex.Zalzinayak@gmail.com','A23895',100000,'e002c0c966f83df42a0ff5ca17cbee41d7c5278800a5aea1dd8c07d4e02183c0','123461'), -- alex
('saroja_kandula','saroja.kandula@gmail.com','A23655',100000,'c36a7b3c781306cc83770356d837d692422676c5167312371b3e27541ffa12ea','123457'), -- saroja
('vineeth_kiragi','vineet.kiragi@gmail.com','A23735',100000,'829ab05dc65afe4e85c0aacac22e4206d725c09c1cd3ebc5fbdda00694ad3f95','123458'), -- vineeth
('Jasmine_Wang','jasmine.wang@gmail.com','A23775',100000,'278c52d0ec5b6f6be8e010f1e0a7635468e9189aea96b8c28b9279369b108f8b','123460'); -- jasmine

INSERT into Fitness_seminar VALUES
('https://us02web.zoom.us/j/87562909621?pwd=RE5YNDIvM0RWRTkzZFd0eGxSQWQrZz09','FS2356','live','A23675','A00001','Yoga Seminar'),
('https://us02web.zoom.us/j/87562909641?pwd=RE5YNDIvM0RWRTkzZFd0eGxSQWQrZz09','FS2378','recorded', 'A23795','A00002','Mental Health Seminar'),
('https://us02web.zoom.us/j/87562909631?pwd=RE5YNDIvM0RWRTkzZFd0eGxSQWQrZz09','FS2498','live', 'A23675','A00001','Diet Plan Seminar'),
('https://us02web.zoom.us/j/87562909651?pwd=RE5YNDIvM0RWRTkzZFd0eGxSQWQrZz09','FS3765','recorded', 'A23675','A00002','Fitness Seminar');

INSERT into Instructor VALUES 
('A00001','John Smith','28000','jsmith@555.net', 'e99b5787e29d2f8fbca7b4d4a9da8a4f7a50efe4133b9acc1b93ff887c9dc0ab', TRUE, TRUE, FALSE, NULL,0), -- jsmith 
('A00002','Iris Flower','23000','Isflwr@555.net', 'c6563d32eaeff464024a71f6d4db12f69158440af07bb25d1628d8c6705551d7', TRUE, FALSE, TRUE, 'A00001',0), -- iflower
('A00003','Ida Gomez','24000','Igomez@555.net', '8bec29ffeadd1aa59ea62be222387418999eddeb5ebe5b1a3d23a60fdf496f28',TRUE,FALSE,FALSE,NULL,0), -- igomez
('A00004','Tim Banner','18000','Tbanner@555.net', '901edfbcc092d4b6f5114f94f7a69ebca45e4001c6f628f9ecfa5a6add78e5f8', TRUE, FALSE, FALSE, 'A00002',0), -- tbanner
('A00005','Hyla Ranz','16000','Hranz@555.net', 'cbcdc1d30db076ecd7d9df91becabe1bceb682f372fd36b509dd1314cb90b3b8', FALSE, FALSE, TRUE, 'A00001',0), -- hranz
('A00006','Remy Madden','17000','Rmadden@555.net', 'd71b0b9ea8439850dad553b22547f050da6ebfb74ff20430c702dc04610c2e20', TRUE,FALSE,TRUE,'A00002',0), -- rmadden
('A00010','kyra Forster','28000','kyra.forester@gmail.com', 'f4eff4179495829be8793c1dd4e53f336b8a1337fedc619d27f93e0c0890341c', TRUE, TRUE, FALSE, NULL,0), -- kforster
('A00020','vikas tadepu','23000','vikas.tadepu@gmail.com', '1f726457d5f156325ad80247cbd7e7bfdf5a3e26b2ced235d0d33e4fc217849c', TRUE, FALSE, TRUE, 'A00001',0), -- vtadeupu
('A00030','Alex Zalzinayak','24000','Alex.Zalzinayak@gmail.com', '09953161148a9b09bc860b774a1a5b101f76b76274a94573717c6b14daaa7867', TRUE,FALSE,FALSE,NULL,0), -- azaliznyak
('A00040','saroja kandula','18000','saroja.kandula@gmail.com', 'a312e6736a53c42cfe92feea3701894b66d422c712e7004e84aead3394518a75',TRUE, FALSE, FALSE, 'A00002',0), -- skandula
('A00050','vineeth kiragi','16000','vineeth.kiragi@gmail.com', 'c42280cac1856c9ce7a5a954a213c09e719a63610a9eb6c1d85532f8f73603a5', FALSE, FALSE, TRUE, 'A00001',0), -- vkiradi
('A00060','Jasmine Wang','17000','Jasmine.Wang@gmail.com', 'cdfb4570b67ee7b9d100972c40cfe926ffaf058023040155fb41e3afadfc37b2', TRUE,FALSE,TRUE,'A00002',0); -- jwang


INSERT into membership VALUES
('123456','Basic',350,'A23675'),
('123457','Premium',350,'A23655'),
('123458','Free',0,'A23735'),
('123459','Free',0,'A23795'),
('123460','Basic',350,'A23775'),
('123461','Premium',350,'A23895');


insert into advisor values ('Maria',  '468799', 'maria.pepe@gmail.com','de5a12f26a2d68db3742d326ad7ecece27dd6b2ffaf04cb2f875d009d2025e92', 40000, 'Dietitian'); -- dietitian, mpepe
insert into advisor values ('Marco',  '555122', 'marco.polo@gmail.com','f14167a245d2053912b589ffd712e3156197402124d14327eb71c25b24171abf', 30000, 'Dietitian'); -- dietitian, mpolo
insert into advisor values ('Marike', '832594', 'marike.summer@hotmail.com','dd82c65136623e100348394d2b22f8edb051e97e34d19a52a3e4372304a318b7', 25000, 'Mental_Coach'); -- mental coach, msummer
insert into advisor values ('Martin', '236772', 'martin.spring@yahoo.com','fa2bf2712a1bc67b4b2ef4349f8f4d4dca4c833291664fcd047be46bc51b0792', 15000, 'Mental_Coach'); -- mental coach, mspring
insert into advisor values ('Bernado', '670046', 'bernado@garces.com','84b5350abc5f0183d0c5b8c914f5d657e0b0f7398063f5a5848103f0a5432aab', 15500, 'Doctor'); -- doctor, bgarces
insert into advisor values ('Carl',  '778543', 'carl.winter@gmail.com','e7c93507f8f434b470e24f43bc592f5e1034013a11f39f76d8606d7124c44ab2', 30500, 'Doctor'); -- doctor, cwinter

insert into advises values ('123457', '468799',0); -- dietitian
insert into advises values ('123457', '670046',0); -- doctor
insert into advises values ('123457', '832594',0); -- mental_coach
insert into advises values ('123461', '468799',0); -- dietitian
insert into advises values ('123461', '778543',0); -- doctor
insert into advises values ('123461', '832594',0); -- mental_coach




insert into Lab_test values('121','Mona',  '670046' ,'123457');
insert into Lab_test values('122','Diana', '778543','123461' );


insert into mental_coaching_plan values('1100', '832594', '123457');
insert into mental_coaching_plan values('1300', '832594', '123461');

insert into dietary_plan values ('11111','468799', '123457');
insert into dietary_plan values ('11112', '468799', '123461');

-- list the macros for diet plan xy
insert into plan_macronutrients values ('11111', 120, 250, 65);
insert into plan_macronutrients values ('11112', 150, 350, 50);

insert into plan_supplements values ('11111', 25, 100, 1500, 2000);
insert into plan_supplements values ('11112', 25, 250, 1500, 1500);


-- Personalized Workout Plans:
insert into Personalized_workout_plan values ('123456','A00001','1');
insert into Personalized_workout_plan values ('123457','A00001','2');
insert into Personalized_workout_plan values ('123458','A00001','3');
insert into Personalized_workout_plan values ('123459','A00002','1');
insert into Personalized_workout_plan values ('123460','A00002','2');
insert into Personalized_workout_plan values ('123461','A00003','1');


insert into Workouts values ('123456','A00001','1','Back and Legs 1');
insert into Workouts values ('123456','A00001','1','Chest 2');
insert into Workouts values ('123456','A00001','1','Arms 1');
insert into Workouts values ('123457','A00001','2','Back and Legs 1');
insert into Workouts values ('123457','A00001','2','Chest and Shoulders 1');
insert into Workouts values ('123457','A00001','2','Arms 2');
insert into Workouts values ('123458','A00001','3','Whole Body 1');
insert into Workouts values ('123458','A00001','3','Whole Body 2');
insert into Workouts values ('123458','A00002','1','Bodyweight 1');
insert into Workouts values ('123460','A00002','2','Bodyweight 2');
insert into Workouts values ('123461','A00003','1','Whole Body 1');
insert into Workouts values ('123461','A00003','1','Whole Body 2');


insert into training_session values ('recorded', 'group', 'http://www.zoom.com/110000', '110000', 'A23795', 'A00010');
insert into training_session values ('live', 'group', 'http://www.zoom.com/120000', '120000', 'A23655', 'A00020');
insert into training_session values ('recorded', 'individual', 'http://www.zoom.com/130000', '130000', 'A23735', 'A00030');
insert into training_session values ('recorded', 'group', 'http://www.zoom.com/140000', '140000', 'A23675', 'A00050');
insert into training_session values ('live', 'group', 'http://www.zoom.com/150000', '150000', 'A23775', 'A00050');
insert into training_session values ('live', 'individual', 'http://www.zoom.com/160000', '160000', 'A23895', 'A00060');

insert into training_session_client values ('110000', '123459');
insert into training_session_client values ('120000', '123457');
insert into training_session_client values ('130000', '123458');
insert into training_session_client values ('140000', '123456');
insert into training_session_client values ('150000', '123460');
insert into training_session_client values ('160000', '123461');


alter table client add foreign key (client_admin_id) references admin(admin_id) on delete cascade on update cascade;
alter table Instructor add foreign key (Trainer_id) references Instructor(ID) on delete set NULL;
alter table Fitness_seminar add foreign key (FS_Inst_ID) references Instructor(ID) on delete cascade on update cascade;
