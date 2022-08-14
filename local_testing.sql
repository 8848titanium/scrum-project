CREATE USER `a3`@`localhost`
    IDENTIFIED BY `123456`;

CREATE DATABASE IF NOT EXISTS `happylearning` DEFAULT CHARACTER SET UTF8MB4;

GRANT ALL PRIVILEGES ON happylearning.* TO `a3`@`localhost`;

USE happylearning;

# 建立lecturer表
CREATE TABLE IF NOT EXISTS `happylearning`.`lecturer`
(
    `lecturer_id`       INT auto_increment NOT NULL,
    `lecturer_name`     VARCHAR(255)       NOT NULL,
    `lecturer_password` VARCHAR(255)       NOT NULL,
    `lecturer_email`    VARCHAR(255)       NOT NULL UNIQUE,
    PRIMARY KEY (`lecturer_id`)
);

# 建立quiz表
CREATE TABLE IF NOT EXISTS `happylearning`.`quiz`
(
    `quiz_id`     INT Primary key NOT NULL,
    `lecturer_id` INT             NOT NULL,
    `quiz_PIN`    VARCHAR(45)     NOT NULL UNIQUE,
    CONSTRAINT `lecturer_quiz`
        FOREIGN KEY (`lecturer_id`)
            REFERENCES `happylearning`.`lecturer` (`lecturer_id`)
);

# 建立question表
CREATE TABLE IF NOT EXISTS `happylearning`.`question`
(
    `question_id` INT Primary key NOT NULL,
    `quiz_id`     INT             NOT NULL,
    `question`    VARCHAR(255)    NOT NULL,
    `type`        INT             NOT NULL,
    `A`           VARCHAR(255),
    `B`           VARCHAR(255),
    `C`           VARCHAR(255),
    `D`           VARCHAR(255),
    `answer`      VARCHAR(255)    NOT NULL,
    CONSTRAINT `quiz_question`
        FOREIGN KEY (`quiz_id`)
            REFERENCES `happylearning`.`quiz` (`quiz_id`)
);

# 建立student表
CREATE TABLE IF NOT EXISTS `happylearning`.`student`
(
    `student_id`       INT auto_increment NOT NULL,
    `student_name`     VARCHAR(255)       NOT NULL,
    `student_password` VARCHAR(255)       NOT NULL,
    `student_email`    VARCHAR(255)       NOT NULL UNIQUE,
    PRIMARY KEY (`student_id`)
);

# 建立score表
CREATE TABLE IF NOT EXISTS `happylearning`.`score`
(
    `quiz_id`    INT NOT NULL,
    `student_id` INT NOT NULL,
    `score`      INT NOT NULL,
    PRIMARY KEY (`quiz_id`, `student_id`),
    CONSTRAINT `student_score`
        FOREIGN KEY (`student_id`)
            REFERENCES `happylearning`.`student` (`student_id`),
    CONSTRAINT `quiz_score`
        FOREIGN KEY (`quiz_id`)
            REFERENCES `happylearning`.`quiz` (`quiz_id`)
);

# 查看已建立的表
SHOW TABLES;

# 插入测试数据
INSERT INTO student(`student_id`, `student_name`, `student_password`, `student_email`)
VALUES ("1", "zjq", "123", "123@outlook.com");
INSERT INTO lecturer(`lecturer_id`, `lecturer_name`, `lecturer_password`, `lecturer_email`)
VALUES ("1", "Michael", "456", "777@outlook.com");

INSERT INTO quiz(`quiz_id`, `lecturer_id`, `quiz_PIN`)
VALUES (1, 1, 12345678);
INSERT INTO quiz(`quiz_id`, `lecturer_id`, `quiz_PIN`)
VALUES (2, 1, 87654321);
INSERT INTO question(`question_id`, `quiz_id`, `question`, `type`, `A`, `B`, `C`, `D`, `answer`)
VALUES (1, 1, "MonoMCQ?", 0, "dasdas", "dsadas", "dasdsa", "dasda", "B");
INSERT INTO question(`question_id`, `quiz_id`, `question`, `type`, `A`, `B`, `C`, `D`, `answer`)
VALUES (2, 2, "MCQ?", 1, "vfdvdf", "vcxvzcx", "sdafsa", "fdasfsa", "AC");
INSERT INTO question(`question_id`, `quiz_id`, `question`, `type`, `A`, `B`, `C`, `D`, `answer`)
VALUES (3, 1, "fill?", 2, NULL, NULL, NULL, NULL, "Filled");
