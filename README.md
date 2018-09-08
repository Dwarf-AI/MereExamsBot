<p align="center">
<img src="https://scontent.fdel13-1.fna.fbcdn.net/v/t1.0-9/17098151_1566835299996458_6420650479652519534_n.png?_nc_cat=0&oh=27ae9f019abaaaddb93e9173f2267a93&oe=5C2E20AE" width = 300 height = 300/>
</p>

[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)

[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=shields)](http://makeapullrequest.com)
![Python Version](https://img.shields.io/badge/pypi-python3.6-blue.svg)

# Rancho
- [Inspiration](#inspiration)
- [Idea](#idea)
- [Features](#features)
    + [CollegeDetail](#collegedetail)
    + [List](#list)
- [Dataset](#dataset)
- [Dependencies](#dependencies)
- [What's Next](#what-s-next)

## Inspiration
Students experience a lot of informative hindrances while searching for education guidance. They have to spend lots of their precious time in searching institution websites which are usually cluttered. Other ed-guide platforms are interested in only collecting email id’s and forwarding to private colleges as leads.

## Idea
We decided to create a chatbot which we will be beneficial for students and something that can answer any of their query and give advice in very personalised and time efficient manner by using latest advances of AI and NLP.

## Features
Every Intent is itself a feature. DialogFlow will help chatbot in understanding what feature user want to use and then rest of work will happen on backend. These are the main features of chatbot.
* [CollegeDetail](#collegedetail)
* [List](#list)
##### CollegeDetail 
Main purpose of CollegeDetail is to provide user any information about any college in user-friendly and personalised way.
* User can ask details about any college.
* Some query examples:
  * `Photos of IITD`
  * `Is there library in IITD`
  * `Intake of IIMA in marketing`
* Context will save all entities to understand next chat in better way.
* Instead of following basic tree like structure which DialogFlow provides, it is exceptionally good in understanding any request at any moment handling contexts well.
##### List
Main purpose of List feature is to provide user list of colleges or courses based on given and saved parameters.
* List is based on two heirarchical entities - `user_desire` and `parameters`.
  * **user_desire** - *user_desire* understands 'list of which parameter user is asking'. It mainly contains - *colleges, programme (degrees) and discipline.*
    * Eg. `list of colleges` , `show me courses`.
  * **parameters** - *parameters* contain parameters on based of which user want to filter the list. It mainly contains - *state, city or district, courses, disciplines, universities, ownership*.
    * Eg. `colleges in faridabad` , `best mba colleges for marketing`.
* Like *College_detail*, *List* intent is also very flexible when handling contexts.
## Sample Chat

> **USER:** Good morning! How are you doing?
>
> **RANCHO:** I am doing very well, thank you for asking.
>
> **USER:** What you can do?
>
> **RANCHO:** I can help you find colleges based on your interests.
>
> **RANCHO:** Along with that, I can also tell you info about any college.
>
> **USER:** Then tell me what you know about IITD?
>
> **RANCHO:** Indian Institute Of Technology, Delhi was established in 1961. It is one of the top colleges of India. College contains major facilities like auditorium library conference hall gymnasium indoor stadium and many other student friendly things. Foreign students are also allowed to take admissionThey also offer scholarship to students depending on criteria.
> 
> **USER:** Can you show me some pics also?
> 
> **RANCHO:** Sure. Here are some from Google
> 
> ![](https://github.com/i-amgeek/MereExamsBot/blob/master/images/iitd_pics.png)
>
> **USER:** awesome! I wanna visit this college.
>
> **RANCHO:** Well, my friend Google told me this address.
>
> <p><img src="https://github.com/i-amgeek/MereExamsBot/blob/master/images/iitd_location.png" width = 300 height = 200/></p>
>
> **USER:** Thanks :+1: .
>
> **RANCHO:** Glad you liked it. :smile:
>
> **USER:** BTW whats the intake for Btech mechanical here?
>
> **RANCHO:** 103 students as per MHRD data.
>
> **USER:** It's out of scope. Help me find other colleges.
>
> **RANCHO:** Any specific location you want to study?
>
> **USER:** Yeah, I am looking for Colleges in Delhi and Haryana only.
>
> **RANCHO:** These are the colleges for BTech mechanical in Delhi and Haryana.
>
> **RANCHO:** {Top 10 colleges} / {show more}
>
> **USER:** And what about electrical?
>
> **RANCHO:** Here are colleges for BTech Electrical in Delhi and Haryana.
>
> **RANCHO:** {Top 10 colleges} / {show more}
>
> **USER:** Thanks RANCHO! You are awesome.
>
> **RANCHO:** Awww yea! :blush:

## Architecture
So what's happening behind the scene?

**UI** ⮕ Frontend Service Sends user message to dialogflow.

                                   ⤋

**DIALOGFLOW** ⮕ Dialogflow performs intent classification on user message.

                                   ⤋

**SERVER** ⮕ Server recieves POST request and processing begins.

                                   ⤋
**UPDATE CONTEXTS** ⮕ Parameters recived from dialogflow are used to update contexts. 

                                   ⤋

**NEW CONTEXTS** ⮕ New context is created based on previously saved context and new parameters from request.

                                   ⤋

**DATABASE QUERY** ⮕ Fetch data from database according to user intention.

                                   ⤋

**MAKE RESPONSE** ⮕ Generate random responses to answer user.

                                   ⤋

**DIALOGFLOW** ⮕ Dialogflow forwards recieved message to UI client.

                                   ⤋

**UI** ⮕ UI renders the JSON and show message to the user.

## Dataset
To maintain transparency and reliability, we use Dataset provided by [MHRD](http://mhrd.gov.in/) and Google Location.
## Dependencies
Making this awesome chatbot would not be possible without these technologies and libraries.
* [Python 3.6]()
* [Pandas]()
* [Scikit-Learn]()
* [DialogFlow]()
* [Flask]()
* [SQL]()

## What's Next
* College Predictor - Tells user Colleges they can get with their scores in competitive exams. Eg. `What colleges I can get with 5343 rank in JEE Mains` .
* College Comparison - User will be able to compare two or more colleges on based of parameters given. Eg. `which is better placement wise - IITD or IITK` .
* Counsellor - Can give complete guidance to students from data analysis. Eg. `Which B.Tech branch should I choose for better future opportunities` .
