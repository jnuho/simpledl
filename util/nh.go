package main

import (
	"bytes"
	"crypto/rand"
	"encoding/json"
	"fmt"
	"math/big"
	"net/http"
	"os"
	"time"

	"github.com/joho/godotenv"
)

type Header struct {
	ApiNm        string `json:"ApiNm"`
	Tsymd        string `json:"Tsymd"`
	Trtm         string `json:"Trtm"`
	Iscd         string `json:"Iscd"`
	FintechApsno string `json:"FintechApsno"`
	ApiSvcCd     string `json:"ApiSvcCd"`
	IsTuno       string `json:"IsTuno"`
	AccessToken  string `json:"AccessToken"`
}

type RequestBody struct {
	Header   Header `json:"Header"`
	Bncd     string `json:"Bncd"`
	Acno     string `json:"Acno"`
	Insymd   string `json:"Insymd"`
	Ineymd   string `json:"Ineymd"`
	TrnsDsnc string `json:"TrnsDsnc"`
	Lnsq     string `json:"Lnsq"`
	PageNo   string `json:"PageNo"`
	Dmcnt    string `json:"Dmcnt"`
}

func main() {
	err := godotenv.Load(".env")
	if err != nil {
		fmt.Println("Error loading .env file")
		return
	}
	url := "https://developers.nonghyup.com/InquireTransactionHistory.nh"

	accessToken := os.Getenv("nh_access_token")
	iscd := os.Getenv("nh_Iscd")

	min := big.NewInt(0)
	max := big.NewInt(10000)

	randomBigInt, err := rand.Int(rand.Reader, new(big.Int).Sub(max, min))
	randStr := fmt.Sprintf("%05d", randomBigInt.Int64())
	fmt.Println(randStr)

	// Format the current date as YYYYMMdd
	t := time.Now()
	today := fmt.Sprintf("%04d%02d%02d", t.Year(), int(t.Month()), t.Day())

	requestBodyData := RequestBody{
		Header: Header{
			ApiNm:        "InquireTransactionHistory",
			Tsymd:        today,
			Trtm:         "112428",
			Iscd:         iscd,
			FintechApsno: "001",
			ApiSvcCd:     "ReceivedTransferA",
			// IsTuno:       "0099",
			AccessToken: accessToken,
		},
		Bncd:     "011",
		Acno:     "3020000010330",
		Insymd:   "20240301",
		Ineymd:   "20240607",
		TrnsDsnc: "A",
		Lnsq:     "DESC",
		PageNo:   "1",
		Dmcnt:    "100",
	}

	requestBody, err := json.Marshal(requestBodyData)
	if err != nil {
		fmt.Println("Error encoding request body:", err)
		return
	}

	resp, err := http.Post(url, "application/json", bytes.NewBuffer(requestBody))
	if err != nil {
		fmt.Println("Error making POST request:", err)
		return
	}
	defer resp.Body.Close()

	// Handle response as needed
	fmt.Print(resp.Body)
}
