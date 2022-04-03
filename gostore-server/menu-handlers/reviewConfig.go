package menuhandlers

import (
	"fmt"
	"os"

	"github.com/glaukiol1/go-remote-storage/gostore-server/config"
)

func ReviewConfig() {
	fmt.Println("\n" + OKBLUE + BOLD + "==> Reading Config File..." + ENDC)
	conf, err := config.GetConfig()

	if err != nil {
		fmt.Println(WARNING + BOLD + "Error while reading config file... " + err.Error())
		os.Exit(1)
	}
	fmt.Println(OKGREEN + BOLD + "Successfully read config file at $GOSTORE_PATH")

	fmt.Println("\n" + OKCYAN + BOLD + "==> gostore.conf:\n" + ENDC + conf)
	fmt.Println("\n" + HEADER + BOLD + "==> Done")
}
