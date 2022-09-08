# create database if doesn't have one.
# db modeling for mysql can't operate without an existed database
# you may need to edit the config.py to use your local database
CREATE DATABASE IF NOT EXISTS `happylearning` DEFAULT CHARACTER SET UTF8MB4;


# Demo
USE happylearning;
# Users
# password hash stored in SHA256 with salted pbkdf2: sample accounts use 123 & 456 as password for lecturer and student respectively
INSERT INTO user(`id`, `username`, `email`, `password_hash`, `type`)
VALUES (1, "Michael", "777@outlook.com",
        "pbkdf2:sha256:260000$HfjeRMqkUsFMgfkm$e835eaa195d8c6170bd8cb629a4a6e1728040d678a26d2595c129ee2ce2d3142",
        'lecturer');
INSERT INTO user(`id`, `username`, `email`, `password_hash`, `type`)
VALUES (2, "zjq", "123@outlook.com",
        "pbkdf2:sha256:260000$bzyD040C4NlJQCkl$ab1b4cc3ed2cb65b24ea38a7760508fb42ed6e54c72c558277156e71eac3a318",
        'student');
INSERT INTO user(`id`, `username`, `email`, `password_hash`, `type`)
VALUES (3, "Hansen", "888@outlook.com",
        "pbkdf2:sha256:260000$Pzcml73HMhU0stRp$37b2976f81d032f90b62c3ead8b574d4d0f032978a7ee6d820cd8c5af13d466d",
        'lecturer');
INSERT INTO user(`id`, `username`, `email`, `password_hash`, `type`)
VALUES (4, "www", "321@outlook.com",
        "pbkdf2:sha256:260000$bzyD040C4NlJQCkl$ab1b4cc3ed2cb65b24ea38a7760508fb42ed6e54c72c558277156e71eac3a318",
        'student');

# Quizzes
INSERT INTO quiz(`id`, `name`, `user_id`)
VALUES (1, 'this is first quiz', 1);
INSERT INTO quiz(`id`, `name`, `user_id`)
VALUES (2, 'second quiz lah', 1);
INSERT INTO quiz(`id`, `name`, `user_id`)
VALUES (3, 'maybe the third?', 3);

# Questions
INSERT INTO question(`id`, `quiz_id`, `question`, `type`, `choice_a`, `choice_b`, `choice_c`, `choice_d`, `answer`)
VALUES (1, 1, 'Quiz 1 Q1?', 'MCQ', 'Quiz 1 A', 'Quiz 1 B', 'Quiz 1 C', 'Quiz 1 D', 'B');
INSERT INTO question(`id`, `quiz_id`, `question`, `type`, `choice_a`, `choice_b`, `choice_c`, `choice_d`, `answer`)
VALUES (2, 2, 'Quiz 2 Q1?', 'MCQ', 'Quiz 2 A', 'Quiz 2 B', 'Quiz 2 C', 'Quiz 2 D', 'B');
INSERT INTO question(`id`, `quiz_id`, `question`, `type`, `choice_a`, `choice_b`, `choice_c`, `choice_d`, `answer`)
VALUES (3, 3, 'Quiz 3 Q1?', 'TF', 'Quiz 3 A', 'Quiz 3 B', null, null, 'B');
INSERT INTO question(`id`, `quiz_id`, `question`, `type`, `choice_a`, `choice_b`, `choice_c`, `choice_d`, `answer`)
VALUES (4, 1, '???', 'MCQ', 'fsdfsddsf', 'fsdfdsfsdfsd', 'fdsfsdfsf', 'fsdfsdfsf', 'B');
INSERT INTO question(`id`, `quiz_id`, `question`, `type`, `choice_a`, `choice_b`, `choice_c`, `choice_d`, `answer`)
VALUES (5, 1, 'ok?', 'MCQ', 'fdsfsfsd', 'sdfdsfs', 'fsddsff', 'fsdf', 'B');
INSERT INTO question(`id`, `quiz_id`, `question`, `type`, `choice_a`, `choice_b`, `choice_c`, `choice_d`, `answer`)
VALUES (6, 1, 'no...', 'MCQ', 'gfsdgdfg', 'fdsafsaf', 'bfdg', 'gdfgvbd', 'B');
INSERT INTO question(`id`, `quiz_id`, `question`, `type`, `choice_a`, `choice_b`, `choice_c`, `choice_d`, `answer`)
VALUES (7, 1, 'TF??', 'TF', 'fdasfasas', 'asbfdsvb', null, null, 'B');
INSERT INTO score(`id`, `quiz_id`, `score`, `student_id`)
VALUES (1, 1, 0, 2);
INSERT INTO score(`id`, `quiz_id`, `score`, `student_id`)
VALUES (2, 1, 0, 4);