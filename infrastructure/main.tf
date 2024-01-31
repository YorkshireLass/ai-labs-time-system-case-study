# terraform/main.tf

/*
  The below configuration assumes that the existing cluster already has the following set up:
   - Load Balancer
   - Security Groups
   - Network configuraton
   - IAM Roles
   - IAM Policies
   - Logging
*/

# TODO : Set variable values
variable "aws_access_key" {}
variable "aws_secret_key" {}
variable "ecs_cluster_name" {}

provider "aws" {
  region     = "eu-west-2"
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key
}

resource "aws_ecs_task_definition" "default" {
  family                  = "AILabsTimeSystem"
  container_definitions   = jsonencode([
    {
      "name": "backend-server",
      "image": "hanwood/ailabstimesystem-server:latest",
      "cpu": 256,
      "memory": 512,
      "essential": true,
      "portMappings": [
        {
          "containerPort": 80,
          "hostPort": 80
        }
      ]
    }
  ])
}

resource "aws_ecs_service" "service" {
  name            = "AILabsTimeSystem_ECS_Service"
  cluster         = var.ecs_cluster_name
  task_definition = aws_ecs_task_definition.default.arn
  launch_type     = "FARGATE"
  desired_count   = 1
}
