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
	Short: "redircts to api key link",
	Long:  `redirects you to obtain api key for history, graphs, and sending to server.`,
	Run: func(cmd *cobra.Command, args []string) {
		url := "http://127.0.0.1:8000/devpulse/get-apikeys" // Placeholder/env for deplotment/docker
		if err := browser.OpenURL(url); err != nil {        // This function handles cross-platform differences
			log.Fatalf("Error opening URL in browser: %v", err)
		}
	},
}

func init() {
	rootCmd.AddCommand(getKeyCmd)
}
