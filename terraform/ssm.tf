data "aws_ssm_parameter" "pypi_token" {
  name = "/pypi/test/token"
}
