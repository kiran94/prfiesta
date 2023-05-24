data "aws_ssm_parameter" "pypi_token" {
  name = "/pypi/token"
}

data "aws_ssm_parameter" "pypi_test_token" {
  name = "/pypi/test/token"
}
