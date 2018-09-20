# Endpoints

`/api/v1` - general prefix

## Project
GET `/projects` - list of all projects  
GET `/projects/:id` - project with :id  
POST `/projects` - create new project  
PATCH `/projects/:id` - update project  

## Build
GET `/projects/:id/builds` - list of all builds per project  
GET `/projects/:id/builds/:id` - build with :id  
POST `/projects/:id/builds` - create new build  
PATCH `/projects/:id/builds/:id` - update build  

## Test Run
GET `/projects/:id/builds/:id/runs` - list of all runs per build  
GET `/projects/:id/builds/:id/runs:id` - run with :id  
POST `/projects/:id/builds/:id/runs` - create new run  
PATCH `/projects/:id/builds/:id/runs/:id` - update run

## Test
GET `/projects/:id/tests` - list of all tests per project  
GET `/projects/:id/tests/:id` - test with :id  
POST `/projects/:id/tests` - create new test(s) //can be an array of [test_names]  
PATCH `/projects/:id/tests/:id` - update test

## Test Result
GET `/projects/:id/builds/:id/runs:id/results` - list of all results per test run  
GET `/projects/:id/builds/:id/runs:id/results/:name` - result of test :name  
POST `/projects/:id/builds/:id/runs:id/results` - create new result  
PUT `/projects/:id/builds/:id/runs:id/results/:name` - update or create test result of test :name
PATCH `/projects/:id/builds/:id/runs:id/results/:name` - update test result of test :name

### Special view of the results
GET `/projects/:id/tests/:name/results` - all results of a given test

#### Optional parameters  
`?buildId=1` - filter by build id  
`?runId=1` - filter by test run id  
`?items=10` - get only last 10 items   
`?since=YYYY-MM-DDTHH:MM:SSZ` - get only items after this date   
`?until=YYYY-MM-DDTHH:MM:SSZ` - get only items before this date   