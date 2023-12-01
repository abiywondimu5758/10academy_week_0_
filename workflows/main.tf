provider "aws" {
  region = "#REGION"
}

resource "aws_instance" "example" {
  ami           = "AMI"
  instance_type = "t2.micro"
}
