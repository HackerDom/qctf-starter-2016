package main

import (
	"encoding/json"
	"html/template"
	"log"
	"os"
	"path"
)

func loadData(filename string, v interface{}) error {
	f, err := os.Open(filename)
	if err != nil {
		return err
	}
	defer f.Close()

	return json.NewDecoder(f).Decode(v)
}

func loadTemplate(name string) *template.Template {
	filepath := path.Join(templateDir, name)
	result, err := template.New(name).ParseFiles(filepath)
	if err != nil {
		log.Fatalf("failed to load %s: %s\n", filepath, err)
	}
	return result
}
