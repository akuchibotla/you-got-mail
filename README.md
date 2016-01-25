# you-got-mail
This is a tool used to determine emails based on the name of a person and a couple URLs of various social media accounts (namely LinkedIn, AngelList, Twitter)

### Dependencies
#### BeautifulSoup 4

### Social Media Username Restrictions
##### LinkedIn
(a-z), (0-9)
##### Angel List
N/A but seems like no symbols work when I try
##### Twitter
(a-z), (0-9), (_)

Social network accounts are constructed with letters and numbers generally.

### Email Username Restrictions
##### GMail
(a-z), (0-9), (-), (_), ('), (.)
##### Yahoo
(a-z), (0-9), (_), (.)
##### Hotmail
(a-z), (0-9), (-), (_), (.)
##### AOL
(a-z), (0-9), (_), (.)

Emails are constructed with letters, numbers, underscores and periods.

### Username Weightage
Given a person's name and links as well as the information provided above on what a valid username is, here is how the weightage process works:

1) Usernames that are represented in more than one link are weighted higher (i.e. if someone had www.linkedin.com/in/foobar, www.angel.co/randomusername, and www.twitter.com/foobar, then 'foobar' has a more favored weight than 'randomusername')

2) Usernames are ranked by their content. Below is a rough guideline for how usernames that are constructed out of specific categories are weighted:
- only letters (weightage = 1.0)
- only letters & numbers (weightage = 0.85)
- only letters & symbols (weightage = 0.85)
- letters, numbers & symbols (weightage = 0.7)
- only numbers (weightage = 0.3)
- only numbers & symbols (weightage = 0.2)
- only symbols (weightage = 0.1)

Here, symbols refer to exclusively underscores and periods. The reason for this weightage is because people tend to prefer using emails that are purely character based with maybe a few numbers or symbols if they have a common name. People will rarely combine letters, numbers, and symbols together or have exclusively numbers and symbols.