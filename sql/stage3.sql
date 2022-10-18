SELECT *
FROM Students 
WHERE Department = 'CS' AND NetId IN (
    SELECT NetId
    FROM Enrollments e NATURAL JOIN Sections S
    WHERE CourseId LIKE 'ECE%'
)
UNION
SELECT *
FROM Students
WHERE Department = 'ECE' AND NetId IN (
    SELECT NetId
    FROM Enrollments e NATURAL JOIN Sections S
    WHERE CourseId LIKE 'CS%'
)
ORDER BY NetId;

SELECT NetId, Name, SUM(Credit) as totalCredit
FROM Students NATURAL JOIN Enrollments
WHERE NetId NOT IN (
    SELECT NetId
    FROM Enrollments
    WHERE Grade = 'F'
)
GROUP BY NetId
HAVING totalCredit >= 8
ORDER BY NetId;