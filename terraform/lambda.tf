data "aws_iam_policy_document" "get_config_secret" {
  statement {
    effect = "Allow"
    actions = [ "secretsmanager:GetSecretValue" ]
    resources = [ aws_secretsmanager_secret.config.arn ]
  }
}

data "aws_iam_policy_document" "write_cloudwatch_metrics" {
  statement {
    effect = "Allow"
    actions = [ "cloudwatch:PutMetricData" ]
    resources = [ "*" ]
  }
}


module "temperature_collector_lambda" {
  source = "terraform-aws-modules/lambda/aws"
  version = "1.47.0"
  function_name = "temperature-collector"
  description = "Collects temperatures from various devices and APIs and writes them to CloudWatch"
  handler = "handler.lambda_handler"
  runtime = "python3.8"
  source_path = "../lambdas/temperature-collector"
  environment_variables = {
    CONFIG_ARN = aws_secretsmanager_secret.config.arn
  }
  attach_policy_jsons = true
  number_of_policy_jsons = 2
  policy_jsons = [
    data.aws_iam_policy_document.get_config_secret.json,
    data.aws_iam_policy_document.write_cloudwatch_metrics.json,
  ]
  memory_size = 128
  timeout = 30
}
