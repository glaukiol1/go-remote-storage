package menuhandlers

import (
	"fmt"
	"os"

	"github.com/glaukiol1/go-remote-storage/gostore-server/config"
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
}
