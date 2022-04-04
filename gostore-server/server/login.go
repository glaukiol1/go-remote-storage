package server

import (
	"context"
	"fmt"
	"net"
	"time"

	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
)

func login(conn net.Conn, message string, client *mongo.Client) {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	users_db := client.Database("users")
	user_collection, err := users_db.Collection("users").Find(ctx, bson.M{})

	if err != nil {
		panic(err)
	}

	var Users []*User

	if err = user_collection.All(ctx, &Users); err != nil {
		panic(err)
	}

	for _, v := range Users {
		fmt.Println(v.Username, v.Password)
	}
	conn.Write([]byte("echo: " + message))
	conn.Close()
	return
}
