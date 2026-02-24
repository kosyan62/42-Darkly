On almost every page in the footer there is a link to facebook, twitter, and instagram.
If we will look at the source code we will see that the links are not the real links to the social media pages, but they are links to the same page with a parameter "page=redirect" and "site=facebook". It is possible to redirect to any page by changing the value of the "site" parameter.
We're changin the value of the parameter to any value and we got the flag.

flag: b9e775a0291fed784a2d9680fcfad7edd6b8cdf87648da647aaf4bba288bcab3