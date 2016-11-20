package main

import (
	"encoding/json"
	"io"
	"io/ioutil"
	"log"
	"net/http"
	"os"
)

var (
	config struct {
		ListenOn, AllowedIP, RequestUserAgent string
	}
	ipRestrictions bool

	translator *Translator
)

const (
	configFilename = "config.json"
	dictFilename = "dictionary.txt"
)

func main() {
	err := loadData(configFilename, &config)
	if err != nil {
		log.Fatal("failed to load config file: ", err)
	}
	ipRestrictions = config.AllowedIP != "*"
	if !ipRestrictions {
		log.Print("debug mode: IP restrictions are disabled")
	}

	translator, err = NewTranslator(dictFilename)
	if err != nil {
		log.Fatal("failed to load translator dictionary: ", err)
	}
	log.Printf("%d string pairs are loaded from dictionary", len(translator.Dict))

	http.HandleFunc("/translate", HandleTranslate)

	log.Print("listening on ", config.ListenOn)
	log.Fatal(http.ListenAndServe(config.ListenOn, nil))
}

func HandleTranslate(w http.ResponseWriter, r *http.Request) {
	rawurl := r.URL.Query().Get("url")
	response, gatewayErr := RequestPage(rawurl)
	if gatewayErr != nil {
		w.WriteHeader(gatewayErr.StatusCode)
		w.Write([]byte(gatewayErr.Message))
		return
	}
	defer response.Body.Close()

	content, err := ioutil.ReadAll(io.LimitReader(response.Body, pageSizeLimit))
	if err != nil {
		w.WriteHeader(http.StatusBadGateway)
		w.Write([]byte("Failed to read the response"))
		return
	}
	w.Write([]byte(translator.Translate(string(content))))
}

const pageSizeLimit = 10 * 1024 * 1024

func loadData(filename string, v interface{}) error {
	f, err := os.Open(filename)
	if err != nil {
		return err
	}
	defer f.Close()

	return json.NewDecoder(f).Decode(v)
}
