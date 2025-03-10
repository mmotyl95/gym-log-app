terraform {
  backend "azurerm" {
    resource_group_name  = "flask-app-rg"
    storage_account_name = "flaskappstorage"
    container_name       = "tfstate"
    key                  = "terraform.tfstate"
  }
}

provider "azurerm" {
  features {}
}

resource "azurerm_container_registry" "acr" {
  name                = "flaskappacr"
  resource_group_name = "flask-app-rg"
  location            = "West Europe"
  sku                 = "Basic"
  admin_enabled       = true
}

resource "azurerm_service_plan" "app_plan" {
  name                = "flask-app-plan"
  resource_group_name = "flask-app-rg"
  location            = "West Europe"
  os_type             = "Linux"
  sku_name            = "B1"
}

resource "azurerm_app_service" "flask_app" {
  name                = "flask-app-service"
  resource_group_name = "flask-app-rg"
  location            = "West Europe"
  app_service_plan_id = azurerm_service_plan.app_plan.id

  site_config {
    linux_fx_version = "DOCKER|flaskappacr.azurecr.io/flask-app:latest"
  }

  app_settings = {
    DOCKER_REGISTRY_SERVER_URL      = "https://${azurerm_container_registry.acr.login_server}"
    DOCKER_REGISTRY_SERVER_USERNAME = azurerm_container_registry.acr.admin_username
    DOCKER_REGISTRY_SERVER_PASSWORD = azurerm_container_registry.acr.admin_password
  }
}