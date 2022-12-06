**Team Name:** iloveCS411 (Team 013) 

**Project Title:** iCourse

### 1. Please list out changes in directions of your project if the final project is different from your original proposal (based on your stage 1 proposal submission).
There have been no changes in the directions of our project. We have created a course management system for both students and professors, and have a very simple and straightforward interface. 
 
### 2. Discuss what you think your application achieved or failed to achieve regarding its usefulness.
Our application is very simple, but provides powerful functionality. Students can search a large catalog for courses, view sections, then register for them. There is no other work necessary. They can also rate professors from directly within the application. For professors, they can manage many different sections and grades in one place, and not have to worry about many platforms.
 
### 3. Discuss if you changed the schema or source of the data for your application
Data for our application is the same (data for courses was taken from UIUC’s course explorer). There have also been no changes for the schema. 
 
### 4. Discuss what you change to your ER diagram and/or your table implementations. What are some differences between the original design and the final design? Why? What do you think is a more suitable design? 
THE ER diagram/table implementations have not changed. 
 
### 5. Discuss what functionalities you added or removed. Why?
One functionality that is not present in the final application is the ability of a user to change their password. This was mentioned to be a feature in the initial proposal, but due to time constraints, we did not get to it (as it was not as high of a priority). 
 
### 6. Explain how you think your advanced database programs complement your application.
We have a trigger where, if a professor changes the max capacity to some number less than the current number of enrolled students, the max capacity for that section just becomes the current number of enrolled students. This could be useful in cases where professors want to remove any extra seats or stop any new registrations. Our transaction is also useful since it handles situations in which two users could be registering for the same section. 
 
### 7. Each team member should describe one technical challenge that the team encountered.  This should be sufficiently detailed such that another future team could use this as helpful advice if they were to start a similar project or where to maintain your project. 
Ruipeng Ge:

Lumeng Xu:

Feiya Yu:

Alvin Zhang: One thing that was difficult was making the search results for courses dynamic (the table of classes changes depending on what keyword is entered and what is fetched from the database). This involved some Javascript code to insert components and remove them (grabbing an element, then adding to its innerHTML), which I was unfamiliar with in the beginning. 
 
### 8. Are there other things that changed comparing the final application with the original proposal?
One difference between the final application and the proposal is a commenting system for students to leave feedback on courses. We prioritized other more important aspects of the application and regretfully, did not get to this feature. 
 
### 9. Describe future work that you think, other than the interface, that the application can improve on
In the future, some things that can be added and improved for our application are as follows:
- Integrate IDP services for login, which would allow users to use their school credentials to access the system
- For the course explorer, it could be useful to have more filtering conditions, as well as filters for grade distributions
- Another feature that would be useful is to display a map to users showing where their classes are located, which would help users account for walking distance
- A useful improvement to the explorer functionality would be to automatically filter out sections that conflict with a user’s existing schedule
 

### 10. Describe the final division of labor and how well you managed teamwork. 
The work was split up depending on each member’s strengths and interests. Ahead of any project deadlines, the topics to be completed were always made known to everyone and distributed. Communication was done over WeChat, and it was where updates were given on project progress. 
 
The division of labor is as follows: 
Ruipeng Ge: Database functionality, Professor’s homepage for managing sections and grades, Student’s course history

Lumeng Xu: Database functionality

Feiya Yu: Worked on login and student homepage. Front-end development for these, and also Flask endpoints for login, drop courses, getting a student’s registered courses. 

Alvin Zhang: Worked on the course explorer page that shows course offerings and sections for those courses. Also added capability for students to enroll in sections. Did the frontend development for this, as well as the flask endpoints necessary. 

