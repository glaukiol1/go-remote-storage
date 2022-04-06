# gostore-server (Server Package)

This is the server of the `go-remote-storage` monorepo. It has all the files for running a gostore server, written in Go. A goal of the _gostore_ project was to make it as user-friendly as possible, and it has been followed in writing this server package.

With default options, the server listens on `localhost:12368`. You __must__ have a MongoDB atlas set up (free). You can find instructions on Google.

After starting the server, it will output any data from important requests, like `cmd_ls` or `cmd_rm`. This is important to see as a SysAdmin if someone is trying to exploit the server.

`I can't access my server from another computer, why?` Well this can be due to the port not being forwarded on your network. In order for other computers outside your network to access the server, you need to [Port Forward](https://portforward.com/) port `12368 (default)`. Then give people your IP (public) and port 12368 for them to connect (using VHS).

To access your server from the local network, have another computer with _gostore-client_ (vhs) installed. Get your local IP of your server computer, and then connect the VHS using your local server IP for `srv_ip` and `12368` for `srv_port` (in vhs).


## :gear: Create a gostore Server

Setting up the gostore server is _very_ simple. It was created as simply as possible so you can start it with minimal knowledge.

### With `make` installed

If you have `make` installed on your system, follow these steps. If not, scroll down to the `No make installation` section.

#### Step #0

Check if you have `go` installed in your system. You can do this by running `go version`. If it outputs the current `go` version, go onto the next step. If not, follow these steps.

- Go [here](https://golang.google.cn/dl/). This is the official Google Go download page.
- Download the version for your platform.

#### Step #1

Go to the `gostore-server` directory if you aren't already there.

- run `make`

If there is no error, continue onto the next step. If there is a error, please _open a issue_ in this GitHub repo.

#### Step #2

Now, a menu will be in your command line, that probably looks like this:

```txt
==> Create A Server
==> Start your current server
==> Server status
==> Review your config file
```

- Make sure `Create A Server` is selected, and press enter.
- Follow the prompts, it will be very simple to follow them.
- ___WARNING___: The `Server Name` must __NOT__ have any spaces or special characters.
- Once the `Successfully read config file at $GOSTORE_PATH` message appeares, a new `gostore.conf` file has been made in the path you specified before.

#### Step #3

Once you are prompted `==> Would you like to start the server? (y/n) `, type `y` and press enter. If everything is good, then your server is up and running.

### No `make` installation

If you don't have `make` installed on your system, follow the steps below.

#### Step #0

Check if you have `go` installed in your system. You can do this by running `go version`. If it outputs the current `go` version, go onto the next step. If not, follow these steps.

- Go [here](https://golang.google.cn/dl/). This is the official Google Go download page.
- Download the version for your platform.

#### Step #1

Run:
- `go build -o gstore-server && make run`
- `./gstore-server`

If there are no errors, follow the next steps.

#### Step #2

Now, a menu will be in your command line, that probably looks like this:

```txt
==> Create A Server
==> Start your current server
==> Server status
==> Review your config file
```

- Make sure `Create A Server` is selected, and press enter.
- Follow the prompts, it will be very simple to follow them.
- ___WARNING___: The `Server Name` must __NOT__ have any spaces or special characters.
- Once the `Successfully read config file at $GOSTORE_PATH` message appeares, a new `gostore.conf` file has been made in the path you specified before.

#### Step #3

Once you are prompted `==> Would you like to start the server? (y/n) `, type `y` and press enter. If everything is good, then your server is up and running.

## Other menu options

What the other 3 menu options do:

- `Start your current server` will start your server if you have created a server using the CLI before.
- `Server status` will return the server status. (Running/Not Running)
- `Review your config file` prints your config file.

