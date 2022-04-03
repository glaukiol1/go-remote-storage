package main

import (
	menu "github.com/glaukiol1/go-arrow-menu"
	menuhandlers "github.com/glaukiol1/go-remote-storage/gostore-server/menu-handlers"
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
	options := []string{
		"Create A Server",
		"Start your current server",
		"Server status",
		"Review your config file",
	}
	menu.StartMenu(options, _main)
}
