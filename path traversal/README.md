The url of any page looks like host/page=something. 
We can use this to traverse the directory structure. Changing the value of the page parameter to "../" we can go one step back in the directory structure.
This can be used to read files from the server, for example /etc/passwd.
This is a very common vulnerability. We're just using page=../../../../../../../../../etc/passwd to read the file.
flag: b12c4b2cb8094750ae121a676269aa9e2872d07c06e429d25a63196ec1c8c1d0