resource "aws_iam_role" "sagemakeraccess" {
  name = var.role_name

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "sagemaker.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "attach_sagemaker_full" {
  role       = aws_iam_role.sagemakeraccess.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSageMakerFullAccess"
}
