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

If you implement it correctly and sort the result by `NetId`, you will get the following result:
```
+--------+---------------------+------------+-------+
| NetId  | Name                | Department | Level |
+--------+---------------------+------------+-------+
| csg100 | Cerrillo, Andrzej   | CS         | Grad  |
| csg130 | Geracimos, Antonin  | CS         | Grad  |
| csg152 | Hiu, Malkeet        | CS         | Grad  |
| csg19  | Barrallo, Shushanik | CS         | Grad  |
| csg198 | Ulpiani, Hassie     | CS         | Grad  |
| csg199 | Juhre, Lahat        | CS         | Grad  |
| csg22  | Gottes, Salec       | CS         | Grad  |
| csg31  | De Martin, Sondos   | CS         | Grad  |
| csg45  | Burwinkel, Trey     | CS         | Grad  |
| csg88  | Ynchaurraga, Faust  | CS         | Grad  |
| eceg1  | Avril, Haby         | ECE        | Grad  |
| eceg14 | Falae, Arola        | ECE        | Grad  |
| eceg25 | Hauswirth, Ignaci   | ECE        | Grad  |
| eceg37 | Ereyñoz, Ionatan    | ECE        | Grad  |
| eceg47 | Dente, Andriu       | ECE        | Grad  |
| eceg49 | Ziereisen, Claustro | ECE        | Grad  |
| eceg53 | Faist, Yongsheng    | ECE        | Grad  |
| eceg57 | Casais, Donata      | ECE        | Grad  |
| eceg68 | Dyson, Ange         | ECE        | Grad  |
| eceg80 | Mairena, Humilde    | ECE        | Grad  |
+--------+---------------------+------------+-------+
```

## Question 2

Write a MySQL query to find all students who take 8 credits or more courses, and never fail (Not `F` in `Grade`) in any of the course they take. Return their `NetId`, `Name`, and total credits `totalCredits`.

If you implement it correctly and sort the result by `NetId`, you will get the following result:
```
+--------+----------------------------+-------------+
| NetId  | Name                       | totalCredit |
+--------+----------------------------+-------------+
| csg1   | Koorts, Kristian           |          10 |
| csg14  | Kirchmann, Orkatz          |          10 |
| csg25  | Rodriguez Bobada, Xiaoping |          10 |
| csg37  | Noizet, Castro             |          10 |
| csg47  | Lemmens, Cleide            |          10 |
| csg49  | Zhestkov, Pearlene         |          10 |
| csg53  | Uselli, Eidan              |          10 |
| csg57  | El Oujgli, Strahil         |          10 |
| csg68  | Praveen, Jader             |          10 |
| csg80  | Niehnhaus, Ria             |          10 |
| eceg18 | Subramani, Mohit           |          10 |
| eceg24 | Lucie, Melvina             |          10 |
| eceg3  | Koneke, Tasia              |          10 |
| eceg38 | Hell, Galileo              |          10 |
| eceg39 | Kouba, Xiaorong            |          10 |
| eceg65 | Ziemke, Geovane            |          10 |
| eceg7  | Meira, Manue               |          10 |
| eceg79 | Lartirigoyen, Danilo       |          10 |
| eceg81 | Agostinelli, Masiel        |          10 |
| eceg99 | Utande, Dionila            |          10 |
+--------+----------------------------+-------------+
```

## Requirements:

1. Write the SQL query for the following question;

2. Perform it on GCP to see if the result is correct. **Save the screenshot of the first 15 rows of result**.

3. Use `EXPLAIN ANALYZE` to see query performance. **Save the screenshots or output of the commands**.

4. Add **3 different indexes** on the database, and re-analyze the performances. **Save the screenshots or output of the commands**.

5. Reason on why the performance change. Write down your analysis.