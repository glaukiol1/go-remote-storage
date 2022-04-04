package server

import (
	"bufio"
	"fmt"
	"net"
	"strings"

	"go.mongodb.org/mongo-driver/mongo"
)

func handleMessage(c net.Conn, db *mongo.Client) {
	for {
		netData, err := bufio.NewReader(c).ReadString('\n')
		if err != nil {
			fmt.Println(err)
			return
		}
		msg := strings.TrimSpace(string(netData))
		key := strings.Split(msg, ":")[0]
		value := strings.Join(strings.Split(msg, ":")[1:], ":")
		if !(len(key) > 0) && !(len(value) > 0) {
			c.Write([]byte("TYPE_ERROR:invalid request"))
			c.Close()
			return
		}
		newMessageHandler(key, value, c).Handle(db)
		c.Close()
		break
	}
}
