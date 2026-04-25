provider "aws" {
  region = "eu-north-1"  # or whichever region
}

resource "aws_ecr_repository" "movie_rec_repo" {
  name = "movie-recommendation"
}