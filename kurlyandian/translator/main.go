package main

import (
	"bytes"
	"io"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"path"
	"path/filepath"
	"regexp"
)

var (
	config struct {
		ListenOn, AllowedIP, BannedDomain, RequestUserAgent string
	}
	ipRestrictions bool

	translator *Translator

	executableDir  = filepath.Dir(os.Args[0])
	configFilename = path.Join(executableDir, "config.json")
	dictFilename   = path.Join(executableDir, "dictionary.txt")
	templateDir    = path.Join(executableDir, "templates")
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

	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		http.ServeFile(w, r, path.Join(templateDir, "index.html"))
	})
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

	contentBytes, err := ioutil.ReadAll(io.LimitReader(response.Body, pageSizeLimit))
	if err != nil {
		w.WriteHeader(http.StatusBadGateway)
		w.Write([]byte("Failed to read the response"))
		return
	}

	content := translator.Translate(string(contentBytes))

	headerBuf := new(bytes.Buffer)
	pageHeaderTemplate.Execute(headerBuf, struct{ URL string }{rawurl})
	content = bodyBeginRegexp.ReplaceAllStringFunc(content, func(matched string) string {
		return matched + headerBuf.String()
	})

	w.Write([]byte(content))
}

var bodyBeginRegexp = regexp.MustCompile(`<body.*?>`)
var pageHeaderTemplate = loadTemplate("page_header.html")

const pageSizeLimit = 10 * 1024 * 1024
