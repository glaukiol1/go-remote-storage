package server

import (
	"context"
	"fmt"
	"net"
	"os"
	"path"
	"strings"
	"time"

	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
)

func isValidPath(path string) bool {
	f := func(r rune) bool {
		return r < 'A' || r > 'z'
	}

	return strings.IndexFunc(path, f) == -1
}

func signup(conn net.Conn, message string, client *mongo.Client) {
	ctx, cancel := context.WithTimeout(context.Background(), 80*time.Second)
	defer cancel()
	fmt.Println("New attempted signup: " + message)
	users_db := client.Database("users")
	user_collection := users_db.Collection("users")

	username_password := strings.Split(message, ":")

	hasUsername := user_collection.FindOne(ctx, bson.M{
		"username": username_password[0],
	})

	if hasUsername.Err() == nil {
		// a user with this username exists
		conn.Write([]byte("TYPE_ERROR:Username is already registered.\n"))
		conn.Close()
		return
	}
	GOSTORE_PATH := os.Getenv("GOSTORE_PATH")
	lpath := path.Join(GOSTORE_PATH)
	fpath := path.Join(GOSTORE_PATH,
		"."+strings.TrimSpace(username_password[0]))
	isValidPath := isValidPath(username_password[0])
	if !isValidPath {
		conn.Write([]byte("TYPE_ERROR:INVALID_USERNAME\n"))
		conn.Close()
		return
	}
	if strings.HasPrefix(fpath, lpath) {
		res, err := user_collection.InsertOne(ctx, bson.D{
			{Key: "username", Value: username_password[0]},
			{Key: "password", Value: username_password[1]},
		})
		if err != nil {
			conn.Write([]byte("TYPE_ERROR\n"))
			return
		}
		os.MkdirAll(fpath, os.ModePerm)
		conn.Write([]byte("TYPE_SUCCESS:ID:" + fmt.Sprint(res.InsertedID) + "\n"))
		conn.Close()
	} else {
		conn.Write([]byte("TYPE_ERROR:INVALID_USERNAME\n"))
		conn.Close()
	}
}
