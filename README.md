##TeamForum

###A Demo Team Management Application

<p><strong> Developer: Francis Kessie</strong></p>

<p><stong>website: http://teamforum.pythonanywhere.com</strong></p>

<p><strong>Hi, Welcome to TeamForum.</strong></p>
<p>TeamForum is a program I am developing to help people organize and manage their teams better. I have an idea to create an application for managing teams that I lead, now i am begining to put it into code. Effective communication is key to successful team management. Then,  I firmly believe that a well organized team is a winning team and would likely achieve more than a poorly organized one.</p>
<p>Whether you are planning a field trip, organizing a program, or just for your day to day communication with colleagues and employees in your department or entire company, TeamForum can help you communicate better. </p>

<p>At the moment the program has a discussions forum and a program planning segments </p>
<p><strong>I have listed some features below.</strong></p><br>
<p><b>Chat Forum</b></p>
<ol>
<li><p>Once you sign up, you have become a member of the team.</p>
</li>
<li><p>You can start a new forum or participate in existing forums.</p>
</li>
<li><p>All members who have signed up to be in the team will be notified by email immediately you create a new forum. The email notification is made up of the title of the post you have created plus 30 characters  in the description you gave the post. Usually, the description should be short and should provide a brief overview of the content of the forum. Members can then log into TeamForum to see the full post and make their contributions.</p>
</li>
<li><p>When you start participating in a forum, you will be recorded as a member in that forum. You will receive email notifications (as above) from that forum when every other member in that particular forum makes a contribution. People in the team who have not contributed to a particular forum will not receive any notifications about post made by people in that forum.</p>
</li>
<li><p>You can start as many post as possible and comment in forums  unlimited number of times.</p>
</li>
<li><p>You can delete or edit the content of a new forum that you authored. You can also edit or delete a contribution you have made in on other people's forum. And of course the admin can delete anything you posted in the forum. No notifications will be given when you edit or delete a contribution in the forum. I particularly like this feature because you can quickly change the content of your communication before members get to see it  </p>
<li><p>There is a time stamp on every post you made. So new posts are placed at the top. And every post you edit get promoted to the top so members can see it quickly.</p>
</li>
</li>
<li><p>TeamFurom uses a Markdown down parser called Mistune and you can format your post nicely using Markdown tags.</p>
</li>
<li><p>You can access the raw post from a forum in JSON format. But you must be logged in first to be able to do this.</p>
<pre><code>     To access all post: 
      http://teamforum.pythonanywhere.com/post/JSON

      To access a single post:
      http://teamforum.pythonanywhere.com/post/&lt;postid&gt;JSON
</code></pre>
</li>
</ol>

<p><b>Program Planning Tool</b></p>
<ol>
<li>You can create a new program</li><br>

<li>Under a program you have created you can Create a list of task to be accomplished</li><br>

<li>When creating a task you can assign different tasks to members in the Forum and also apply due dates to the task</li><br>

<li>Under a program you also have an option to create a registration page if you are going to be registering people. The program allows you to record few information about the people registered. You will see the total number of people registered at the top of the registration table as you add new people</li>

</ol>

