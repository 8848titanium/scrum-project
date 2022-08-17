CREATE DATABASE IF NOT EXISTS `happylearning` DEFAULT CHARACTER SET UTF8MB4;

# Demo entries
# password hash in SHA256: two sample account use 123 & 456 respectively
INSERT INTO user(`id`, `name`, `email`, `password_hash`, `type`) VALUES (1, "Michael", "777@outlook.com", "B3A8E0E1F9AB1BFE3A36F231F676F78BB30A519D2B21E6C530C0EEE8EBB4A5D0", 'lecturer');
INSERT INTO lecturer(`lecturer_id`) VALUES (1);

INSERT INTO user(`id`, `name`, `email`, `password_hash`, `type`) VALUES (2, "zjq", "123@outlook.com", "A665A45920422F9D417E4867EFDC4FB8A04A1F3FFF1FA07E998E86F7F7A27AE3", 'student');
INSERT INTO student(`student_id`) VALUES (2);


INSERT INTO quiz(`id`, `user_id`, `pin`)
VALUES (1, 1, 123456);
INSERT INTO quiz(`id`, `user_id`, `pin`)
VALUES (2, 1, 654321);
