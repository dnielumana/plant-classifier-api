terraform {
    required_providers {
        aws = {
            source  = "hashicorp/aws"
            version = "~> 5.0"
        }
    }
}

provider "aws" {
    region = "us-east-1"
}

resource "aws_security_group" "api_sg" {
    name        = "plant-classifier-sg"
    description = "Allow HTTP and SSH traffic"

    ingress {
        from_port   = 22
        to_port     = 22
        protocol    = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    ingress {
        from_port   = 8000
        to_port     = 8000
        protocol    = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    egress {
        from_port   = 0
        to_port     = 0
        protocol    = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }
}

resource "aws_instance" "api_server" {
    ami           = "ami-0fe74bfcad4fd6bd2"
    instance_type = "t3.micro"
    vpc_security_group_ids = [aws_security_group.api_sg.id]
    key_name = aws_key_pair.deploy_key.key_name

    tags = {
        Name = "plant-classifier-api"
    }
}

resource "aws_key_pair" "deploy_key" {
    key_name   = "plant-classifier-key"
    public_key = file("~/.ssh/plant-classifier-key.pub")
}

output "instance_public_ip" {
    value = aws_instance.api_server.public_ip
}