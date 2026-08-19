# What I Learned

## 1. Django Project Design

i have have worked on a personal and company project during my internship so i know about the basic project folder structure but in that project i have added the test which i have not used earlier in the any project to run this type of test cases using pytest.

## 2. Box Selection Logic

In this project I learned how to handle different conditions before selecting a box. It is not only about checking the total weight. I learned that I also need to check the product dimensions in different rotations, the total volume of all items, and the packing efficiency.
I also learned that if multiple boxes can fit the order, we should select the cheapest one. If two boxes have the same cost, then the box with the smaller internal volume should be selected.
I also understood why we need to give a proper error when no box is suitable instead of only returning that no box was found.


## 3. Service Layer

I also learned that keeping business logic separate makes the views cleaner and easier to understand.
sometime i see the keep the actual logic somewhere is the plus points for a projects we can scale up our project, and it make reusable to mentioning that file also in django we have flexible coding to adding file and using whenever we want.

## 4. Testing with Pytest

working with the pytest is a new experience for me for that i get the help of AI like chatgpt, gemini and make test case scenarios to cover almost all points to test.

## 5. Debugging

after done of implementation of the project i have don't know the command to run the test environment in pytest for that i use go to pytest documentation and find the commands and related date to perform for the test cases.

I have face the problem of adding the less dimention in the test scenario in that time it is not taking for the rotate result that does not matching and it has getting my two test cases failed so after i do some research check the models and there defined validation and solve that to adding the correct input.
I checked the test data, the box dimensions, the packing efficiency, and the calculation used by the algorithm. 


## 6. API Development

i have setup all dependecies related to that project to add app names in settings added urls in core app but forget to add inside the main project folder to include that urls so that time my test cases failed after checking all i got that missmatch problem

also added that unneccessary status code for the resonse for the action i need to get 201 instead of 200 so that i have debug that point and use the chatgpt after getting all the requirement i implement that step by step and test in terminal all test cases which is arount 30 that all are pass and i added that inside test_output.md file


## 7. Overall Learning

this project is firstly new for me to add those requrements so i learn from this project to adding seperate logic to reuse and best for scalable the project also i learn little bit about the pytest and gather the all requiremnts by reserch on internet or any ai to get actual what ineed to implements in that project so i analyze that, and debug the problems i faced during the implementaion also i added this on github to i have now did some practice to git commands and use the postman for the getting the results for that i created collection so overall, I learned a lot from this assignment, especially about testing, debugging, separating business logic, API validation, and verifying the implementation against requirements. 