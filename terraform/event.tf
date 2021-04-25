resource "aws_cloudwatch_event_rule" "temperature_collector" {
  name = "temperature-collector-event-rule"
  description = "Execute the Temperature Collector every 5 minutes"
  schedule_expression = "rate(5 minutes)"
}


resource "aws_cloudwatch_event_target" "temperature_collector" {
  rule = aws_cloudwatch_event_rule.temperature_collector.*.name[0]
  arn = module.temperature_collector_lambda.this_lambda_function_arn
}


resource "aws_lambda_permission" "temperature_collector_trigger" {
  principal = "events.amazonaws.com"
  action = "lambda:InvokeFunction"
  function_name = module.temperature_collector_lambda.this_lambda_function_name
  source_arn = aws_cloudwatch_event_rule.temperature_collector.arn
}
