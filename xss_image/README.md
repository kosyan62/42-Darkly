On the main page there are several images but only one of them has a link attribute.
The link attribute seems to be vulnerable to XSS. If we will click on image, we will get on a page url/?page=media&src=nsa.
nsa there is a parameter which will be rendered inside object tag.
so we can inject javascript code. src=data:text/html;base64,PHNjcmlwdD5hbGVydCgnWFNTJyk8L3NjcmlwdD4=, which will be rendered as <script>alert(1)</script>.
In our case we will get the flag instead of alert box.
Flag: 928d819fc19405ae09921a2b71227bd9aba106f9d2d37ac412e9e5a750f1506d
