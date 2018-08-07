/* create user emailing with password 'emailing'; */
/* drop table emailing_users; drop table emailing_addresses; drop table emailing_domains; drop table emailing_users_addresses; drop table emailing_users_domains; */

create table emailing_users
(
	id 					numeric(10),
	name				varchar(200),
	passwd				varchar(200),
	constraint pk_emailing_users_id primary key (id),
	constraint ck_name UNIQUE (name),
	constraint auto_name_notnull check (name is NOT NULL),
	constraint auto_passwd_notnull check (passwd is NOT NULL)
);

create table emailing_addresses
(
	id 					numeric(10),
	address				varchar(200),
	constraint pk_emailing_addresses_id primary key (id),
	constraint ck_address UNIQUE (address),
	constraint auto_address_notnull check (address is NOT NULL)
);

create table emailing_domains
(
	id 					numeric(10),
	domain				varchar(200),
	constraint pk_emailing_domains_id primary key (id),
	constraint ck_domain UNIQUE (domain),
	constraint auto_domain_notnull check (domain is NOT NULL)
);

create table emailing_users_addresses
(
	id_user 		numeric(10),
	id_address		numeric(10),
	constraint pk_emailing_users_addresses primary key (id_user, id_address),
	constraint fk_id_user foreign key (id_user) references emailing_users (id),
	constraint fk_id_address foreign key (id_address) references emailing_addresses (id)
);

create table emailing_users_domains
(
	id_user 		numeric(10),
	id_domain		numeric(10),
	constraint pk_emailing_users_domains primary key (id_user, id_domain),
	constraint fk_id_user foreign key (id_user) references emailing_users (id),
	constraint fk_id_domain foreign key (id_domain) references emailing_domains (id)
);

/* demo user */

INSERT INTO emailing_users (id, name, passwd) VALUES (1, 'demo', 'fe01ce2a7fbac8fafaed7c982a04e229');
INSERT INTO emailing_addresses (id, address) VALUES (1, 'demo@test.com');
INSERT INTO emailing_domains (id, domain) VALUES (1, 'demo.com');
INSERT INTO emailing_users_addresses (id_user, id_address) VALUES (1, 1);
INSERT INTO emailing_users_domains (id_user, id_domain) VALUES (1, 1);