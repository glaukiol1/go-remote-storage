package server

import (
	"bufio"
	"fmt"
	"net"
	"strings"
)

const (
	HEADER  = "\033[95m"
	OKCYAN  = "\033[96m"
	WARNING = "\033[93m"
	BOLD    = "\033[1m"
	ENDC    = "\033[0m"
	CLEAR   = "\033[H\033[2J"
	OKGREEN = "\033[92m"
	OKBLUE  = "\033[94m"
	FAIL    = "\033[91m"
)

func Start(port int) {
	go func() { serverStart(port) }()
}

func handleMessage(c net.Conn) {
	for {
		netData, err := bufio.NewReader(c).ReadString('\n')
		if err != nil {
			fmt.Println(err)
			return
		}
		msg := strings.TrimSpace(string(netData))
		println("New Msg: " + msg)
		c.Close()
		break
	}
}

func serverStart(port int) {
	fmt.Println(HEADER + BOLD + "==> Starting server in port " + fmt.Sprint(port) + "..." + ENDC)
	PORT := ":" + fmt.Sprint(port)
	l, err := net.Listen("tcp", PORT)
	if err != nil {
		fmt.Println(err)
		return
	}
	defer l.Close()
	fmt.Println(OKBLUE + BOLD + "==> Server successfully started, listening in localhost:" + fmt.Sprint(port) + ENDC)

	for {
		c, err := l.Accept()
		if err != nil {
			fmt.Println(err)
			return
		}
		go handleMessage(c)
	}
}
