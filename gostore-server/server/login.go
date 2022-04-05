package server

import (
	"bufio"
	"context"
	"fmt"
	"io/fs"
	"net"
	"os"
	"path"
	"strconv"
	"strings"
	"time"

	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
)

func handle_after_login(conn net.Conn, username_password []string) {
	netData, err := bufio.NewReader(conn).ReadString('\n')
	if err != nil {
		fmt.Println(err)
		return
	}
	cmd := strings.TrimSpace(string(netData))
	if cmd == "TYPE_END" {
		return
	}
	if strings.HasPrefix(cmd, "CMD_LS") {
		cmd_ls(conn, strings.Split(cmd, ":")[1:], username_password)
	}
	if strings.HasPrefix(cmd, "TYPE_GET") {
		type_get(conn, strings.Split(cmd, ":")[1:], username_password)
	}
	handle_after_login(conn, username_password)
}

func getFileJSON(file fs.DirEntry) []byte {
	return []byte(" {\"name\":\"" + file.Name() + "\", \"isDir\":" + strconv.FormatBool(file.IsDir()) + "}\n")
}

func cmd_ls(conn net.Conn, args []string, username_password []string) {
	GOSTORE_PATH := os.Getenv("GOSTORE_PATH")
	if len(args) != 1 {
		conn.Write([]byte("TYPE_ERROR:PASS DIR ARG"))
		return
	}
	fmt.Println(args)
	files, err := os.ReadDir(path.Join(
		GOSTORE_PATH,
		"."+strings.TrimSpace(username_password[0]),
		args[0]))
	if err != nil {
		conn.Write([]byte("TYPE_NOT_ACCESS_DIR"))
		return
	}
	if len(files) == 0 {
		conn.Write([]byte("TYPE_NO_FILES"))
	}
	for _, file := range files {
		conn.Write(getFileJSON(file))
	}
}

func split(buf []byte, lim int) [][]byte {
	var chunk []byte
	chunks := make([][]byte, 0, len(buf)/lim+1)
	for len(buf) >= lim {
		chunk, buf = buf[:lim], buf[lim:]
		chunks = append(chunks, chunk)
	}
	if len(buf) > 0 {
		chunks = append(chunks, buf[:])
	}
	return chunks
}

func type_get(conn net.Conn, args []string, username_password []string) {
	GOSTORE_PATH := os.Getenv("GOSTORE_PATH")
	if len(args) != 1 {
		conn.Write([]byte("TYPE_ERROR:PASS DIR ARG"))
		conn.Close()
		return
	}
	fmt.Println(args)
	file_bytes, err := os.ReadFile(path.Join(
		GOSTORE_PATH,
		"."+strings.TrimSpace(username_password[0]),
		args[0]))
	if err != nil {
		conn.Write([]byte("TYPE_ERROR:COULDN'T ACCESS FILE"))
		conn.Close()
		return
	}
	conn.Write([]byte("TYPE_START_RESPONSE\n"))
	arrs := split(file_bytes, 1024)
	for _, arr := range arrs {
		conn.Write(arr)
	}
	conn.Write([]byte("TYPE_END_RESPONSE\n"))
}

func login(conn net.Conn, message string, client *mongo.Client) {
	ctx, cancel := context.WithTimeout(context.Background(), 80*time.Second)
	defer cancel()
	fmt.Println("New attempted login: " + message)
	users_db := client.Database("users")
	user_collection := users_db.Collection("users")

	username_password := strings.Split(message, ":")

	if len(username_password) != 2 {
		not_found(conn)
		return
	}
	user := user_collection.FindOne(ctx, bson.M{"username": username_password[0]})
	var user_field bson.M
	err := user.Err()
	if err != nil {
		fmt.Println(err.Error())
		conn.Write([]byte("TYPE_ERROR:USER_NOT_FOUND"))
		conn.Close()
		return
	}
	err = user.Decode(&user_field)
	if err != nil {
		conn.Write([]byte("TYPE_ERROR:DB_ERROR"))
		conn.Close()
		return
	}
	if user_field["username"] == strings.TrimSpace(username_password[1]) {
		conn.Write([]byte("TYPE_SUCCESS:LOGGED_IN\n"))
		if err != nil {
			not_found(conn)
			return
		}
		handle_after_login(conn, username_password)
	} else {
		conn.Write([]byte("TYPE_ERROR:DB_ERROR"))
		conn.Close()
		return
	}
}
