package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"regexp"
	"strings"
)

type Translator struct {
	Dict map[string]string
}

func NewTranslator(dictFilename string) (*Translator, error) {
	f, err := os.Open(dictFilename)
	if err != nil {
		return nil, err
	}
	defer f.Close()
	content, err := ioutil.ReadAll(f)
	if err != nil {
		return nil, err
	}

	lines := strings.Split(string(content), "\n")
	result := &Translator{Dict: make(map[string]string)}
	for _, line := range lines {
		if line == "" {
			continue
		}

		chunks := strings.Split(line, dictSeparator)
		if len(chunks) != 2 {
			return nil, fmt.Errorf("Line doesn't contain exactly two chunks separated by '%s': %s",
				dictSeparator, line)
		}

		result.Dict[chunks[0]] = chunks[1]
	}
	return result, nil
}

const dictSeparator = " = "

func (translator *Translator) Translate(text string) string {
	for key, value := range translator.Dict {
		expr := regexp.MustCompile(`(^|\PL)` + regexp.QuoteMeta(key) + `($|\PL)`)
		text = expr.ReplaceAllString(text, `${1}`+regexp.QuoteMeta(value)+`${2}`)
	}
	return text
}
