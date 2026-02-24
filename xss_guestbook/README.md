This vulnerability is broken. 
Usually for ctf XSS is a vulnerability where you can inject some html/javascript code into the page. But in this case, the vulnerability is that you can inject some html/javascript code into the page.
To check for possible XSS I'm using <script>alert(1)</script>. 1 is just a number which will appear in the alert box. If the alert box appears, it means that the code is executed and the vulnerability is present.
In this case, input is properly sanitized, but when your input is jsut "script", the flag appears on the page.

Flag: 0fbb54bbf7d099713ca4be297e1bc7da0173d8b3c21c1811b916a3a86652724e