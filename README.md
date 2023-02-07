# Fetch take home assignment

## How to run
1. Install docker: https://docs.docker.com/get-docker/
2. cd Fetch

3. ```docker build . -t fetch_assignment:v0 && docker run -p 8080:80 fetch_assignment:v0```
4. goto http://localhost:8080/index.html on your browser.

This will open up a website where you can upload your own data and get the results. You'll also get to see some beautiful graphs!


## More information
1. All of the Exploratory data analysis has been done in *fetch-eda.ipynb*. This can be referred to see why I chose the models I chose and how.
2. The training of the model and data pre processing that I have used is in *fetch-training.ipynb*

## How to run .ipynb files
1. Install requirements.txt and press Shift+Enter to run each code block in sequence.

## Future Scope
1. Get month wise sales.
2. Number of saturdays, sundays in each month and use that metric as people tend to spend more on weekends.
3. Adjust by a factor due to recession metrics and revenue loss of similar companies and integrate that into the model.
4. Day by month - since people spend more at the end and start of the month due to salaries.
5. Festivals in the month by weightage (black friday/Chirstmas increases sales by a lot! but independence day may not.)
6. Discounts by major companies in which months (Amazon sales, etc). This may increase the use of fetch rewards during that period
7. Get the year over growth of fetch by year and apply that percent to prediction. We can check the revenue increase of Fetch and take the average growth of company into account. (For eg. google suggested that this year the revenue was 84 million)
8. School holidays, events, etc.
9. Get more data! For may techniques more data would be needed. I could potentially use data aungmentation or few-shot learning but it doesnt seem like that would work very well. Apart from this it may require more time, data, and research.
