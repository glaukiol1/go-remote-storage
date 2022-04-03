package config

import (
	"os"
	"path"
	"strings"
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

type Sk_v struct {
	Key   string
	Value string
}

func GetConfigObj() ([]*Sk_v, error) {
	GOSTORE_PATH := os.Getenv("GOSTORE_PATH")
	dat, err := os.ReadFile(path.Join(GOSTORE_PATH, "gostore.conf"))
	if err != nil {
		return nil, err
	}
	data := string(dat)

	arr_data := strings.Split(data, "\n")

	var key_value_array []*Sk_v
	for _, v := range arr_data {
		k_v := strings.Split(v, ":")
		key := k_v[0]
		value := strings.ReplaceAll(k_v[1], " ", "")
		key_value_array = append(key_value_array, &Sk_v{key, value})
	}
	return key_value_array, nil
}
