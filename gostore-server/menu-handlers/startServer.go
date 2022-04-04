package menuhandlers

import (
	"fmt"
	"os"
	"strconv"
	"strings"

	"github.com/glaukiol1/go-remote-storage/gostore-server/config"
	"github.com/glaukiol1/go-remote-storage/gostore-server/server"
)

func StartServer() {
	fmt.Println(BOLD + HEADER + "==> Starting server..." + ENDC)
	fmt.Println("\n" + OKBLUE + BOLD + "==> Reading Config File..." + ENDC)
	k_v, err := config.GetConfigObj()
	if err != nil {
		fmt.Println(WARNING + BOLD + "\nError while reading config file... " + err.Error())
		os.Exit(1)
	}
	fmt.Println(OKGREEN + BOLD + "\nSuccessfully read config file at $GOSTORE_PATH")
	var PORT int
	var MONGOSRV string
	for _, v := range k_v {
		if v.Key == "PORT" {
			PORT, err = strconv.Atoi(strings.TrimSpace(v.Value))
			if err != nil {
				panic(err)
			}
		} else if v.Key == "MONGOSRV" {
			MONGOSRV = strings.TrimSpace(v.Value)
		}
	}
	server.Start(PORT, MONGOSRV)
	for {
	}
}
