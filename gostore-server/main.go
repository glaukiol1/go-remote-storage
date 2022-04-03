package main

import (
	"fmt"

	menu "github.com/glaukiol1/go-arrow-menu"
	menuhandlers "github.com/glaukiol1/go-remote-storage/gostore-server/menu-handlers"
)

const (
	HEADER  = "\033[95m"
	OKCYAN  = "\033[96m"
	WARNING = "\033[93m"
	BOLD    = "\033[1m"
	ENDC    = "\033[0m"
	CLEAR   = "\033[H\033[2J"
)

func _main(choice int) {
	switch choice {
	case 0:
		menuhandlers.CreateServer()
	case 1:
		menuhandlers.StartServer()
	case 2:
		menuhandlers.ServerStatus()
	case 3:
		menuhandlers.ReviewConfig()
	}
}

func main() {
	fmt.Println(HEADER + BOLD + "GoStore Server Command-Line Utility" + ENDC)
	options := []string{
		"Create A Server",
		"Start your current server",
		"Server status",
		"Review your config file",
	}
	menu.StartMenu(options, _main)
}
