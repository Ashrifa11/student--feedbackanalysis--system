CREATE DATABASE IF NOT EXISTS student_feedback;
USE student_feedback;

CREATE TABLE IF NOT EXISTS courses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    course_name VARCHAR(150) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS feedback (
    id INT AUTO_INCREMENT PRIMARY KEY,
    course_id INT NOT NULL,
    rating TINYINT NOT NULL,
    comment VARCHAR(1000) NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_feedback_course FOREIGN KEY (course_id) REFERENCES courses(id),
    CONSTRAINT chk_rating CHECK (rating BETWEEN 1 AND 5)
);

INSERT IGNORE INTO courses (course_name) VALUES
('Python Programming'), ('Database Management Systems'), ('Data Structures');
