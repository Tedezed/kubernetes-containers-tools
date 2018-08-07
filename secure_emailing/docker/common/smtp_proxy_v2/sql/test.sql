# TEST

# PASS demo == 'fe01ce2a7fbac8fafaed7c982a04e229'
INSERT INTO emailing_users (id, name, passwd) VALUES (1, 'demo', 'fe01ce2a7fbac8fafaed7c982a04e229');
INSERT INTO emailing_addresses (id, address) VALUES (1, 'demo1@test.com');
INSERT INTO emailing_addresses (id, address) VALUES (2, 'demo2@test.com');
INSERT INTO emailing_domains (id, domain) VALUES (1, 'demo1.com');
INSERT INTO emailing_domains (id, domain) VALUES (2, 'demo2.com');
INSERT INTO emailing_users_addresses (id_user, id_address) VALUES (1, 1);
INSERT INTO emailing_users_addresses (id_user, id_address) VALUES (1, 2);
INSERT INTO emailing_users_domains (id_user, id_domain) VALUES (1, 1);
INSERT INTO emailing_users_domains (id_user, id_domain) VALUES (1, 2);
INSERT INTO emailing_users (id, name, passwd) VALUES (2, 'test', 'fe01ce2a7fbac8fafaed7c982a04e229');
INSERT INTO emailing_addresses (id, address) VALUES (3, 'test@pepe.com');
INSERT INTO emailing_domains (id, domain) VALUES (3, 'example.com');
INSERT INTO emailing_users_addresses (id_user, id_address) VALUES (2, 3);
INSERT INTO emailing_users_domains (id_user, id_domain) VALUES (2, 3);

# NEXT ID
SELECT max(id)+1 as next_id FROM emailing_users;
SELECT max(id)+1 as next_id FROM emailing_addresses;
SELECT max(id)+1 as next_id FROM emailing_domains;

# BASE QUERY
SELECT passwd 
FROM emailing_users
WHERE name='demo';

SELECT domain
FROM emailing_domains
WHERE id IN (SELECT id_domain
		 FROM emailing_users_domains
		 WHERE id_user = (SELECT id
						  FROM emailing_users
						  WHERE name='demo'));
SELECT address
FROM emailing_addresses
WHERE id IN (SELECT id_address
		 FROM emailing_users_addresses
		 WHERE id_user = (SELECT id
						  FROM emailing_users
						  WHERE name='demo'));