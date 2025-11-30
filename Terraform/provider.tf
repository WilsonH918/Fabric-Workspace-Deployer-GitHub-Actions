terraform {
  required_version = ">= 1.3"
  required_providers {
    fabric = {
      source  = "microsoft/fabric"
      version = ">= 1.0.0"
    }
  }
}

provider "fabric" {
    preview = true
}