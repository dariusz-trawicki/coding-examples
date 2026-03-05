output "ec2_instance_id" {
  description = "EC2 instance ID"
  value       = aws_instance.demo.id
}

output "ec2_public_ip" {
  description = "Public IP for SSH"
  value       = aws_instance.demo.public_ip
}

output "ec2_public_dns" {
  description = "Public DNS for SSH"
  value       = aws_instance.demo.public_dns
}

output "sns_topic_arn" {
  description = "SNS Topic ARN"
  value       = aws_sns_topic.cpu_alert.arn
}

output "alarm_name" {
  description = "CloudWatch alarm name"
  value       = aws_cloudwatch_metric_alarm.high_cpu.alarm_name
}

output "ssh_command" {
  description = "Ready-to-use SSH command"
  value       = "ssh -i '${replace(var.public_key_path, ".pub", "")}' ec2-user@${aws_instance.demo.public_dns}"
}
