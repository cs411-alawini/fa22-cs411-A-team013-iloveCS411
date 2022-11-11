"""Defines all the functions related to the database"""

from app import db

DEFAULT_SEM = 'SP23'

def login(NetId, Password):
    conn = db.connect()
    results = conn.execute("SELECT * FROM UserInfo WHERE NetId='{}';".format(NetId)).fetchall()
    print(results)
    if len(results) == 0:
        ret = 2 # No User
        conn.close()
        return ret
    true_pw = results[0][1]
    user_type = results[0][2]
    print(NetId, Password, true_pw, user_type, results[0][0], len(results))
    if Password != true_pw:
        ret = 3 # password failed
        conn.close()
        return ret
    ret = 0 if user_type=='Student' else 1
    conn.close()
    return ret

def show_schedule(netId, semester):
    '''
    Search for course schedule given netId and semester.
    Input:
    -- netId (string): NetId of a student
    -- semester (string): given semester (e.g. FA22 or SP23)
    Output:
    -- schedule (list): each item of schedule is a tuple including course information
        CRN, CourseId, Title, LectureType, LectureTime, Location, Credit, Grade
    =================================
    e.g. 
    Input: 'ruipeng4', 'FA22'
    Output:
    [
        (35852, 'CS476', 'Program Verification', 'Lecture-Discussion', 'TUE09:30AM-10:45AM,THU09:30AM-10:45AM', 'Transportation Building 101', 3, 'A+'), 
        (63293, 'CS447', 'Natural Language Processing', 'Online', '', 'None None', 4, 'A+'), 
        (74468, 'CS441', 'Applied Machine Learning', 'Online Lecture', '', 'None None', 4, 'A+'), 
        (75726, 'CS411', 'Database Systems', 'Lecture', 'MON03:30PM-04:45PM,WED03:30PM-04:45PM', 'Campus Instructional Facility 3039', 3, 'A+')
    ]
    '''
    conn = db.connect()
    query = "SELECT CRN, CourseId, Title, LectureType, LectureTime, Location, Credit, Grade \
    FROM Enrollments NATURAL JOIN Sections NATURAL JOIN Courses \
    WHERE NetId = '{}' AND semester = '{}';".format(netId, semester)
    results = conn.execute(query).fetchall()
    ret = [x for x in results]
    conn.close()
    print(ret)
    return ret

def drop(netId, CRN):
    '''
    Drop a given course.
    PS: You should check eligibility before dropping a course, including:
        1. If the CRN is not enrolled by the student, return an error;
        2. If a Grade is already granted for the course, prevent drop and return an error;
    WARNING: You should always be cautious when performing DELETE queries!
    Input: 
    -- netId (string): NetId of a student
    -- CRN (int): CRN of a section
    Operation:
        1. Check if the course can be dropped.
        2. If the course can be dropped, delete it from Enrollment, return 0 (success)
        3. Else, prevent the drop and return an error code 
    Output:
    -- return value (int): indicating dropping successful or not.
        return 0: Drop success.
        return 1: Invalid, the given CRN is not enrolled by the student.
        return 2: Invalid, a grade is already asserted, cannot drop at this stage.
    '''
    conn = db.connect()
    query1 = "SELECT CRN, Grade FROM Enrollments WHERE NetId = '{}' AND CRN = {};".format(netId,CRN)
    result1 = conn.execute(query1).fetchall()
    #print(result1)
    if len(result1) == 0:
        ret = 1 # the CRN is not enrolled by the student
        conn.close()
        return ret
    if result1[0][1] != None:
        ret = 2 # a Grade is already granted for the course
        conn.close()
        return ret
    
    del_query = "DELETE FROM Enrollments \
        WHERE NetId = '{}' AND CRN = {};".format(netId, CRN)
    conn.execute(del_query)
    print("delete success!")
    conn.close()
    return 0

def credit_avail(prompt, credit):
    if prompt.find(",") != -1:
        lst = prompt.strip().split(",")
        low = int(lst[0])
        high = int(lst[1])
        return credit == low or credit == high
    elif prompt.find("-") != -1:
        lst = prompt.strip().split("-")
        low = int(lst[0])
        high = int(lst[1])
        return credit >= low and credit <= high
    else:
        return credit == int(prompt.strip())

def min_credit(prompt):
    if prompt.find(",") != -1:
        lst = prompt.strip().split(",")
        low = int(lst[0])
        return low
    elif prompt.find("-") != -1:
        lst = prompt.strip().split("-")
        low = int(lst[0])
        return low
    else:
        return int(prompt.strip())

