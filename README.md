# 📁 go-remote-storage
Remote File Storage written in Go (server) & Python (client). It is made for demonstrational purposes on how to create a remote storage client & server with communication over TCP (no FTP!). The files are also being sent through TCP, not FTP.


  
## ℹ️ General Info

This is a project which demonstrates a secure and easy way to program a remote file storage application. It has user accounts, which are stored in a MongoDB database. Users can login using the _gostore-client_ python program. Each user has their own folder, and they can perform actions, or run commands. All these commands or actions are being proccessed by the Server. To make this interaction user-friendly, I have created a VSH (virtual shell) in which users can run simple commands and get prompts instead of having to manually send packets to the server. The _vsh_ is also a part of _gostore-client_.

You can specific documentation below:

|Package|Link|Package written in|
|----|----|----|
|Client|(Not created)[docs](gostore-client/README.md)|Python|
|Server|[docs](gostore-server/README.md)|Go (Go-lang)|

## :memo: TO-DOS

TODOs for both client and server.

- Add a `mkdir` command and proccess it in the server | **Done**
- Show the _all_ the response messages on error (client) | **Done**
- When the pipe has been closed or errored, show a _fatal_ error message and quit. (client)
- Better format the `ls` command (client) | **Done**
- Add signup (server & client) | **Done**
- Create a .username folder on signup (server) | **Done**
- Encrypt the files | **Done**
- Display errors in the client VHS, not display plain response on error.
- Do not reset connection when the client enters the _get_ filename incorrectly.
- Display how many mb's were sent to the server when using _send_ and at what speed (mb/s).

#
