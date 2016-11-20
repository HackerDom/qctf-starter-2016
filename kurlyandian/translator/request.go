package main

import (
	"fmt"
	"net"
	"net/http"
	"net/url"
)

type GatewayError struct {
	StatusCode int
	Message    string
}

func RequestPage(rawurl string) (*http.Response, *GatewayError) {
	parsedURL, gatewayErr := CheckAndParseURL(rawurl)
	if gatewayErr != nil {
		return nil, gatewayErr
	}

	targetHost := parsedURL.Host
	if ipRestrictions {
		parsedURL.Host = config.AllowedIP
	}
	request, err := http.NewRequest(http.MethodGet, parsedURL.String(), nil)
	if err != nil {
		return nil, &GatewayError{http.StatusBadRequest,
			"Failed to create a request on given URL: " + err.Error()}
	}
	request.Host = targetHost
	request.Header.Set("User-Agent", config.RequestUserAgent)

	client := new(http.Client)
	response, err := client.Do(request)
	if err != nil {
		return nil, &GatewayError{http.StatusBadGateway, "Request has failed: " + err.Error()}
	}

	if response.StatusCode != http.StatusOK {
		response.Body.Close()
		return nil, &GatewayError{http.StatusForbidden,
			fmt.Sprintf("Request returned status code %d, but only 200 is allowed", response.StatusCode)}
	}
	return response, nil
}

func CheckAndParseURL(rawurl string) (*url.URL, *GatewayError) {
	if rawurl == "" {
		return nil, &GatewayError{http.StatusBadRequest, "No URL provided"}
	}

	parsedURL, err := url.Parse(rawurl)
	if err != nil {
		return nil, &GatewayError{http.StatusBadRequest, "Invalid URL: " + err.Error()}
	}

	if parsedURL.Host == config.BannedDomain {
		return nil, &GatewayError{http.StatusForbidden,
			fmt.Sprintf("Domain %s is forbidden by the service administration", parsedURL.Host)}
	}

	if ipRestrictions {
		addrs, err := net.LookupHost(parsedURL.Host)
		if err != nil {
			return nil, &GatewayError{http.StatusNotFound, "Host not found: " + parsedURL.Host}
		}

		if len(addrs) != 1 || addrs[0] != config.AllowedIP {
			return nil, &GatewayError{http.StatusForbidden,
				fmt.Sprintf("Only pages on server %s can be translated", config.AllowedIP)}
		}
	}

	return parsedURL, nil
}
