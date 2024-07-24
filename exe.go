package main

import (
	"flag"
	"fmt"
	"io/ioutil"
	"log"
	"regexp"
	"time"

	expect "github.com/google/goexpect"
	"github.com/google/goterm/term"
)

const (
	timeout = 10 * time.Minute
)

var (
	addr = flag.String("address", "", "address of telnet server")
	user = flag.String("user", "", "username to use")
	pass = flag.String("pass", "", "password to use")
	cmd  = flag.String("cmd", "", "command to run")

	userRE = regexp.MustCompile("Username:")
	passRE = regexp.MustCompile("Password:")
	table  = regexp.MustCompile("Interface")
)

type InterfaceStatus struct {
	Interface   string `json:"interface"`
	Status      string `json:"status"`
	Protocol    string `json:"protocol"`
	Description string `json:"description"`
}

func main() {
	flag.Parse()
	fmt.Println(term.Bluef("Telnet 1 example"))

	e, _, err := expect.Spawn(fmt.Sprintf("telnet %s", *addr), -1)
	if err != nil {
		log.Fatal(err)
	}
	defer e.Close()

	e.Expect(userRE, timeout)

	fmt.Println(user)

	e.Send(*user + "\n")

	e.Expect(passRE, timeout)

	e.Send(*pass + "\n")

	time.Sleep(3 * time.Second)

	e.Send(*cmd + "\n")

	time.Sleep(3 * time.Second)

	result, _, _ := e.Expect(table, timeout)
	e.Send("exit\n")

	fmt.Println(term.Greenf("%s: result: %s\n", *cmd, result))

	// Define the file path
	filePath := "status.log"

	// Write the JSON data to the file
	err = ioutil.WriteFile(filePath, []byte(result), 0644)
	if err != nil {
		fmt.Println("Error writing to file:", err)
		return
	}

	fmt.Println("JSON data written to", filePath)
}
