package menu

import (
	"fmt"
)

var currentChoice = 0

type Menu struct {
	currentChoice int
	choices       []string
	data          string
	onExit        func(choice int)
}

func (menu *Menu) print() {
	menu.formatCurrent()
	fmt.Print("\033[H\033[2J" + menu.data)
}

func (menu *Menu) start() {
	menu.print()
	inputGet(menu)
}

func (menu *Menu) formatCurrent() {
	total := ""
	for i, choice := range menu.choices {
		if i == menu.currentChoice {
			total += Colors.OKCYAN + Colors.BOLD + "==> " + choice + Colors.ENDC + "\n"
		} else {
			total += Colors.BOLD + "==> " + choice + Colors.ENDC + "\n"
		}
	}
	menu.data = total
}

func (menu *Menu) down() {
	if menu.currentChoice+1 != len(menu.choices) {
		menu.currentChoice += 1
	}
	menu.print()
}

func (menu *Menu) up() {
	if menu.currentChoice != 0 {
		menu.currentChoice -= 1
	}
	menu.print()
}

func (menu *Menu) exit() {
	menu.onExit(menu.currentChoice)
}

func StartMenu(choices []string, onExit func(choice int)) {
	menu := &Menu{0, choices, "", onExit}

	menu.start()
}
