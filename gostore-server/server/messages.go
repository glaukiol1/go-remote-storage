package server

import (
	"fmt"
	"net"

	"go.mongodb.org/mongo-driver/mongo"
)

type messageHandler struct {
	Key        string
	Value      string
	Connection net.Conn
}

func (mh *messageHandler) Handle(db *mongo.Client) {
	fmt.Println("New command requested; " + mh.Key)
	switch mh.Key {
	case "TYPE_LOGIN":
		login(mh.Connection, mh.Value, db)
	case "TYPE_ECHO":
		type_echo(mh.Connection)
	case "TYPE_SIGNUP":
		signup(mh.Connection, mh.Value, db)
	default:
		not_found(mh.Connection)
	}
}

func type_echo(conn net.Conn) {
	conn.Write([]byte("TYPE_TEXT:SRV_NAME+ECHO"))
}

func not_found(conn net.Conn) {
	conn.Write([]byte("TYPE_ERROR:invalid request"))
	conn.Close()
}

func newMessageHandler(key, value string, conn net.Conn) *messageHandler {
	return &messageHandler{key, value, conn}
}
