Report of Monaco 2018 Racing
----------------------------

This web application shows report of Monaco 2018 Racing.
Also it has restAPI. All data is stored in SQLite DB


Web interface
`````````````

The application has a few routes:

- http://localhost:5000/ - index page
- http://localhost:5000/report/ - shows general racing statistic
- http://localhost:5000/report/drivers/  - shows list of drivers name and code.
  Code has a link on info about driver
- http://localhost:5000/report/drivers/?driver_id=SVF shows info about a driver

Each route could get order parameter

- http://localhost:5000/report/drivers/?order=desc

API
```

There is restful API, available at http://localhost:5000/api/v1/ .
There is detailed specification which can be seen through swagger(http://localhost:5000/apidocs/).

Endpoints:

- http://localhost:5000/report/
- http://localhost:5000/report/<drivers_id>
- http://localhost:5000/drivers/

Query parameters:

- format [json|xml]