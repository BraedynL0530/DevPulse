/*
Copyright © 2026 NAME HERE <EMAIL ADDRESS>
*/
package cmd

import (
	"bytes"
	"encoding/json"
	"fmt"
	"math"
	"net/http"
	"sort"
	"sync"
	"time"

	"github.com/spf13/cobra"
)

// analyticsCmd represents the analytics command
var analyticsCmd = &cobra.Command{
	Use:   "analytics",
	Short: "Gets latency and throughput",
	Long:  `long output for later`,
	Run: func(cmd *cobra.Command, args []string) {

		if test == true {
			metrics := collectMetrics(url)
			fmt.Println("Metrics:", metrics)
		}

		if interval <= 0 {
			collectAndSendMetrics(url, apikey) // single run
		} else {
			ticker := time.NewTicker(time.Duration(interval) * time.Second)
			defer ticker.Stop()
			for range ticker.C {
				collectAndSendMetrics(url, apikey)
			}
		}
	},
}

func collectAndSendMetrics(url, apikey string) {
	sendApi := "http://127.0.0.1:8000/api.devpulse/add-history" // Future me use env later for deployment (no local host:8000)
	metrics := collectMetrics(url)
	body, _ := json.Marshal(metrics)

	req, err := http.NewRequest(
		http.MethodPost,
		sendApi, // Link not the best naming
		bytes.NewBuffer(body),
	)

	if err != nil {
		return
	}

	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("API-Key", apikey)

	client := &http.Client{Timeout: 10 * time.Second}
	resp, err := client.Do(req)

	if err != nil {
		return
	}

	defer resp.Body.Close()
}

type RunMetrics struct {
	AvgLatency float64 `json:"avg_latency_ms"`
	P95Latency float64 `json:"p95_latency_ms"`
	Success    int     `json:"success"`
	Errors     int     `json:"errors"`
	Total      int     `json:"total"`
}

func collectMetrics(url string) RunMetrics {
	concurrency := 10
	duration := 5 * time.Second
	var wg sync.WaitGroup
	var mu sync.Mutex
	var totalRequest = 0
	var totalErrors = 0

	start := time.Now()
	deadline := start.Add(duration)
	latencies := []time.Duration{}

	for i := 0; i < concurrency; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			for time.Now().Before(deadline) {
				reqStart := time.Now()
				resp, err := http.Get(url)

				if err != nil {
					continue
				}
				if resp.StatusCode >= 400 {
					resp.Body.Close()
					mu.Lock()
					totalErrors++
					mu.Unlock()
					continue
				}

				latency := time.Since(reqStart)
				resp.Body.Close()

				mu.Lock()
				latencies = append(latencies, latency)
				totalRequest++
				mu.Unlock()
			}
		}()

	}

	wg.Wait()
	Success := totalRequest - totalErrors
	Errors := totalErrors

	sort.Slice(latencies, func(i, j int) bool {
		return latencies[i] < latencies[j]
	})

	var AvgLatency time.Duration
	var P95latency time.Duration
	if len(latencies) > 0 {
		P95Index := int(math.Ceil(0.95*float64(len(latencies)))) - 1
		P95latency = latencies[P95Index]
		AvgLatency = sum(latencies) / time.Duration(len(latencies))

	}

	return RunMetrics{
		AvgLatency: float64(AvgLatency) * 1e-6,
		P95Latency: float64(P95latency) * 1e-6,
		Success:    Success,
		Errors:     Errors,
		Total:      totalRequest + totalErrors,
	}

}

type History struct {
	ProjectName string  `json:"project_name"`
	ProjectId   string  `json:"project_id"`
	AvgLatency  float64 `json:"avg_latency_ms"`
	P95Latency  float64 `json:"p95_latency_ms"`
	Success     int     `json:"success"`
	Errors      int     `json:"errors"`
	Total       int     `json:"total"`
}

func exportHistory() {

}

func sum(durations []time.Duration) time.Duration {
	var total time.Duration
	for _, d := range durations {
		total += d
	}
	return total
}

var latencyThreshold int
var export string
var interval int
var apikey string
var url string
var test bool

func init() {
	rootCmd.AddCommand(analyticsCmd)
	analyticsCmd.Flags().IntVarP(&latencyThreshold, "latency-threshold", "l", 200, "Latency threshold for alert Defualts 200")
	analyticsCmd.Flags().StringVarP(&export, "export", "e", "json", "exports DB as a Json or CSV")
	analyticsCmd.Flags().BoolVarP(&test, "test", "t", false, "dosent send just collects and prints")
	analyticsCmd.Flags().IntVarP(&interval, "interval", "i", 0, "interval(seconds) of automatic request, off by defualt ")
	analyticsCmd.Flags().StringVarP(&apikey, "api-key", "a", "", "allows data to be stored and dashboard use") // Check config first if nil both require apikey, then check if ledgit
	analyticsCmd.Flags().StringVarP(&url, "url", "u", "", "Add url to your site")

}
