# you-got-mail
This is a tool used to determine emails based on the name of a person and a couple URLs of various social media accounts (supported accounts are LinkedIn, AngelList, GitHub, and Twitter)

### Dependencies
BeautifulSoup 4

### API Usage
Email Hippo (Obtain a free key for up to 200 requests at https://www.emailhippo.com)

If you would like to use another API, feel free to replace `email_verifier.py` to whatever you'd like

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

### Workflow
1) Information is entered by the user (the more information, the better)

2) Possible usernames are generated via link usernames and via hardcoding popular usernames for first and last name combinations (such as "firstname_lastname")

3) These usernames are weighted by content as described above

4) Domains and social media accounts are crawled, scraped, and regex is used to determine whether or not emails exist within them and in the case that they do, they are weighted highly

5) Usernames get linked to the most popular email providers (GMail, Yahoo, Hotmail, AOL) as well as personal domains in order to generate emails

6) Emails are validated and the ones that are valid are printed out in decreasing order of confidence (i.e. the most probable emails are printed first)

### How To Use
Make sure you have obtained an Email Hippo key and have inputted it into `email_verifier.py` where it says `YOUR_KEY_HERE`

Here is the most basic example:
```
python -i main.py
>>> main(first_name='John', last_name='Doe')
```
With this example, it is hard to determine what the emails are because the name is such a common one. The more information provided, the easier the process becomes. For example, here we have:

```
python -i main.py
>>> main(first_name='Anand', last_name='Kuchibotla', domains=['akuchibotla.com'], linkedin_url='linkedin.com/in/akuchibotla', angellist_url='angel.co/anand-kuchibotla', github_url='github.com/akuchibotla')
```

In this example, the correct email is retrieved. Note that though every field except for `first_name` and `last_name` are optional, it is in your best interest to enter as much information as possible.

### Breakdown of Files
`main.py` runs the program, as outline above

`generator.py` exposes two functions that generate and weight possible usernames and possible emails from the infromation entered by the user

`crawler.py` crawls domains intelligently (it ignores files and only follows links within the domain)

`email_verifier.py` exposes a function that uses Email Hippo's API to return whether or not an email actually exists (must enter API key for this to work)

`mock_email_verifier.py` exposes a mock function to emulate `email_verifier.py` by returning 30% of emails inputted into it as valid

`utils.py` has some common functions used throughout the program