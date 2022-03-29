package main

import (
	"fmt"
	"image"
	"image/png"
	"os"
)

func openPng(file string) image.Image {
	myFile, err := os.Open(file)
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
	defer myFile.Close()

	myImage, err := png.Decode(myFile)
	if err != nil {
		fmt.Println(err)
		os.Exit(2)
	}

	return myImage
}

func editPng(img image.Image) image.Image {
	myImage := img
	var color = img.At(0, 0)
	fmt.Println(color)

	return myImage
}

func main() {
	myImage := openPng("images/outImage.png")
	editPng(myImage)
	out, _ := os.Create("images/illusion.png")
	png.Encode(out, myImage)
	out.Close()
}
