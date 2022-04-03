package main

import (
	"fmt"

	menu "github.com/glaukiol1/go-arrow-menu"
)

func _main(choice int) {
	fmt.Print("Choice: " + fmt.Sprint(choice))
}

func main() {
	options := []string{
		"Create A Server",
		"Start your current server",
		"Review your config file",
	}
	menu.StartMenu(options, _main)
}
