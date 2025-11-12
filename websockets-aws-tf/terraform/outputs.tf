output "alb_dns_name" {
  description = "Adres ALB. Użyj ws://<to>/ws w kliencie"
  value       = aws_lb.this.dns_name
}
output "ecr_repo_url" {
  value = aws_ecr_repository.repo.repository_url
}
