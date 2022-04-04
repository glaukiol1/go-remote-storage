package menuhandlers

import (
	"fmt"
	"os"
	"strconv"
	"strings"

	"github.com/glaukiol1/go-remote-storage/gostore-server/config"
	"github.com/glaukiol1/go-remote-storage/gostore-server/server"
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

func CreateServer() {
	fmt.Println(CLEAR + HEADER + BOLD + "==> GoStore | Create Server..." + ENDC)
	fmt.Print("Enter Server Name: ")
	var servername string
	fmt.Scanln(&servername)
	fmt.Print("Enter full path for the GoStore server: ")
	var gostorepath string
	fmt.Scanln(&gostorepath)

	fmt.Println("\n" + OKBLUE + BOLD + "==> Writing Config File..." + ENDC)

	err := config.SetConfig(gostorepath, servername, "12368")

	if err != nil {
		fmt.Println(WARNING + BOLD + "Error while writting config file... " + err.Error())
		os.Exit(1)
	}

	fmt.Println(OKGREEN + BOLD + "Successfully wrote config file at $GOSTORE_PATH")

	fmt.Println("\n" + OKBLUE + BOLD + "==> Reading Config File..." + ENDC)
	conf, err := config.GetConfig()

	if err != nil {
		fmt.Println(WARNING + BOLD + "Error while reading config file... " + err.Error())
		os.Exit(1)
	}
	fmt.Println(OKGREEN + BOLD + "Successfully read config file at $GOSTORE_PATH")

	fmt.Println("\n" + OKCYAN + BOLD + "==> gostore.conf:\n" + ENDC + conf)
	fmt.Println("\n" + OKBLUE + BOLD + "==> Successfully set configs" + ENDC)
	fmt.Print("\n\n")
	fmt.Println(WARNING + BOLD + "==> Would you like to start the server? (y/n) " + ENDC)
	var startserver string
	fmt.Scanln(&startserver)
	if startserver == "y" {
		fmt.Println("\n" + OKBLUE + BOLD + "==> Reading Config File..." + ENDC)
		k_v, err := config.GetConfigObj()
		if err != nil {
			fmt.Println(WARNING + BOLD + "\nError while reading config file... " + err.Error())
			os.Exit(1)
		}
		fmt.Println(OKGREEN + BOLD + "\nSuccessfully read config file at $GOSTORE_PATH")
		for _, v := range k_v {
			if v.Key == "PORT" {
				port, err := strconv.Atoi(strings.TrimSpace(v.Value))
				if err != nil {
					panic(err)
				}
				server.Start(port)
				for {
				}
			}

		}
		fmt.Println(WARNING + BOLD + "Failed to parse config file... " + err.Error())
		os.Exit(1)
	}
}
