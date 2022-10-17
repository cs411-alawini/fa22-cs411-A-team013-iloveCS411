# Stage 3 Instructions

> Ruipeng Ge 10/17/2022

## Database Schema

Below is the schema for i-course database regarding students and enrollments of courses:

> `Students`
> | Attribute | Type |
> | --------- | -------------|
> | NetId | VARCHAR(255) |
> | Name | VARCHAR(255) |
> | Department | VARCHAR(255) |
> | Level | ENUM('Grad', 'Undergrad') |

> `Courses`
> | Attribute | Type |
> | --------- | -------------|
> | CourseId | VARCHAR(255) |
> | Department | VARCHAR(255) |
> | Title |  VARCHAR(255) |
> | Description | VARCHAR(5000) |

> `Sections`
> | Attribute | Type |
> | --------- | -------------|
> | CRN | int |
> | LectureType | VARCHAR(255) |
> | AvaliableCredits | VARCHAR(255) |
> | Restrictions | VARCHAR(255)| 
> | LectureTime | VARCHAR(255)|
> | Capacity | int |
> | Location | VARCHAR(255) |
> | CourseId | VARCHAR(255) |

> `Enrollments`
> | Attribute | Type |
> | --------- | -------------|
> | CRN | int |
> | NetId | VARCHAR(255) |
> | Semester | VARCHAR(255) |
> | Credit | int |
> | Grade | VARCHAR(255) |

## Question 1

Write a MySQL query to find all students in `CS` who take at least one course offered by `ECE`, and all students in `ECE` who take at least one course offered by `CS`. Return their `NetId`, `Name`, `Department`, and `Level`.

## Question 2

Write a MySQL query to find all students who take 8 credits or more courses, and never fail (Not `F` in `Grade`) in any of the course they take. Return their `NetId`, `Name`, and total credits `totalCredits`.

## Requirements:

1. Write the SQL query for the following question;

2. Perform it on GCP to see if the result is correct. **Save the screenshot of the first 15 rows of result**.

3. Use `EXPLAIN ANALYZE` to see query performance. **Save the screenshots or output of the commands**.

4. Add **3 different indexes** on the database, and re-analyze the performances. **Save the screenshots or output of the commands**.

5. Reason on why the performance change. Write down your analysis.