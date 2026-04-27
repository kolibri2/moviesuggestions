provider "aws" {
  region = "eu-north-1"  # or whichever region
}

# ECR
resource "aws_ecr_repository" "movie_rec_repo" {
  name = "movie-recommendation"
}

# VPC

resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
  tags = {
    Name = "movie-recommendation-vpc"
  }
}

resource "aws_subnet" "public" {
    vpc_id = aws_vpc.main.id
    cidr_block = "10.0.0.0/24"
    map_public_ip_on_launch = true
}

resource "aws_internet_gateway" "main" {
    vpc_id = aws_vpc.main.id
}

resource "aws_route_table" "public" {
    vpc_id = aws_vpc.main.id

    route {
        cidr_block = "0.0.0.0/0"
        gateway_id = aws_internet_gateway.main.id
    }
}

resource "aws_route_table_association" "public" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public.id
}

# security group

resource "aws_security_group" "movie_recommendation_sg" {
  name        = "movie_recommendation_sg"
  description = "allow inbound traffic on p8000 and all outbound traffic"
  vpc_id      = aws_vpc.main.id

  tags = {
    Name = "movie_recommendation_sg"
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


# iam role

resource "aws_iam_role" "ecsTaskExecutionRole" {
  name = "ecsTaskExecutionRole"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect    = "Allow"
        Principal = { Service = "ecs-tasks.amazonaws.com" }
        Action    = "sts:AssumeRole"
      }
    ]
  })
}


resource "aws_iam_role_policy_attachment" "ecsTaskExecutionRole_policy" {
  role       = aws_iam_role.ecsTaskExecutionRole.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}


# cluster

resource "aws_ecs_cluster" "movie_recommendation_cluster" {
  name = "movie-rec-cluster"
}

resource "aws_ecs_task_definition" "movie_recommendation_task" {
  family                   = "movie-recommendation-task"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 256
  memory                   = 512
  execution_role_arn       = aws_iam_role.ecsTaskExecutionRole.arn

  container_definitions = jsonencode([
    {
      name      = "movie-rec"
      image     = "${aws_ecr_repository.movie_rec_repo.repository_url}:latest"
      essential = true
      portMappings = [
        {
          containerPort = 8000
          protocol      = "tcp"
        }
      ]
    }
  ])
}