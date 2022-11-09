"""Defines all the functions related to the database"""

from app import db

def login(NetId, Password):
    conn = db.connect()
    results = conn.execute("SELECT * FROM UserInfo WHERE NetId='{}'".format(NetId)).fetchall()
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
    ===============================================================================
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
    WHERE NetId = '{}' AND semester = '{}'".format(netId, semester)
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
        3. Else, prevent the drop and return an error code (e.g. 1 for course not found, 2 for invalid drop, ... you can define for yourself)
    Output:
    -- return value (int): indicating dropping successful or not.
    '''
    raise NotImplementedError
    return -1

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
    '''
    raise NotImplementedError
    return -1

def keyword_course_search(keyword):
    '''
    Given a keyword, search all relavant course information and return.
        (Title contains keyword)
    Input:
    -- keyword (string): 
    Output:
    -- course_lst (list): a list, each item is a tuple of **course** information including
        CourseId, Title, Department, Number of Sections, Enrolled Student number, Capacity
        e.g. [
            ['CS999', 'Some Title', 'CS', 3, 48, 50],
            ['CS888', 'Another Title', 'CS', 4, 100, 100]
        ]
    PS: You may need to use GROUP BY and aggregation functions for this operation.
    '''
    raise NotImplementedError
    return []

def show_sections(courseId):
    '''
    Show all sections given a course id.
    Input:
    -- CourseId (string):
    Output:
    -- section_lst (list): a list, each item is a tuple of **section** information including
        CRN, Lecture Type, Lecture Time, Location, Avaliable Credits(list), Instructor Names(list), Enrolled Student Number, Capacity, Restrictions
        e.g. [
            [00001, 'Lecture-Discussion', 'MON09:00am-10:15am', 'CIF 3039', [3, 4], ['Anna John', 'Bob Keith'], 10, 15, '']
        ]
    PS: You may use several SEARCH queries and process the data
    '''
    raise NotImplementedError
    return []

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
    '''
    raise NotImplementedError
    return -1

def student_search(condition):
    raise NotImplementedError
    return []

'''
def fetch_todo() -> dict:
    """Reads all tasks listed in the todo table

    Returns:
        A list of dictionaries
    """

    conn = db.connect()
    query_results = conn.execute("Select * from tasks;").fetchall()
    conn.close()
    todo_list = []
    for result in query_results:
        item = {
            "id": result[0],
            "task": result[1],
            "status": result[2]
        }
        todo_list.append(item)

    return todo_list


def update_task_entry(task_id: int, text: str) -> None:
    """Updates task description based on given `task_id`

    Args:
        task_id (int): Targeted task_id
        text (str): Updated description

    Returns:
        None
    """

    conn = db.connect()
    query = 'Update tasks set task = "{}" where id = {};'.format(text, task_id)
    conn.execute(query)
    conn.close()


def update_status_entry(task_id: int, text: str) -> None:
    """Updates task status based on given `task_id`

    Args:
        task_id (int): Targeted task_id
        text (str): Updated status

    Returns:
        None
    """

    conn = db.connect()
    query = 'Update tasks set status = "{}" where id = {};'.format(text, task_id)
    conn.execute(query)
    conn.close()


def insert_new_task(text: str) ->  int:
    """Insert new task to todo table.

    Args:
        text (str): Task description

    Returns: The task ID for the inserted entry
    """

    conn = db.connect()
    query = 'Insert Into tasks (task, status) VALUES ("{}", "{}");'.format(
        text, "Todo")
    conn.execute(query)
    query_results = conn.execute("Select LAST_INSERT_ID();")
    query_results = [x for x in query_results]
    task_id = query_results[0][0]
    conn.close()

    return task_id


def remove_task_by_id(task_id: int) -> None:
    """ remove entries based on task ID """
    conn = db.connect()
    query = 'Delete From tasks where id={};'.format(task_id)
    conn.execute(query)
    conn.close()
'''