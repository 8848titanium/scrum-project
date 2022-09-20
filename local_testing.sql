# create database if doesn't have one.
# db modeling for mysql can't operate without an existed database
# you may need to edit the config.py to use your local database
CREATE DATABASE IF NOT EXISTS `happylearning` DEFAULT CHARACTER SET UTF8MB4;


# Demo
USE happylearning;
# Users
# password hash stored in SHA256 with salted pbkdf2: sample accounts use 123 & 456 as password for lecturer and student respectively
INSERT INTO user(`id`, `username`, `email`, `password_hash`, `type`)
VALUES (1, "Michael", "michael@mail.com",
        "pbkdf2:sha256:260000$sgDUxgpSQkBC9ozl$f733f607c4174b238b45d3471694ba846da4c10fd3e8252265f5700a0be4f2f0",
        'lecturer');
INSERT INTO user(`id`, `username`, `email`, `password_hash`, `type`)
VALUES (2, "Jw", "jw@mail.com",
        "pbkdf2:sha256:260000$zNix0OSbqdRD2rz6$eba4d658e7c626d684a632a6696f82adf44196e411c490a085f7db1541a98201",
        'student');

# Quizzes
INSERT INTO quiz(`id`, `name`, `user_id`)
VALUES (1, 'this is first quiz', 1);
INSERT INTO quiz(`id`, `name`, `user_id`)
VALUES (2, 'second quiz lah', 1);

# Questions
INSERT INTO question(`id`, `quiz_id`, `question`, `choice_a`, `choice_b`, `choice_c`, `choice_d`, `answer`)
VALUES (1, 1, 'What is Scrum?', 'Huh?', 'A secret of Singaporean food', 'A project development Methodology',
        'Typo right? Scum is someone being 💩', 'C');
INSERT INTO question(`id`, `quiz_id`, `question`, `choice_a`, `choice_b`, `choice_c`, `choice_d`, `answer`)
VALUES (2, 2, 'What does Scrum Master do?', 'An expert of making the secret food',
        'Facilitate Scrum to a team by ensuring Scrum Framework is followed', 'Rush development team to code',
        'None of Others', 'B');
INSERT INTO question(`id`, `quiz_id`, `question`, `choice_a`, `choice_b`, `choice_c`, `choice_d`, `answer`)
VALUES (3, 1, 'What is Scrum Cycle?', 'A secret formula of Singaporean donut',
        'A fun facility that children play to spin', 'A period of time when a team delivers a set amount of woks',
        'None of Others', 'D');
INSERT INTO question(`id`, `quiz_id`, `question`, `choice_a`, `choice_b`, `choice_c`, `choice_d`, `answer`)
VALUES (4, 1, 'Do you think our site is awesome?', 'Hell yes, looks awesome on my 144P palm PDA',
        'Nah, looks lame on my ProMotion screen', 'Whaat?', 'Duh....', 'A');
INSERT INTO score(`id`, `quiz_id`, `score`, `rank_score`, `student_id`)
VALUES (1, 1, 4, 3921, 2);