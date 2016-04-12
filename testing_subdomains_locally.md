From: https://reinteractive.net/posts/199-developing-and-testing-rails-applications-with-subdomains
and http://www.daveoncode.com/2016/01/29/testing-flask-subdomain-routing-locally/

The `lvh.me` domain has specifically been set up to resolve itself
and all subdomains to 127.0.0.1

So you can test subdomains by going to e.g. `sub.lvh.me`.
Note you have to set the SERVER_NAME config to e.g. `lvh.me:5000`
