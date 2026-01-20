/*
Copyright © 2026 NAME HERE <EMAIL ADDRESS>
*/
package cmd

import (
	"fmt"

	"github.com/spf13/cobra"
)

// analyticsCmd represents the analytics command
var analyticsCmd = &cobra.Command{
	Use:   "analytics",
	Short: "Gets latency and throughput",
	Long:  `long output for later`,
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Println("analytics called")
		//if interval <= 0 {
		//collectAndSendMetrics() // single run
		//} else {
		//    ticker := time.NewTicker(time.Duration(interval) * time.Second)
		//    defer ticker.Stop()
		//    for {
		//collectAndSendMetrics()
		// <-ticker.C
		//    }
		//}
	},
}

var latencyThreshold int
var export string
var interval int
var apikey string

func init() {
	rootCmd.AddCommand(analyticsCmd)
	analyticsCmd.Flags().IntVarP(&latencyThreshold, "latency-threshold", "lt", 200, "Latency threshold for alert Defualts 200")
	analyticsCmd.Flags().StringVarP(&export, "Export", "e", "json", "exports DB as a Json or Strings/CSV")
	analyticsCmd.Flags().IntVarP(&interval, "interval", "i", 0, "interval of automatic request, defult 0(off)")
	analyticsCmd.Flags().StringVarP(&apikey, "api-key", "a", "", "allows data to be stored and dashboard use") // Check config first if nil both require apikey, then check if ledgit

}
