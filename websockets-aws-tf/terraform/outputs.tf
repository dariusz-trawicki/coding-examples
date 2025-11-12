output "alb_dns_name" {
  description = "ALB address. Use ws://<this>/ws in the client"
  value       = aws_lb.this.dns_name
}
output "ecr_repo_url" {
  value = aws_ecr_repository.repo.repository_url
}
