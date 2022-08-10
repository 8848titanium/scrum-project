# heroku database
USE egb6uc2xprot3fmz;

# lecturer table
CREATE TABLE IF NOT EXISTS `egb6uc2xprot3fmz`.`lecturer`
(
    `lecturer_id`       INT auto_increment NOT NULL,
    `lecturer_name`     VARCHAR(255)       NOT NULL,
    `lecturer_password` VARCHAR(255)       NOT NULL,
    `lecturer_email`    VARCHAR(255)       NOT NULL UNIQUE,
    PRIMARY KEY (`lecturer_id`)
);

# quiz table
CREATE TABLE IF NOT EXISTS `egb6uc2xprot3fmz`.`quiz`
(
    `quiz_id`     INT Primary key NOT NULL,
    `lecturer_id` INT             NOT NULL,
    `quiz_PIN`    VARCHAR(45)     NOT NULL UNIQUE,
    CONSTRAINT `lecturer_quiz`
        FOREIGN KEY (`lecturer_id`)
            REFERENCES `egb6uc2xprot3fmz`.`lecturer` (`lecturer_id`)
);

# question table
CREATE TABLE IF NOT EXISTS `egb6uc2xprot3fmz`.`question`
(
    `question_id` INT Primary key NOT NULL,
    `quiz_id`     INT             NOT NULL,
    `question`    VARCHAR(255)    NOT NULL,
    `type`        INT             NOT NULL,
    `answer`      VARCHAR(255)    NOT NULL,
    CONSTRAINT `quiz_question`
        FOREIGN KEY (`quiz_id`)
            REFERENCES `egb6uc2xprot3fmz`.`quiz` (`quiz_id`)
);

# student table
CREATE TABLE IF NOT EXISTS `egb6uc2xprot3fmz`.`student`
(
    `student_id`       INT auto_increment NOT NULL,
    `student_name`     VARCHAR(255)       NOT NULL,
    `student_password` VARCHAR(255)       NOT NULL,
    `student_email`    VARCHAR(255)       NOT NULL UNIQUE,
    PRIMARY KEY (`student_id`)
);

# score table
CREATE TABLE IF NOT EXISTS `egb6uc2xprot3fmz`.`score`
(
    `quiz_id`    INT NOT NULL,
    `student_id` INT NOT NULL,
    `score`      INT NOT NULL,
    PRIMARY KEY (`quiz_id`, `student_id`),
    CONSTRAINT `student_score`
        FOREIGN KEY (`student_id`)
            REFERENCES `egb6uc2xprot3fmz`.`student` (`student_id`),
    CONSTRAINT `quiz_score`
        FOREIGN KEY (`quiz_id`)
            REFERENCES `egb6uc2xprot3fmz`.`quiz` (`quiz_id`)
);

# testing entries
INSERT INTO student(`student_id`, `student_name`, `student_password`, `student_email`)
VALUES ("1", "zjq", "123", "123@outlook.com");
INSERT INTO lecturer(`lecturer_id`, `lecturer_name`, `lecturer_password`, `lecturer_email`)
VALUES ("1", "Michael", "456", "777@outlook.com");
