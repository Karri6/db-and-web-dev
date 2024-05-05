# Discussion forum web-app
> App created for the *'Databases and web-development'* course at University of Helsinki, using **Python, Flask** and **PSQL.**

## Intro
The web-app is a familiar messaging board/ discussion forum, where users can post **messages** in different **topics** and **threads**, as well as create new topics and threads to discuss about.
Admin user can view a complete log of what happens in the app and can be tested using the given admin profile in the *[instructions](sovellus/instructions.md).*\
The project idea is a slightly modified version of the *"Discussion app"* example idea from the course page.

---

## Contents:
- [How to use](#how-to-use)
- [Features](#features)
- [Database Tables](#database-tables)
- [Current State](#current-state)

--- 

## How to use
App can be tested by following the instructions given on the course page on how to run a flask app. 
For more detailed instructions see [sovellus/instructions.md](sovellus/instructions.md)

---

## Features
- Users can log in and out **DONE**
- Users can create new account to login with **DONE**
- Users can see and interract with topics that are shown on the homepage of the application **DONE**
- Users can create new *topics* **DONE**
- Users can create new *threads* under the topics **DONE**
- Users can send a new *message* under existing threads **DONE**
- Users can create and modify a user profile page **DONE**
- Admins can follow the activity on the app/page. **DONE**

### unfinished features that were in the origirnal plan
- Users can see when the last message was sent in each topic, as well as how many threads are under the topic
- Admins can add and remove messages, threads and topics
- Admins can ban users

--- 

## Database tables
- *users* **DONE**
  - user details as username and user id
- *user profiles* **DONE**
  - user profile details such as name, age, bio
- *topics* **DONE**
  - topics posted on the page
- *threads* **DONE**
  - threads posted under topics, connected with topic id
- *messages* **DONE**
  - messages posted under threads, connected with thread id
- *log* **DONE**
  - a complete log of every event that occurs in the website

--- 

## Current State 
### (7.4.-24)
- User can Create new profile (username and password) or login with previously created username and password.
- User can Interact and Add new topics on the homepage
- User can Add new Threads under the topics
- User can Send new messages under the threads

### (24.4.-24)
- User can view their personal profile
- User can edit their personal profile
- App logs every action to a separate log table
- Admin user can log in
- Admin user can view the logs in an Admin only page

### (2.5.-24)
- Updated sql queries to match given criteria
- Added csrf protection
- Simple styling with a css style sheet

### (5.5.-24)
- Finalized project
- Updated and cleaned readme.md  
