Report of Monaco 2018 Racing
----------------------------

This application can build racing report from `web_report/static/report_data`
and represent it in web

There is submodule `web_report/racing_report` that builds report into instance of `Report` class

The application has a few routes:

- http://localhost:5000/ - index page
- http://localhost:5000/report - shows general racing statistic
- http://localhost:5000/report/drivers/  - shows list of drivers name and code. Code has a link on info about driver
- http://localhost:5000/report/drivers/?driver_id=SVF shows info about a driver

Also, each route could get order parameter

- http://localhost:5000/report/drivers/?order=desc