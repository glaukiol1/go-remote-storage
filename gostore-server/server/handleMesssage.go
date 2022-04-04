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
		key_value := strings.Split(msg, ":")
		if len(key_value) != 2 {
			c.Write([]byte("TYPE_ERROR:invalid request"))
			c.Close()
			return
		}
		newMessageHandler(key_value[0], key_value[1], c).Handle(db)
		c.Close()
		break
	}
}
