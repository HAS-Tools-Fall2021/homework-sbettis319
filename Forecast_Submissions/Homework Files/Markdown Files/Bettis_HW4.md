Sierra Bettis
HAS Tools - 401
Sepetmber 19, 2021

_________
## Grade: 
3/3: Good work! I didn't take off points but here are some comments for things to work on and check out in the solution. 
- For question 1 remember all of the data have to be the same thing in a numpy array. So now they are all floats. 
- For questions 3&4 I noted in class last week you shoul divide by the total number of september days not the total number of days. This is why your percentages are so low. You can check the solution for examples of how to do this. 
- Question 5: your answers on this one are skewed a little high because you are only taking the average of the flow greater than 140cfs based on your conditional statement. 
- I still don't see any markdown formatting. If you have questions about how to insert that let me know but please make sure to try out some of that next time.  Also note that you need to save your files as .md files for them to be markdown files. I added the extension to this one but you should add in the future. 
_________

1. Provide a summary of the forecast values you picked and why. 
Include discussion of the quantitative analysis that lead to your
prediction. This can include any analysis you complete but must 
include at least two histograms and some quantitative discussion
of flow quantiles that helped you make your decision.

I think that the flow might increase at the end of September, also
based on last weeks prediction. For the first histogram, I just looked
at the average flow in all of September and the average for flow was
230.93 cfs when the flow was greater than 100. The flow in September
has an average value of 79.95 cfs when the flow is less than 100. 
I also did an average of all the years for when flow is less than 100 for the 20th of Sepetmber, is 82.3 cfs and when it is greater than 100
cfs, the value is 203.9 cfs. So, the value I chose for this week is 140 cfs and 150cfs for the 2nd week based on the same characteristics.

1. Describe the variable flow_data:

What is it?
Numpy (ndarray)

What type of values is is composed of?
It is composed of flow, month, year, and day data as integers.

What is are its dimensions, and total size?
The dimensions are 2 and the total size is (11936,4)

3. How many times was the daily flow greater than your prediction 
in the month of September (express your answer in terms of the 
total number of times and as a percentage)?

301 - 2.5%

4. How would your answer to the previous question change if you 
considered only daily flows in or before 2000? Same question for 
the flows in or after the year 2010? (again report total number 
of times and percentage)

2000 --> 317 - 2.6%
2010 --> 225 - 1.9%

5. How does the daily flow generally change from the first half 
of September to the second?

From the numpys I created, the flow in the second half of September is greater than the first half. The flow in the second half of September has a mean flow of 340 cfs and the mean flow of the first half of September is 275 cfs. 