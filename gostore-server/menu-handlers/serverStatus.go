package menuhandlers

import (
	"fmt"
	"net"
	"os"
	"strconv"

	"github.com/glaukiol1/go-remote-storage/gostore-server/config"
)

func ServerStatus() {
	fmt.Println(CLEAR + HEADER + BOLD + "==> GoStore | Server Status..." + ENDC)
	fmt.Println("\n" + OKBLUE + BOLD + "==> Reading Config File..." + ENDC)
	k_v, err := config.GetConfigObj()
	if err != nil {
		fmt.Println(WARNING + BOLD + "Failed to parse config file... " + err.Error())
		os.Exit(1)
	}
	fmt.Println(OKGREEN + BOLD + "Successfully read config file at $GOSTORE_PATH")
	var port int
	for _, v := range k_v {
		if v.Key == "PORT" {
			port, err = strconv.Atoi(v.Value)
			if err != nil {
				fmt.Println(WARNING + BOLD + "Failed to parse config file... " + err.Error())
				os.Exit(1)
			}
		}
	}
	_, err = net.Dial("tcp4", "localhost:"+fmt.Sprint(port))
	if err != nil {
		fmt.Println(FAIL + BOLD + "==> Server at localhost:" + fmt.Sprint(port) + " is not available.")
		os.Exit(1)
	}
	fmt.Println(OKBLUE + BOLD + "==> Server at localhost:" + fmt.Sprint(port) + " is available!")

}
