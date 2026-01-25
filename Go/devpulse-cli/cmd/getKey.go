/*
Copyright © 2026 NAME HERE <EMAIL ADDRESS>
*/
package cmd

import (
	"log"

	"github.com/pkg/browser"
	"github.com/spf13/cobra"
)

// getKeyCmd represents the getKey command
var getKeyCmd = &cobra.Command{
	Use:   "getKey",
	Short: "A brief description of your command",
	Long: `A longer description that spans multiple lines and likely contains examples
and usage of using your command. For example:

Cobra is a CLI library for Go that empowers applications.
This application is a tool to generate the needed files
to quickly create a Cobra application.`,
	Run: func(cmd *cobra.Command, args []string) {
		url := "http://127.0.0.1:8000/api.devpulse/get-apikeys" // Placeholder
		if err := browser.OpenURL(url); err != nil {            // This function handles cross-platform differences for you
			log.Fatalf("Error opening URL in browser: %v", err)
		}
	},
}

func init() {
	rootCmd.AddCommand(getKeyCmd)
}
