package config

import (
	"os"
	"path"
)

func SetConfig(gostorepath, servername, port string) error {
	os.Setenv("GOSTORE_PATH", gostorepath)
	data := []byte(
		"SERVERNAME: " + servername + "\nPORT: " + port)
	file, err := os.Create(path.Join(gostorepath, "gostore.conf"))
	if err != nil {
		return err
	}
	defer file.Close()

	_, err = file.Write(data)
	if err != nil {
		return err
	}
	return nil
}

func GetConfig() (string, error) {
	GOSTORE_PATH := os.Getenv("GOSTORE_PATH")
	dat, err := os.ReadFile(path.Join(GOSTORE_PATH, "gostore.conf"))
	if err != nil {
		return "", err
	}
	return string(dat), nil
}