def change_credit(netId, CRN, credit):
    '''
    Change credit for a given course.
    PS: You should check eligibility before update, including:
        1. If the CRN is not enrolled by the student, return an error;
        2. If a Grade is already granted for the course, prevent update and return an error;
        3. If the credit is not avaliable for the course, prevent update and return an error;
    Input: 
    -- netId (string): NetId of a student
    -- CRN (int): CRN of a section
    -- credit (int): credit to be changed.
    Operation:
        1. Check if the course credit can be updated.
        2. If can, make update, return 0 (success)
        3. Else, prevent the update and return an error code (e.g. 1 for course not found, 2 for invalid update, ... you can define for yourself)
    Output:
    -- return value (int): indicating update successful or not.
        return 0: Update Success
        return 1: Invalid: No enrollment records found for this student given CRN
        return 2: Invalid: A grade is already asserted and cannot update at this stage
        return 3: Invalid: The input credit is not avaliable for this course
    '''
    conn = db.connect()
    print(netId, CRN, credit)
    credit = int(credit)
    query1 = "SELECT CRN, Grade FROM Enrollments WHERE NetId = '{}' AND CRN = {};".format(netId,CRN)
    result1 = conn.execute(query1).fetchall()
    #print(result1)
    if len(result1) == 0:
        ret = 1 # the CRN is not enrolled by the student
        print("CRN not found in Enrollments")
        conn.close()
        return ret
    if result1[0][1] != None:
        ret = 2 # a Grade is already granted for the course
        print("Grade already granted")
        conn.close()
        return ret
    query3 = "SELECT AvaliableCredits FROM Sections WHERE CRN = {};".format(CRN)
    result3 = conn.execute(query3).fetchall()
    prompt = result3[0][0]
    if not credit_avail(prompt, credit):
        print("Credit not avaliable.")
        ret = 3
        conn.close()
        return ret
    query4 = "UPDATE Enrollments SET Credit = {} WHERE NetId = '{}' AND CRN = {};".format(credit,netId,CRN)
    conn.execute(query4)
    print("update success.")
    conn.close()
    return 0

def keyword_course_search(keyword):
    '''
    Given a keyword, search all relavant course information and return.
        (Title contains keyword, case insensitive)
    Input:
    -- keyword (string): 
    Output:
    -- course_lst (list): a list, each item is a tuple of **course** information including
        CourseId, Title, Department, Enrolled Student number, Capacity
    ===========================
    e.g.
    Input: "data"
    Output:
    [
        ('CS107', 'Data Science Discovery', 'CS', 0, 330), 
        ('CS225', 'Data Structures', 'CS', 0, 2493), 
        ('CS307', 'Modeling and Learning in Data Science', 'CS', 0, 75), 
        ('CS411', 'Database Systems', 'CS', 0, 1586), 
        ('CS412', 'Introduction to Data Mining', 'CS', 0, 600), 
        ('CS511', 'Advanced Data Management', 'CS', 0, 93), 
        ('CS512', 'Data Mining Principles', 'CS', 0, 150), 
        ('ECE365', 'Data Science and Engineering', 'ECE', 0, 198), 
        ('ECE471', 'Data Science Analytics using Probabilistic Graph Models', 'ECE', 0, 120), 
        ('FIN550', 'Big Data Analytics in Finance for Predictive and Causal Analysis', 'FIN', 0, 196)
    ]

    '''
    # raise NotImplementedError
    conn = db.connect()
    course_query = "SELECT CourseId, Department, Title\
        FROM Courses\
        WHERE upper(Title) LIKE '%%{}%%';".format(keyword.upper())
    course_lst = conn.execute(course_query).fetchall()
    res = []
    for course in course_lst:
        courseId = course[0]
        department = course[1]
        title = course[2]
        cap_query = "SELECT SUM(Capacity) FROM Sections WHERE CourseId = '{}';".format(courseId)
        capacity = conn.execute(cap_query).fetchall()[0][0]
        num_query = "SELECT COUNT(*) FROM Enrollments \
            WHERE CRN IN (SELECT CRN FROM Sections WHERE CourseId = '{}') \
            AND Semester = '{}';".format(courseId, DEFAULT_SEM)
        num_enrolled = conn.execute(num_query).fetchall()[0][0]
        res.append((courseId, title, department, num_enrolled, int(capacity)))
    conn.close()
    print(res)
    return res

