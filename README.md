# Discussion forum web-app
> App created for the course Databases and web-development course at University of Helsinki, using Python, Flask and PSQL.

## Intro
Web-app will be a familiar messaging board/ discussion forum, where users can post **messages** in different **topics** and **threads**, as well as create new topics and threads to discuss about.
The idea is a slightly modified version of the *"Discussion app"* example idea from the course page.

## Contents:
- [Features](#features)
- [Database Tables](#initial-plan-has-6-database-tables)
- [Current State](#current-state)
- [How to use](#how-to-use)
- [Notes](#notes)


## Features
- Users can log in and out **DONE**
- Users can create new account to login with **DONE**
- Users can see and interract with topics that are shown on the homepage of the application **DONE**
- ~Users can see when the last message was sent in each topic, as well as how many threads are under the topic~
- Users can create new *topics* **DONE**
- Users can create new *threads* under the topics **DONE**
- Users can send a new *message* under existing threads **DONE**
- Users can create and modify a user profile page **DONE**
- Admins can follow the activity on the app/page. **DONE**
- Admins can add and remove messages, threads and topics
- ~Admins can ban users~

### Initial plan has 6 database tables 
- *users* **DONE**
- *user profiles* **DONE**
- *topics* **DONE**
- *threads* **DONE**
- *messages* **DONE**
- *log* **DONE**

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


## How to use
App can be tested by following the instructions given on the course page on how ot run a flask app. 
For detailed instructions see [sovellus/instructions.md](sovellus/instructions.md)


## Notes
- goal is to get this project done quick, thus unlikely I will incorporate any extra features or a fancy interface.
- features as well as database tables are subject to change during the project


