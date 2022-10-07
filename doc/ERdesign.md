# Database conceptual design

## ER diagram

![ER_diagram](images/er.png)

## Entities

There are a total of five entities for our database design. Each is explained in detail as follows.

### 1. User Info

This is an entity regarding user login information, with three attributes.

1. NetId: a unique identifier to distinguish between users. This should be a string attribute and primary key for this table. NetId will serve as the username for login page.
2. Password: a string attribute, password for login the platform.
3. UserType: an enumerate attribute with values `Student` or `Professor`. This is to identify whether the user is a student or professor.

This entity is designed according to the assumptions:
1. Every user in this platform will have a unique NetId and cannot be modified, regradless of their identity (student or professor).
2. Users can change their password, which is the only allowed update operation for this entity table. We do not support new users to register. 
3. Once the user entered the NetId and password, the system will automatically identify the type of the user (student or professor), and lead the user to the corresponding menu. We suppose that one person can only be either a student or a professor.

### 2. Students

This is an entity for information of students. There are four attributes:

1. NetId: a string attribute to uniquely identify a student as the primary key.
2. Name: a string attribute to identify student's name.
3. Department: a string attribute to identify their department.
4. Level: an enumarate attribute with values `Grad` and `Undergrad`, to identify the degree level of their program.

Here we make the following assumptions:
1. A student is either a graduate or an undergraduate student. This field is to check their eligibility for registering.
2. Here we do not set the foreign key constraints for attribute `NetId` referencing `UserInfo`. One reason is that we need a stronger constraint to also check whether the `UserType` is `Student`. We will use assertion for the constraint. Another reason is that since we do not allow user to register, the cardinality of the table is constant. Once all the information is imported, we will no longer allow any update in this table. 

### 3. Professors

The entity is similar to the `Student`, with similar attributes and assumptions. We have the following attributes for the entity:
1. NetId: a string attribute to uniquely identify a professor as the primary key.
2. Name: a string attribute to identify professor's name.
3. Department: a string attribute to identify their department.

Since we have the similar assumptions. We will treat `NetId` here the same way as in `Students`.

### 4. Courses

The entity is for course information and have the following attributes:

1. CourseId: a string attribute to uniquely identify a course (as primary key). The string here follows the format `<department> + <number>`, such as `CS411`. 
2. Department: a string attribute to identify the department for the course. 
3. Title: a string attribute for the name of the course. 
4. Description: a long string attribute for the description of the course.

Here we assume that a course can only be owned by one department. In real situations, a course may have different course id in different department (e.g. `CS450` is also `ECE491`). We regard these two as **different** courses, since they aim at different students and may have different requirements, although they may be instructed by the same instructor, and give lectures together.

### 5. Sections

Section is the class that are arranged for a specific course. A section of the course will have its own instructors, lecture time and location and capacity. It has the following attributes:

1. CRN (Course reference number): a integer value to uniquely identify a course section (as primary key).
2. LectureType: a string value to identify how the lectures are given. (e.g. `In-person Lecture`, `Lecture&Discussion`, `Online lecture`, etc.)
3. AvaliableCredits: a string value to identify the avaliable credits for the section. This is for students to select how many credits they want for their enrollments. We use a formatted string to represent a set of intergers, split with "`,`" (e.g. `3,4` means 3 or 4 credits avaliable).
4. Restrictions: a string value to identify the restrictions for registering this section. This is mainly for sections only for undergrads or only for graduates. (e.g. `None` means no restrictions, `U` means undergrads not allowed to register, `G` means graduates not allowed to register, `UG` means both undergrad or graduates are not allowed to register, thought not likely to appear)
5. LectureTime: a string value to identify the lecture time for the section. The string follows the format of `<DAY><TIME_START><TIME_END>` and separated by "`,`" (e.g. `MON15301645,WED15301645` means lectures will be given on Monday and Wedesday at 3:30 to 4:45pm).
6. Capacity: a integer to show the max capacity for this section. This will be served as a eligibility check for enrollments.
7. Location: a string attribute to identify the location of the lecture.

One section belongs to a course. However, `Sections` here is not a weak entity because `CRN` itself is enough to uniquely identify a section. We will use relation `Consist` (shown below) to show the relation between courses and sections.

There are a few other assumptions:
1. Lectures will have a fixed schedule every week. We believe the UIUC course system follows this as well.
2. There will be no restrictions regarding section attributes other than the capacity and level restrictions. We do not have restrictions that are not mentioned in the attributes, such as prerequisits. 

## Relations

There are a total of 4 relations in our database design, which will addressed in details as follows:

### 1. Enrollment (Students and Sections)

