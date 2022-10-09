#Entities

CREATE TABLE UserInfo(
    NetId VARCHAR(255),
    Password VARCHAR(255),
    UserType ENUM('Student', 'Professor'),
    PRIMARY KEY(NetId)
);

CREATE TABLE Students(
    NetId VARCHAR(255),
    Name VARCHAR(255),
    Department VARCHAR(255),
    Level ENUM('Grad', 'Undergrad'),
    PRIMARY KEY(NetId)
);

CREATE TABLE Professors(
    NetId VARCHAR(255),
    Name VARCHAR(255),
    Department VARCHAR(255),
    PRIMARY KEY(NetId)
);

CREATE TABLE Courses(
    CourseId VARCHAR(255),
    Department VARCHAR(255),
    Title VARCHAR(255),
    Description VARCHAR(5000),
    PRIMARY KEY(CourseId)
);

CREATE TABLE Sections(
    CRN int,
    LectureType VARCHAR(255),
    AvaliableCredits VARCHAR(255),
    Restrictions VARCHAR(255),
    LectureTime VARCHAR(255),
    Capacity int,
    Location VARCHAR(255),
    CourseId VARCHAR(255),
    PRIMARY KEY(CRN),
    FOREIGN KEY(CourseId) REFERENCES Courses(CourseId) ON DELETE CASCADE
);

#Relationships

CREATE TABLE Instruct(
    Professor VARCHAR(255),
    CRN int,
    PRIMARY KEY(Professor, CRN),
    FOREIGN KEY(Professor) REFERENCES Professors(NetId) ON DELETE CASCADE,
    FOREIGN KEY(CRN) REFERENCES Sections(CRN) ON DELETE CASCADE
);

CREATE TABLE Ratings(
    Student VARCHAR(255),
    Professor VARCHAR(255),
    Rate Real,
    Comment VARCHAR(5000),
    PRIMARY KEY(Student, Professor),
    FOREIGN KEY(Student) REFERENCES Students(NetId) ON DELETE CASCADE,
    FOREIGN KEY(Professor) REFERENCES Professors(NetId) ON DELETE CASCADE
);

CREATE TABLE Enrollments(
    CRN int,
    NetId VARCHAR(255),
    Semester VARCHAR(255),
    Credit int,
    Grade VARCHAR(255),
    PRIMARY KEY(NetId, CRN),
    FOREIGN KEY(CRN) REFERENCES Sections(CRN) ON DELETE CASCADE,
    FOREIGN KEY(NetId) REFERENCES Students(NetId) ON DELETE CASCADE
);