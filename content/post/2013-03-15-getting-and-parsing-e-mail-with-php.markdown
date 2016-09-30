---
categories:
- How-To
comments: true
date: 2009-12-18
layout: post
title: Getting and Parsing E-mail with PHP
---

Here's my Problem:
My website sends text files to a partner's site via FTP. Our partner site sends us the results of their processing the file in an e-mail. This e-mail is a the direct output from their processing script. Or, the relevant details are buried in a bunch of garbled text. 

<!-- more -->

My Solution:
I first looked at message piping, but my hosting provider doesn't provide an easy way to do this.
Then I found <a href='http://www.phpclasses.org/browse/package/2.html' title='PHP Classes: POP3 e-mail client'>this PHP class</a> from PHP classes, which handles the interactions with the server. You do have to create an account with PHP classes to download the files. If you e-mail me directly, I could send them to you.
It's easy enough to get working quickly.
<pre lang="PHP">
$pop3->hostname="localhost";    // POP 3 server host name 

$user="username";                    // Authentication user name 
$password="password";             // Authentication password  

$pop3->debug=1;                    // Output debug information
$pop3->html_debug=1;            // Debug information is in HTML
</pre>
Edit the test_pop3.php file. All you need to do is change the sever name, user name and password to get rolling. After you see the full output and it's getting the mail correctly, I recommend setting the debug and html_debug values to 0. This will cut out the unnecessary text of the interaction with the server and just show you the messages and what's going on.

One hangup of this class, the body of the message is an array and the message was repeated twice in the array.  
<pre lang="PHP">array(14) {
  [0]=> string(30) "--0016e6d99d7ed848e5047b02e012"
  [1]=> string(44) "Content-Type: text/plain; charset=ISO-8859-1"
  [2]=> string(0) ""
  [3]=> string(71) "This is a test. If this were an actual message, important text would be"
  [4]=> string(5) "here."
  [5]=> string(0) ""
  [6]=> string(30) "--0016e6d99d7ed848e5047b02e012"
  [7]=> string(43) "Content-Type: text/html; charset=ISO-8859-1"
  [8]=> string(0) ""
  [9]=> string(77) "This is a test. If this were an actual message, important text would be here."
  [10]=> string(4) ""
  [11]=> string(0) ""
  [12]=> string(32) "--0016e6d99d7ed848e5047b02e012--"
  [13]=> string(0) ""
}</pre>
Luckily, the part boundaries are included in the array which makes it fairly easy to split the array and just get the message once.
<pre lang="PHP">
$oneBody = array();
$delimiter = $body[0];
$oneBody_i = 0;
for($body_i=3; $body_i&lt;count($body); $body_i++) // starts on 3 to skip the top of the body stuff
{
  if($body[$body_i] == $delimiter)
      break;
  $oneBody[$oneBody_i] = $body[$body_i];
  $oneBody_i++;
}</pre>

I needed to run some regular expressions on the body and imploded it into a single string.
<pre lang='php'>$bodyString = implode('', $oneBody);</pre>
Now I have the body of my e-mail message as a string variable ready for processing. Alternatively, you can change the first parameter in implode( to a line break if you need to display the message not as one long string.

Lastly, once you process your messages, you don't need them anymore.
<pre lang='PHP' escaped="true">
if(($error=$pop3->DeleteMessage($index))=="")
  echo "&lt;PRE&gt;Marked message $index for deletion.&lt;/PRE&gt;\n";
</pre>
The DeleteMessage( method will mark messages for deletion when you close the connection to your mail server. Please note that this method does not immediately delete the messages and messages can still be 'un-deleted' until the connection is closed. The ResetDeletedMessages( method is used to un-mark all messages for deletion.

Happy Parsing!!

--Chris