def show_sections(courseId):
    '''
    Show all sections given a course id.
    Input:
    -- CourseId (string):
    Output:
    -- section_lst (list): a list, each item is a tuple of **section** information including
        CRN, Lecture Type, Avaliable Credits, Lecture Time, Location, Instructor Names, Capacity, Restrictions
    ============================
    e.g. 
    Input: "CS173"
    Output:
    [
        (30102, 'Lecture', '3', 'TUE09:30AM-10:45AM,THU09:30AM-10:45AM', 'Campus Instructional Facility 3039', 'Cosman, Benjamin', '0/300', 'Grad cannot Enroll'), 
        (40083, 'Lecture', '3', 'TUE03:30PM-04:45PM,THU03:30PM-04:45PM', 'Campus Instructional Facility 0027/1025', 'Cosman, Benjamin', '0/483', 'Grad cannot Enroll'), 
        (72280, 'Lecture', '3', 'TUE09:30AM-10:45AM,THU09:30AM-10:45AM', 'Campus Instructional Facility 3039', 'Cosman, Benjamin', '0/300', 'Grad cannot Enroll'), 
        (72281, 'Lecture', '3', 'TUE03:30PM-04:45PM,THU03:30PM-04:45PM', 'Campus Instructional Facility 0027/1025', 'Cosman, Benjamin', '0/483', 'Grad cannot Enroll')
    ]
    '''
    # raise NotImplementedError
    conn = db.connect()
    query = "SELECT CRN, LectureType, AvaliableCredits, LectureTime, Location, Capacity, Restrictions \
        FROM Sections \
        WHERE CourseId = '{}';".format(courseId)
    section_lst = conn.execute(query).fetchall()
    res = []
    for section in section_lst:
        crn = section[0]
        ltype = section[1]
        credits = section[2]
        time = section[3]
        location = section[4]
        instruct_query = "SELECT p.Name FROM Instruct i JOIN Professors p ON (i.Professor = p.NetId) WHERE i.CRN = {};".format(crn)
        name_lst = conn.execute(instruct_query).fetchall()
        instructors = ""
        for i in range(len(name_lst)):
            name = name_lst[i]
            instructors += name[0]
            if i < len(name_lst)-1:
                instructors += "; "
        num_query = "SELECT COUNT(*) FROM Enrollments WHERE CRN = {} AND Semester = '{}';".format(crn, DEFAULT_SEM)
        num_enrolled = conn.execute(num_query).fetchall()[0][0]
        capacity = str(num_enrolled)+"/"+str(section[5])
        restrict_raw = section[6]
        if restrict_raw == 'U':
            restriction = "Undergrad cannot Enroll"
        elif restrict_raw == 'G':
            restriction = "Grad cannot Enroll"
        else:
            restriction = "No Level Restrictions"
        res.append((crn, ltype, credits, time, location, instructors, capacity, restriction))
    conn.close()
    print(res)
    return res

def enroll(netId, CRN):
    '''
    Enroll in Sections.
    PS: You should check eligibility before inserting data into database, including:
    - 1. Check restrictions and Level of student
    - 2. Check Capacity of the section
    - 3. Check if the students enrolled in the course before (have records of enrollment of the same CourseId)
    Input
    - netId (string)
    - CRN (int)
    Output
    -- return value (int): indicating insert successful or not.
        return 0: Enroll Success
        return 1: Invalid. Level Restrictions prevent enrollment.
        return 2: Invalid. Exceed Capacity.
        return 3: Invalid. Already enrolled in this section.
    '''
    #raise NotImplementedError
    #return -1 
    conn = db.connect()
    query1 = "SELECT Level FROM Students WHERE NetId = '{}';".format(netId)
    query2 = "SELECT Restrictions FROM Sections WHERE CRN = {};".format(CRN)
    result1 = conn.execute(query1).fetchall()
    result2 = conn.execute(query2).fetchall()
    if result1[0][0] == "Undergrad" and result2[0][0].find("U") != -1:
        ret = 1 # it has restriction to this student
        print("Restrictions.")
        conn.close()
        return ret
    elif result1[0][0] == "Grad" and result2[0][0].find("G") != -1:
        ret = 1 # it has restriction to this student
        print("Restrictions.")
        conn.close()
        return ret
    query3 = "SELECT COUNT(NetId) FROM Enrollments WHERE CRN = {} AND Semester = '{}';".format(CRN, DEFAULT_SEM)
    query4 = "SELECT Capacity, AvaliableCredits FROM Sections WHERE CRN = {};".format(CRN)
    result3 = conn.execute(query3).fetchall()
    result4 = conn.execute(query4).fetchall()
    if 1 + result3[0][0] > result4[0][0]:
        ret = 2 # it exceeds the capacity
        print("Capacity.", result3[0][0], result4[0][0])
        conn.close()
        return ret
    query5 = "SELECT CRN FROM Enrollments WHERE CRN = {} AND NetId = '{}';".format(CRN, netId)
    result5 = conn.execute(query5).fetchall()
    if len(result5) != 0:
        ret = 3 # the student has enrolled in this class before
        print("Enrolled.")
        conn.close()
        return ret
    cr = min_credit(result4[0][1])
    query6 = "INSERT INTO Enrollments (CRN, NetId, Semester, Credit) VALUES ({}, '{}', '{}', {});".format(CRN,netId,DEFAULT_SEM,cr)
    conn.execute(query6)
    print("insert success.")
    conn.close()
    return 0

def student_search(condition):
    raise NotImplementedError
    return []

