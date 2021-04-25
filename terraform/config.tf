resource "aws_secretsmanager_secret" "config" {
  name = "temperature-collector-config"
  description = "Configuration values for the Temperature Collector"
}
