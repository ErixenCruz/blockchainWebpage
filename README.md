# blockchainWebpage
Erixen Cruz ec622@drexel.edu
6 December 2019
SE 575 Professor Brian Mitchell
Blockchain webpage with Python and Django

This solution was developed and tested on tux. ssh to tux.cs.drexel.edu with
-L8000:0.0.0.0:8000 for ssh tunneling for the webpage.

Run "bash setup.bash" or "./setup.bash" to create a virtual environment in the
directory and install django in it.

Then activate the virtual environment with "source blockchainWebpageEnv/bin/activate".

Then you can launch the server with "./runServer.bash".

Then you can view the solution at 127.0.0.1:8000/blocks/ on a web browser.


The difficulty for hash solving is 5. The parallel mining algorithm uses 4
threads, so it is roughly 4 times faster than the sequential implementation.

Video of usage is at https://www.youtube.com/watch?v=deVJgNq0pBE
