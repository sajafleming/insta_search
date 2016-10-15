![App Screen Shot](/readmescreenshot/screenshot.png)

Insta Search allows users to search for pictures by a hashtag and ranging between certain dates. Insta Search uses the Instagram API to query for results and shows the results to the user on the same page.

Backend challenges:

1. Fault tolerance: If the Instagram API does not respond in time, the system will die. Since I have no control over the external API and it has a risk of timing out, I added a NUM_RETRIES variable which will continue to retry the API call as many times as specified. (see get_photos.py)

2. Minimize API hits: In order to minimize API calls, I first check to see if I have the tag the user searched for stored in the database along with the end date of their date range. Note: the Instagram endpoint I am using only searches recent photos so there is no way I can go back in time and search for the start date which is why I only check for end date. If the tag and end date pair is not in my database, only then will I query the Instagram API.  (see date_tag_exists function in server.py)

3. Parallel processes: In order to have multiple searches happen at once, I need multiple threads. I added 3 threads to my Procfile by adding “-w 3”. Note: only 1 worker is available with the free tier of heroku, so my app is still only running with 1 thread. (see Procfile)

4. End date in the future: If the end date is in the future or if there is no end date given, I simply reassign the date to the current date. If there is no start date, I assign start date to an arbitrary low date so that when I check to see if the photo tag is > start date it will always be true. (see server.py lines 61-70)

Full-stack: Python, Javascript, JQuery, Flask, SQLAlchemy, PostgreSQL, HTML, CSS, Heroku