`Enrollment` is a relation between `Students` and `Sections` to mark the course enrollments of each students. This relation will also have attributes regarding the academic performances, such as grades, credits and so on. The relation has the following attributes:
1. Semester: a string attribute to identify the semester when students enrolled in the course, following the format of `<season>+<year>` (e.g. `fall22` or `spring21`).
2. Grade: a string attribute to identify the grade students received for their courses. Usually this attributes is assigned either a letter grade (e.g. `A`, `B+`) or `None` (the instructors have not assigned a grade yet). 
3. Credit: an integer to identify the credit students choose for their courses. This should be an integer that is listed in `AvaliableCredit` in the related section.

This relation will be a **many-to-many** relation, since a student can enroll in multiple sections, and a section can hold multiple students. However, we do have restrictions based on the following assumptions:
1. One student can only enroll in the same course (and of course the same section) once. This is to ensure that `NetId` and `CRN` combined can uniquely identify an enrollment record.
2. Credit must be a positive integer. No half credit supported.
3. Grades is preferred as letter grades, and only getting `D` or above will students earn their credits. However, we may use this attribute to hold some unexpected situations for their grades (e.g. Grade postponed). But these will not count when calculating GPA and students will not earn the credits for this section.

### 2. Consist (Courses and Sections)

This is a relation to represent different class arrangement (known as sections) of courses. This is a **many-to-one** relation
for a section can only belong to one course, while a course can have multiple sections.

The `Consist` relation has no attributes. And since this is a many-to-one relation, we will not create a separate table for it. We will simply add `CourseId`, the primary key of `Courses`, to `Sections` and add foreign key constraints.

### 3. Instruct (Sections and Professors)

This is a relation to identify the instructors of different sections. This is a **many-to-many** relation based on the following assumptions:
1. The `Instruct` relation has nothing to do with `Courses`. When talking about instructors, we focus on `Sections`. In the course management page, professors can manage each section separately, even if they belong to the same course.
2. One section can have multiple instructors. And one professor can instruct multiple sections.
3. We only maintain information for current instructors of each section. That indicates for each `(NetId, CRN)` pair in `Instruct`, the professor will be shown in the information page for the section as a current instructor.

### 4. Ratings (Students and Professors)

Students can rate their professors, and the information will be stored as `Ratings` relation. This is a **many-to-many** relation. It has following attributes:
1. Rate: a real number for the rating. It scales from 0 to 5.
2. Comment: a long string attribute for detailed comments.

It based on the following assumptions:
1. Students can rate any number of professors and each professor can be rated by any number of students. However, one student can only leave one valid rating for one professor. This is to ensure that Student's `NetId` and Professor's `NetId` can uniquely identify one rating record.
2. We will not set restrictions of leaving comments or rating any professors. However, we may show a message on the page when a student did not take any courses instructed by this professor they rated.

## Relational Schema
The database design will be converted into 8 tables.

**1. UserInfo**

```
UserInfo(
    NetId VARCHAR(255) [PK],
    Password VARCHAR(255),
    UserType ENUM('Student', 'Professor')
)
```

**2. Students**
```
Students(
    NetId VARCHAR(255) [PK],
    Name VARCHAR(255),
    Department VARCHAR(255),
    Level ENUM('Grad', 'Undergrad')
)
```

**3. Professors**
```
Professors(
    NetId VARCHAR(255) [PK],
    Name VARCHAR(255),
    Department VARCHAR(255)
)
```

**4. Courses** 
```
Courses(
    CourseId VARCHAR(255) [PK],
    Department VARCHAR(255),
    Title VARCHAR(255),
    Description VARCHAR(5000)
)
```

**5. Sections**
```
Sections(
    CRN int [PK],
    LectureType VARCHAR(255),
    AvaliableCredits VARCHAR(255),
    Restrictions VARCHAR(255),
    LectureTime VARCHAR(255),
    Capacity int,
    Location VARCHAR(255),
    CourseId VARCHAR(255) [FK to Courses.CourseId]
)
```

**6. Instruct**
```
Instruct(
    Professor VARCHAR(255) [PK] [FK to Professors.NetId],
    CRN int [PK] [FK to Sections.CRN]
)
```

**7. Ratings**
```
Ratings(
    Student VARCHAR(255) [PK] [FK to Students.NetId],
    Professor VARCHAR(255) [PK] [FK to Professors.NetId],
    Rate REAL,
    Comment VARCHAR(5000)
)
```

**8. Enrollments**
```
Enrollments(
    CRN int [PK] [FK to Sections.CRN],
    NetId VARCHAR(255) [PK] [FK to Students.NetId],
    Semester VARCHAR(255),
    Credit int,
    Grade VARCHAR(255)
)
```

## MySQL DDL commands

```mysql
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
    Rate Decimal,
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







```